from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import os
import time
from PyPDF2 import PdfReader
from io import BytesIO
import requests

from application.http_session_rpa import HttpSessionRpa
from application.extract_notification_base import ExtractNotificationBase

from google.cloud import storage
import logging


logger = logging.getLogger(__name__)

class ExtractNotificationManual(ExtractNotificationBase):
    def __init__(self):
        pass

    @staticmethod
    def upload_to_gcs(pdf_content: bytes, destination_path: str):
        bucket_name = "notificaciones-sunat-store"

        try:
            client = storage.Client(project="estudios-contables")
            bucket = client.bucket(bucket_name)

            blob = bucket.blob(destination_path)
            blob.upload_from_file(pdf_content, content_type="application/pdf")

            logger.info(f"Archivo subido a gs://{bucket_name}/{destination_path}")

        except Exception as e:
            logger.error(f"Error al subir archivo a GCS: {e}")


    def extract(self, session: HttpSessionRpa):
        url = "https://ww1.sunat.gob.pe/ol-ti-itvisornoti/visor/bajarArchivo"
        notification_data = []

        try:
            WebDriverWait(session.automator.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.NAME, "iframeApplication"))
            )

            notification_elements = WebDriverWait(session.automator.driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, '//ul[@id="listaMensajes"]/li'))
            )

            for notification in notification_elements:
                logger.debug(notification.get_attribute("outerHTML"))
                soup = BeautifulSoup(notification.get_attribute("outerHTML"), 'html.parser')

                subject = soup.find('a', class_="linkMensaje text-muted").text
                publish_date = soup.find('small', class_="text-muted fecPublica").text
                notification_id = notification.get_property('id') 
                notification_type = "SIN TIPO"
                if len(soup.select('div>span[class*="label tag"]')) > 0:
                    notification_type = soup.select('div>span[class*="label tag"]')[0].text

                try:
                    link_element = notification.find_element(By.CLASS_NAME, "linkMensaje")
                    link_element.click()
                except Exception as e:
                    logger.warning(f"Elemento no encontrado: {e}")
                    continue

                session.automator.driver.switch_to.frame(session.automator.driver.find_element(By.NAME, "contenedorMensaje"))

                cookies_dict = {cookie['name']: cookie['value'] for cookie in session.automator.driver.get_cookies()}

                try:
                    page_source = session.automator.driver.page_source
                    soup_detail = BeautifulSoup(page_source, 'html.parser')

                    download_links = soup_detail.find_all('a', href=lambda x: x and "goArchivoDescarga" in x)
                    gcs_paths = []

                    for download_link in download_links:
                        onclick_text = download_link['href']
                        params = onclick_text.split('goArchivoDescarga(')[1].split(')')[0].split(',')
                        id_archivo, ind_mensaje, id_mensaje = [p.strip() for p in params]

                        logger.info(f"Descargando archivo - ID Mensaje: {id_mensaje}, ID Archivo: {id_archivo}, Ind Mensaje: {ind_mensaje}")

                        data = {
                            "accion": "archivo",
                            "idMensaje": id_mensaje,
                            "idArchivo": id_archivo,
                            "sistema": ind_mensaje,
                            "indMensaje": "5"
                        }

                        response = requests.post(url, data=data, cookies=cookies_dict)

                        if response.status_code == 200:
                            content_type = response.headers.get('Content-Type')
                            content_disposition = response.headers.get('Content-Disposition', '')

                            filename = "{}_{}_{}".format(id_mensaje, id_archivo, ind_mensaje)
                            if "filename=" in content_disposition:
                                filename += "_" + content_disposition.split("filename=")[-1].strip().replace('"', '')
                            # file_path = os.path.join("descargas", filename)
                            # os.makedirs("descargas", exist_ok=True)

                            # with open(file_path, "wb") as f:
                            #     f.write(response.content)

                            # logger.info(f"Archivo guardado: {file_path}")

                            if "application/pdf" in content_type:
                                try:
                                    pdf_bytes = BytesIO(response.content)
                                    gcs_path = f"20606208414/20606208414/{notification_type}/{filename}".replace(" ", "_")
                                    ExtractNotificationManual.upload_to_gcs(pdf_bytes, gcs_path)
                                    gcs_paths.append("gs://notificaciones-sunat-store/" + gcs_path)
                                    # pdf_text = "".join(page.extract_text() or "" for page in reader.pages)
                                    # logger.info(f"Texto extraído del PDF:{pdf_text[:1000]}")
                                except Exception as e:
                                    gcs_path = None
                                    logger.warning(f"Error al subir el PDF a GCS: {e}")
                            else:
                                logger.info(f"Archivo descargado, pero no es un PDF. Tipo de contenido: {content_type}")
                        else:
                            logger.warning(f"No se pudo descargar el archivo {id_archivo}, status: {response.status_code}")

                except Exception as e:
                    logger.warning(f"No se pudo acceder al iframe del mensaje: {e}")

                notification_info = {
                    "id": notification_id,
                    "subject": subject,
                    "publish_date": publish_date,
                    "type": notification_type,
                    "url_archivo": ",".join(gcs_paths)
                }
                notification_data.append(notification_info)
                
                session.automator.driver.switch_to.default_content()
                WebDriverWait(session.automator.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "iframeApplication")))

        except Exception as e:
            logger.error(f"Error inesperado en el proceso de extracción: {e}")
        finally:
            session.automator.driver.quit()
        return notification_data
