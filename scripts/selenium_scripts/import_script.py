import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

# Path to chromedriver
PATH = "C:\chromedriver.exe"
URL = "https://localhost:8091/admin1"
EMAIL = "bizneselektronicznylampy@gmail.com"
PASSWORD = "bizneselektroniczny"
PRODUCTS = '1'
CATEGORY = '0'
ATTRIBUTES = '2'
PRODUCTS_CONFIG = "products_config"
CATEGORY_CONFIG = "category_config"
COMBINATIONS_CONFIG ="combinations_config"

def load(file_path,option,config,driver, force_id = False, delete_before_import = True, reset = True):


    select_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "entity"))
    )
    select_object = Select(select_element)
    select_object.select_by_value(option)
    time.sleep(1)

    file_box = driver.find_element_by_id("file")
    time.sleep(1)
    file_box.send_keys(file_path)
    #loading file
    time.sleep(3)

    if force_id:
        driver.execute_script("document.getElementById('forceIDs_1').checked = true")
        time.sleep(1)

    if delete_before_import:
        driver.execute_script("document.getElementById('truncate_1').checked = true")

    import_file_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.NAME, "submitImportFile"))
    )
    import_file_button.click()

    if reset:
        driver.switch_to.alert.accept()

    select_configuration =  Select(WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "valueImportMatchs"))
    ))


    select_configuration.select_by_visible_text(config)
    time.sleep(1)

    WebDriverWait(driver, 10).until(
     EC.presence_of_element_located((By.ID, "loadImportMatchs"))
    ).click()

    driver.find_element_by_id("skip").send_keys(Keys.BACK_SPACE)
    driver.find_element_by_id("skip").send_keys(1)
    time.sleep(1)

    import_button = driver.find_element_by_id("import")
    import_button.click()

    success_button = WebDriverWait(driver, 10000000).until(
        EC.element_to_be_clickable((By.ID, "import_close_button"))
    )
    success_button.click()

if __name__ == "__main__":

    driver = webdriver.Chrome(PATH)
    driver.maximize_window()
    driver.get(URL)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login"))
    )

    email_field = driver.find_element_by_id("email")
    password_field = driver.find_element_by_name("passwd")
    submit_button = driver.find_element_by_id("submit_login")

    email_field.clear()
    password_field.clear()

    email_field.send_keys(EMAIL)
    password_field.send_keys(PASSWORD)

    submit_button.submit()

    try:
        advanced_subtab = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.ID, "subtab-AdminAdvancedParameters"))
        )

        import_link = advanced_subtab.find_element_by_id("subtab-AdminImport")\
            .find_element_by_tag_name("a").get_attribute('href')

        reset_link = advanced_subtab.find_element_by_id("subtab-AdminLogs")\
            .find_element_by_tag_name("a").get_attribute('href')
        driver.get(import_link)
        load(os.getcwd() + "/categories.csv",CATEGORY, CATEGORY_CONFIG, driver, delete_before_import=False, reset= False)
        load(os.getcwd() + "/lamps.csv",PRODUCTS,PRODUCTS_CONFIG, driver,force_id=True)
        load(os.getcwd() + "/attributes.csv",ATTRIBUTES, COMBINATIONS_CONFIG, driver)

    finally:
        driver.quit()

