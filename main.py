# Importa la la biblioteca Selenium para automatizar acciones en el navegador

import data
import time
import selector
from selenium import webdriver


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

# Aquí se definen los métodos y acciones que se realizan en la página
    # Incluye el método de inciialización
    # También incluyen pausas, para esperar que la página se cargue completamente antes de realizar otras acciones
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        time.sleep(1)
        self.driver.find_element(*self.selector.from_field).send_keys(from_address)

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
        time.sleep(1)
        self.driver.find_element(*self.select_comfort).click()

    def get_comfort_rate(self):
        return self.driver.find_element(*self.select_comfort).is_enabled()

    def set_phone_number(self, phone_number):
        time.sleep(1)
        self.driver.find_element(*self.phone_number_button).click()
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)
        time.sleep(1)
        self.driver.find_element(*self.phone_next_button).click()
        time.sleep(1)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property('value')

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

    def get_payment_method(self):
        return self.driver.find_element(*self.card_number_field).get_property('value')

    def get_cvv(self):
        return self.driver.find_element(*self.cvv_number_field).get_property('value')

    def credit_card_added_correctly(self):
        return self.driver.find_element(*self.card_added_checkmark).is_enabled()

    def message_field(self, driver_message):
        self.driver.find_element(*self.controller_message).send_keys(driver_message)
        time.sleep(1)

    def get_message(self):
        return self.driver.find_element(*self.controller_message).get_property('value')

    def blanket(self):
        self.driver.find_element(*self.order_a_blanket).click()
        time.sleep(1)

    def get_blanket_and_tissues(self):
        return self.driver.find_element(*self.order_a_blanket).is_enabled()

    def order_icrecream(self):
        self.driver.find_element(*self.icecream_counter).click()
        self.driver.find_element(*self.icecream_counter).click()
        time.sleep(1)

    def get_icream(self):
        return self.driver.find_element(*self.icecream_number).is_displayed()

    def order_a_taxi(self):
        self.driver.find_element(*self.order_taxi_button).click()
        time.sleep(45)

    def get_a_taxi(self):
        return self.driver.find_element(*self.order_taxi_button).is_enabled()

    def get_driver_modal(self):
        return self.driver.find_element(*self.driver_modal).is_displayed()


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
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.ask_for_a_taxi()
        routes_page.comfort_rate()
        assert routes_page.get_comfort_rate() == True

    def test_set_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

    def test_set_payment_method(self):
        routes_page = UrbanRoutesPage(self.driver)
        card_number = data.card_number
        cvv_number = data.card_code
        routes_page.obtain_code()
        routes_page.payment_method(card_number, cvv_number)
        assert routes_page.get_payment_method() == card_number
        assert routes_page.get_cvv() == cvv_number
        assert routes_page.credit_card_added_correctly() == True

    def test_message(self):
        routes_page = UrbanRoutesPage(self.driver)
        driver_message = data.message_for_driver
        routes_page.message_field(driver_message)
        assert routes_page.get_message() == driver_message

    def test_blancket_and_tissues(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.blanket()
        assert routes_page.get_blanket_and_tissues() == True

    def test_icecream(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_icrecream()
        assert routes_page.get_icream() == True

    def test_order_a_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.order_a_taxi()
        assert routes_page.get_a_taxi() == True

    def test_driver_modal(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.get_driver_modal()
        assert routes_page.get_driver_modal() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
