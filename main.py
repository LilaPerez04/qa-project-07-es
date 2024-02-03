# Importa la la biblioteca Selenium para automatizar acciones en el navegador

import data
import time
from selenium import webdriver
# from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait


# No modificar - Devuelve el código para confirmar el teléfono
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado /"
                            " el código en tu aplicación.")
        return code


# Esta parte del código define los localizadores para identificar los elementos de la página
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    taxi_button = (By.CSS_SELECTOR, 'button.button.round')
    select_comfort = (By.XPATH, '//div[@class="tcard-title" and text()="Comfort"]')
    phone_number_button = (By.CLASS_NAME, 'np-text')
    phone_number_field = (By.ID, 'phone')
    phone_next_button = (By.XPATH, '//div[@class="modal"]//button[@class="button full"]')
    confirmation_code = (By.ID, 'code')
    confirmation_button = (By.XPATH, '(//div[@class="modal"]//div[@class="section active"]//button[@class="button full"])[1]')
    add_payment_method = (By.CLASS_NAME, 'pp-text')
    add_card = (By.XPATH, '(//div[@class="pp-title"])[2]')
    card_number_field = (By.ID, 'number')
    cvv_number_field = (By.XPATH, '//input[@name="code"]')
    unfocus_element = (By.CLASS_NAME, 'plc')
    link_button = (By.XPATH, '(//div[@class="pp-buttons"]//button[@class="button full"])[1]')
    payment_close_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    controller_message = (By.ID, 'comment')
    order_a_blanket = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    icecream_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

# Aquí se definen los métodos y acciones que se realizan en la página
    # Incluye el método de inciialización
    # También incluyen pausas, para esperar que la página se cargue completamente antes de realizar otras acciones
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        time.sleep(1)
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        time.sleep(1)
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def ask_for_a_taxi(self):
        time.sleep(1)
        self.driver.find_element(*self.taxi_button).click()

    def comfort_rate(self):
        time.sleep(2)
        self.driver.find_element(*self.select_comfort).click()

    def set_phone_number(self, phone_number):
        time.sleep(1)
        self.driver.find_element(*self.phone_number_button).click()
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)
        time.sleep(1)
        self.driver.find_element(*self.phone_next_button).click()
        time.sleep(1)

    def obtain_code(self):
        number_code = retrieve_phone_code(driver=self.driver)
        time.sleep(1)
        self.driver.find_element(*self.confirmation_code).send_keys(number_code)
        time.sleep(1)
        self.driver.find_element(*self.confirmation_button).click()
        time.sleep(1)

    def payment_method(self, card_number, cvv_number):
        self.driver.find_element(*self.add_payment_method).click()
        self.driver.find_element(*self.add_card).click()
        time.sleep(1)
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        time.sleep(1)
        self.driver.find_element(*self.cvv_number_field).send_keys(cvv_number)
        time.sleep(1)
        self.driver.find_element(*self.unfocus_element).click()
        time.sleep(1)
        self.driver.find_element(*self.link_button).click()
        self.driver.find_element(*self.payment_close_button).click()
        time.sleep(1)

    def message_field(self, driver_message):
        self.driver.find_element(*self.controller_message).send_keys(driver_message)
        time.sleep(1)

    def blanket(self):
        self.driver.find_element(*self.order_a_blanket).click()
        time.sleep(1)

    def order_icrecream(self):
        self.driver.find_element(*self.icecream_counter).click()
        self.driver.find_element(*self.icecream_counter).click()
        time.sleep(1)

    def order_a_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()
        time.sleep(45)


# Aquí están las variables y métodos de clase
    # Incluye la asignación de las variables del documento data.py, la llamada a los métodos
    # Y algunas pruebas assert
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado /
        # para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        #        cls.driver = webdriver.Chrome(desired_capabilities=capabilities)
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        phone_number = data.phone_number
        card_number = data.card_number
        cvv_number = data.card_code
        driver_message = data.message_for_driver
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        routes_page.ask_for_a_taxi()
        routes_page.comfort_rate()
        routes_page.set_phone_number(phone_number)
        routes_page.obtain_code()
        routes_page.payment_method(card_number, cvv_number)
        routes_page.message_field(driver_message)
        routes_page.blanket()
        routes_page.order_icrecream()
        routes_page.order_a_taxi()
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
