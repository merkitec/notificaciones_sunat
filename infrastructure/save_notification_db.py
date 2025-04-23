import logging
from application.save_notification_base import SaveNotificationBase
import requests
from datetime import datetime, timezone
import json

logger = logging.getLogger(__name__)

class SaveNotificationDb(SaveNotificationBase):
    def __init__(self, config=None):
        super().__init__()
        self.config = config

    def save(self, notifications, ruc):
        logger.info("Guardando en base de datos")

        # Get all the Notificacion Types
        notificacion_types = self.call_get_notificacion_types_endpoint()

        # Get the Ruc object
        ruc = self.call_get_ruc_endpoint(ruc)

        for notification in notifications:
            tipo_notificacion = [t for t in notificacion_types if str(t['nombre']).upper() == str(notification["type"]).upper()]
            if len(tipo_notificacion) == 0:
                tipo_notificacion = [t for t in notificacion_types if str(t['nombre']).upper() == 'SIN TIPO']
            self.call_create_notificacion_endpoint(
                notification["id"],
                notification["subject"],
                datetime.strptime(notification["publish_date"], "%d/%m/%Y %H:%M:%S").isoformat(),
                ruc["id"],
                tipo_notificacion[0]["id"],
                False,
                datetime.now(timezone.utc).isoformat(),
                'EXTRACT_PROCESS',
                notification["url_archivo"]
            )
            logger.info(f"Notification saved: {notification['id']}")

    def call_get_ruc_endpoint(self, ruc):
        """
        Calls the get_ruc FastAPI endpoint.

        Parameters:
        - ruc (str): The RUC (Tax Identification Number) to retrieve.

        Returns:
        - dict: JSON response from the API.

        Raises:
        - requests.HTTPError: If the request fails.
        """
        # Construct the endpoint URL
        base_url = self.config["URLS"]["persist_base_url"]
        url = f"{base_url.rstrip('/')}/rucs/{ruc}"
        logger.info(f"Calling endpoint: {url}")

        # Send the GET request
        response = requests.get(url)

        # Raise an exception for HTTP error responses
        response.raise_for_status()

        # Return the response as JSON
        return json.loads(response.text)

    def call_get_notificacion_types_endpoint(self):
        """
        Calls the get_notificacion_types FastAPI endpoint.

        Returns:
        - dict: JSON response from the API.

        Raises:
        - requests.HTTPError: If the request fails.
        """
        # Construct the endpoint URL
        base_url = self.config["URLS"]["persist_base_url"]
        url = f"{base_url.rstrip('/')}/tipos_notificacion?skip=0&limit=100"
        logger.info(f"Calling endpoint: {url}")

        # Send the GET request
        response = requests.get(url)

        # Raise an exception for HTTP error responses
        response.raise_for_status()

        # Return the response as JSON
        return json.loads(response.text)

    def call_create_notificacion_endpoint(self,
        notificacion_id: str,
        asunto: str,
        fecha_publicacion: str = None,
        ruc_id: int = None,
        tipo_id: int = None,
        eliminado: bool = False,
        fecha_creacion: str = None,
        usuario_creador: str = None,
        url_archivo: str = None
    ):
        """
        Calls the create_notificacion_endpoint FastAPI endpoint.
        
        Parameters:
        - notificacion_id (str): Notification identifier.
        - asunto (str): The subject or description of the notification.
        - fecha_publicacion (str, optional): Publication date in ISO 8601 format.
        - ruc_id (int, optional): ID of the Ruc.
        - tipo_id (int, optional): ID of the TipoNotificacion.
        - eliminado (bool, optional): Flag indicating if the notification is marked as deleted.
        - fecha_creacion (str, optional): Creation timestamp in ISO 8601 format.
        - usuario_creador (str, optional): Username of the creator.
        
        Returns:
        - dict: JSON response from the API.
        
        Raises:
        - requests.HTTPError: If the request fails.
        """
        # Set default creation timestamp if not provided
        if fecha_creacion is None:
            fecha_creacion = datetime.now().isoformat()
        
        # Build the payload for the POST request
        payload = {
            "notificacion_id": notificacion_id,
            "asunto": asunto,
            "fecha_publicacion": fecha_publicacion,
            "ruc_id": ruc_id,
            "tipo_id": tipo_id,
            "eliminado": eliminado,
            "fecha_creacion": fecha_creacion,
            "usuario_creador": usuario_creador,
            "url_archivo": url_archivo
        }
        
        # Remove keys where the value is None
        payload = {key: value for key, value in payload.items() if value is not None}
        
        # Construct the endpoint URL
        base_url = self.config["URLS"]["persist_base_url"]
        url = f"{base_url.rstrip('/')}/notificaciones/"
        logger.info(f"Calling endpoint: {url}")
        logger.debug(json.dumps(payload, indent=2))

        # Send the POST request
        response = requests.post(url, json=payload)
        
        # Raise an exception for HTTP error responses
        response.raise_for_status()
        
        logger.info(f"Save Notificacion = {notificacion_id} - request status: {response.status_code}")
        # Return the response as JSON
        return response.json()

# Example usage:
if __name__ == "__main__":
    import configparser
    config = configparser.ConfigParser()
    config.read("config.ini")

    save = SaveNotificationDb(config)

    try:
        result = save.save(
            [
                {
                    "id": "notif001",
                    "subject": "Test Notification",
                    "publish_date": datetime.now(timezone.utc).isoformat(),
                    "type": "VALORES"
                }
            ],
            "20606208414"
        )
        # result = save.call_create_notificacion_endpoint(
        #     notificacion_id="notif001",
        #     asunto="Test Notification",
        #     fecha_publicacion=datetime.now(timezone.utc).isoformat(),
        #     ruc_id="20606208414",
        #     tipo_id="VALORES",
        #     usuario_creador="testuser"
        # )
        print("Response from API:", result)
    except requests.HTTPError as e:
        print("HTTP error occurred:", e)
    except Exception as e:
        print("An error occurred:", e)
