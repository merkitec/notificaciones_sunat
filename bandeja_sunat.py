import time
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service as ChromeService
import datetime
import pyautogui as robot

######## V A R I A B L E S   G E N E R A L E S   ###########


def prueba_v2():
    
    url_start = 'https://e-menu.sunat.gob.pe/cl-ti-itmenu/MenuInternet.htm'

    ruc = '20606208414'

    user = 'ALLODANS'

    psw = 'fulsildsp'

    ######## X PATH NECESARIOS #######

    x_input_login_ruc = 'html//input[@id="txtRuc"]'

    x_input_login_user = 'html//input[@id="txtUsuario"]'

    x_input_login_psw = 'html//input[@id="txtContrasena"]'

    x_bottom_login_ingreso = 'html//button[@id="btnAceptar"]'

    x_bottom_buzon = 'html//a[@id="aOpcionBuzon"]'



    # O P C I O N E S     S E L E N I U M:

    opciones = webdriver.ChromeOptions()

    opciones.add_experimental_option("excludeSwitches",['enable-automation'])
    prefs = {"credentials_enable_service": False,"profile.password_manager_enabled": False}
    opciones.add_experimental_option("prefs", prefs)
    opciones.add_argument("user-data-dir=C:\\Users\\josej\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 3")
    driver =  webdriver.Chrome(options=opciones)
    driver.maximize_window()
    wait = WebDriverWait(driver,60)


    ########   P R O C E S O      G E N E R A L   ###########

    ##### Ingreso a SUNAT

    driver.get(url_start)

    # Ingresando datos para iniciar sesión:
    wait.until(ec.visibility_of_element_located((By.XPATH,x_input_login_ruc)))
    driver.find_element(By.XPATH,x_input_login_ruc).send_keys(ruc)
    driver.find_element(By.XPATH,x_input_login_user).send_keys(user)
    driver.find_element(By.XPATH,x_input_login_psw).send_keys(psw)
    time.sleep(0.7)
    driver.find_element(By.XPATH,x_bottom_login_ingreso).click()
    driver.find_element(By.XPATH,x_bottom_buzon).click()
    time.sleep(10)
    


prueba_v2()