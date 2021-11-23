import time
import random
import names
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\chromedriver.exe"
URL = "https://localhost:8091"
PRODUCTS_NUM = 2
FIRST_CATEGORY_PRODUCTS_NUM = 1
FIRST_CATEGORY = '/index.php?id_category=17&controller=category'
SECOND_CATEGORY = '/index.php?id_category=24&controller=category'

#FIRST_CATEGORY = '/index.php?id_category=7&controller=category'
#SECOND_CATEGORY = '/index.php?id_category=15&controller=category'

class Test:

    def __init__(self, driver, url, products_num, first_category_products_num, first_category, second_category):
        self.driver = driver
        self.url = url
        self.products_num = products_num
        self.first_category_products_num = first_category_products_num
        self.second_category_products_num = products_num - first_category_products_num
        self.first_category_url = url + '/' + first_category
        self.second_category_url = url + '/' + second_category

    def test(self):
        self.fill_cart(self.first_category_products_num, self.first_category_url)
        self.fill_cart(self.second_category_products_num, self.second_category_url)

        selected_product_index = random.randint(0,self.products_num - 1)
        self.remove_product(selected_product_index)
        self.create_account()
        self.fill_order_form()

    def fill_cart(self, products_num, category_url):
        added_products = 0
        current_page_number = 1

        while(added_products<products_num):
            self.driver.get(category_url + '?page=' + str(current_page_number))
            try:
                products_on_page = len(WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product'))
                ))
            except Exception:
                print('Not enough products for this category: ' + category_url)
                return

            for product_index in range(products_on_page):
                if (added_products >= products_num):
                    break

                products = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'product'))
                )

                products[product_index].click()
                added_products += self.add_one_product()

                self.driver.get(category_url + '?page=' + str(current_page_number))

            current_page_number += 1


    def add_one_product(self):
        NOT_ADDED = 0
        ADDED = 1
        try:
            product_quantities = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.product-quantities > span'))
            )
        except Exception:
            return NOT_ADDED

        quantity = product_quantities.get_attribute('data-stock')

        if int(quantity) == 0:
            return NOT_ADDED

        selected_quantity = random.randint(1,int(quantity))
        driver.find_element_by_id('quantity_wanted').clear()
        driver.find_element_by_id('quantity_wanted').send_keys(Keys.BACK_SPACE)
        driver.find_element_by_id('quantity_wanted').send_keys(selected_quantity)
        driver.find_element_by_css_selector('.add > button').click()

        btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'.cart-content-btn > button'))
        )
        btn.click()
        return ADDED

    def remove_product(self, selected_product_index):
        cart_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.header > a'))
        )
        cart_link.click()

        remove_links = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.remove-from-cart'))
        )
        remove_links[selected_product_index].click()

        cart_itmes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.cart-item'))
        )


    def create_account(self):
        FIRST_NAME = 'Luke'
        LAST_NAME = 'Skywalker'
        EMAIL = names.get_last_name()+'luukeskywalker2@gmail.com'
        PASSWORD = 'LeiaOrgana123321'
        MALE = 0

        self.driver.get(self.url)

        sign_in_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.user-info > a'))
        )
        sign_in_link.click()

        create_account_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.no-account > a'))
        )
        create_account_link.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#customer-form'))
        )

        gender_radio_btn = self.driver.find_elements_by_css_selector('label.radio-inline')
        gender_radio_btn[MALE].click()

        name_field = self.driver.find_element_by_css_selector('#field-firstname')
        name_field.send_keys(FIRST_NAME)

        last_name_field = self.driver.find_element_by_css_selector('#field-lastname')
        last_name_field.send_keys(LAST_NAME)

        email_field = self.driver.find_element_by_css_selector('#field-email')
        email_field.send_keys(EMAIL)

        password_field = self.driver.find_element_by_css_selector('#field-password')
        password_field.send_keys(PASSWORD)

        customer_privacy_checkbox = self.driver.find_element_by_css_selector\
            ('.custom-checkbox > label > input[name=customer_privacy]')
        customer_privacy_checkbox.click()

        psgdpr_checkbox = self.driver.find_element_by_css_selector \
            ('.custom-checkbox > label > input[name=psgdpr]')
        psgdpr_checkbox.click()

        submit_btn = self.driver.find_element_by_css_selector\
            ('button.btn.btn-primary.form-control-submit.float-xs-right')
        submit_btn.click()

        personal_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.hidden-sm-down'))
        ).text



    def fill_order_form(self):
        cart_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.header > a'))
        )
        cart_link.click()

        order_form_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.text-sm-center > a'))
        )
        order_form_link.click()
        self.fill_address()
        self.choose_delivery_method()
        self.choose_payment_method()
        self.check_status()

    def fill_address(self):
        CITY = 'GDANSK'
        POSTAL_CODE = '80-223'
        ADDRESS = 'Gabriela Narutowicza 11/12'

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.js-address-form'))
        )

        addres_field = self.driver.find_element_by_css_selector('#field-address1')
        addres_field.send_keys(ADDRESS)

        postal_code_field = self.driver.find_element_by_css_selector('#field-postcode')
        postal_code_field.send_keys(POSTAL_CODE)

        city_field = self.driver.find_element_by_css_selector('#field-city')
        city_field.send_keys(CITY)

        continue_btn = self.driver.find_element_by_css_selector\
            ('.form-footer.clearfix > button[name=confirm-addresses]')
        continue_btn.click()

    def choose_delivery_method(self):
        delivery_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#delivery_option_2'))
        )
        delivery_option.click()

        subbmit_bttn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'confirmDeliveryOption'))
        )
        subbmit_bttn.click()

    def choose_payment_method(self):
        delivery_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#payment-option-2'))
        )
        delivery_option.click()
        self.driver.find_element_by_id('conditions_to_approve[terms-and-conditions]').click()

        subbmit_bttn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Złóż zamówienie')]"))
        )
        subbmit_bttn.click()

    def check_status(self):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Płatność przy odbiorze')]"))
            )
        except Exception:
            print("TEST FAILED")
        self.driver.get(self.url+'/index.php?controller=history')
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Przygotowanie w toku')]"))
            )
        except Exception:
            print("TEST FAILED")


if __name__ == "__main__":

    driver = webdriver.Chrome(PATH)
    driver.maximize_window()
    #driver.find_element_by_class_name()

    test = Test(driver, URL, PRODUCTS_NUM, FIRST_CATEGORY_PRODUCTS_NUM, FIRST_CATEGORY, SECOND_CATEGORY)
    test.test()