
import data
import UrbanRoutesPage
from selenium import webdriver
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
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.set_from(data.address_from)
        routes_page.set_to(data.address_to)
        assert routes_page.get_from() == data.address_from
        assert routes_page.get_to() == data.address_to

    def test_select_comfort(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.ask_for_a_taxi()
        routes_page.comfort_rate()
        assert routes_page.get_comfort_rate() == True

    def test_set_phone_number(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number

    def test_set_payment_method(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        card_number = data.card_number
        cvv_number = data.card_code
        routes_page.obtain_code()
        routes_page.payment_method(card_number, cvv_number)
        assert routes_page.get_payment_method() == card_number
        assert routes_page.get_cvv() == cvv_number
        assert routes_page.credit_card_added_correctly() == True

    def test_message(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        driver_message = data.message_for_driver
        routes_page.message_field(driver_message)
        assert routes_page.get_message() == driver_message

    def test_blancket_and_tissues(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.blanket()
        assert routes_page.get_blanket_and_tissues() == True

    def test_icecream(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.order_ice_cream()
        assert routes_page.get_ice_cream() == True

    def test_order_a_taxi(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.order_a_taxi()
        assert routes_page.get_a_taxi() == True

    def test_driver_modal(self):
        routes_page = UrbanRoutesPage.UrbanRoutesPage(self.driver)
        routes_page.get_driver_modal()
        assert routes_page.get_driver_modal() == True

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
