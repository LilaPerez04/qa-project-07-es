import time
import selector
import utils


class UrbanRoutesPage:
    # Aquí se definen los métodos y acciones que se realizan en la página
    # Incluye el método de inicialización
    # También incluyen pausas, para esperar que la página se cargue completamente antes de realizar otras acciones

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        time.sleep(1)
        self.driver.find_element(selector.from_field[0], selector.from_field[1]).send_keys(from_address)

    def set_to(self, to_address):
        time.sleep(1)
        self.driver.find_element(selector.to_field[0], selector.to_field[1]).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(selector.from_field[0], selector.from_field[1]).get_property('value')

    def get_to(self):
        return self.driver.find_element(selector.to_field[0], selector.to_field[1]).get_property('value')

    def ask_for_a_taxi(self):
        time.sleep(1)
        self.driver.find_element(selector.taxi_button[0], selector.taxi_button[1]).click()

    def comfort_rate(self):
        time.sleep(1)
        self.driver.find_element(selector.select_comfort[0], selector.select_comfort[1]).click()

    def get_comfort_rate(self):
        return self.driver.find_element(selector.select_comfort[0], selector.select_comfort[1]).is_enabled()

    def set_phone_number(self, phone_number):
        time.sleep(1)
        self.driver.find_element(selector.phone_number_button[0], selector.phone_number_button[1]).click()
        self.driver.find_element(selector.phone_number_field[0], selector.phone_number_field[1]).send_keys(phone_number)
        time.sleep(1)
        self.driver.find_element(selector.phone_next_button[0], selector.phone_next_button[1]).click()
        time.sleep(1)

    def get_phone_number(self):
        return self.driver.find_element(selector.phone_number_field[0], selector.phone_number_field[1]).get_property('value')

    def obtain_code(self):
        number_code = utils.retrieve_phone_code(driver=self.driver)
        time.sleep(1)
        self.driver.find_element(selector.confirmation_code[0], selector.confirmation_code[1]).send_keys(number_code)
        time.sleep(1)
        self.driver.find_element(selector.confirmation_button[0], selector.confirmation_button[1]).click()
        time.sleep(1)

    def payment_method(self, card_number, cvv_number):
        self.driver.find_element(selector.add_payment_method[0], selector.add_payment_method[1]).click()
        self.driver.find_element(selector.add_card[0], selector.add_card[1]).click()
        time.sleep(1)
        self.driver.find_element(selector.card_number_field[0], selector.card_number_field[1]).send_keys(card_number)
        time.sleep(1)
        self.driver.find_element(selector.cvv_number_field[0], selector.cvv_number_field[1]).send_keys(cvv_number)
        time.sleep(1)
        self.driver.find_element(selector.unfocus_element[0], selector.unfocus_element[1]).click()
        time.sleep(1)
        self.driver.find_element(selector.link_button[0], selector.link_button[1]).click()
        self.driver.find_element(selector.payment_close_button[0], selector.payment_close_button[1]).click()
        time.sleep(1)

    def get_payment_method(self):
        return self.driver.find_element(selector.card_number_field[0], selector.card_number_field[1]).get_property('value')

    def get_cvv(self):
        return self.driver.find_element(selector.cvv_number_field[0], selector.cvv_number_field[1]).get_property('value')

    def credit_card_added_correctly(self):
        return self.driver.find_element(selector.card_added_checkmark[0], selector.card_added_checkmark[1]).is_enabled()

    def message_field(self, driver_message):
        self.driver.find_element(selector.controller_message[0], selector.controller_message[1]).send_keys(driver_message)
        time.sleep(1)

    def get_message(self):
        return self.driver.find_element(selector.controller_message[0], selector.controller_message[1]).get_property('value')

    def blanket(self):
        self.driver.find_element(selector.order_a_blanket[0], selector.order_a_blanket[1]).click()
        time.sleep(1)

    def get_blanket_and_tissues(self):
        return self.driver.find_element(selector.order_a_blanket[0], selector.order_a_blanket[1]).is_enabled()

    def order_ice_cream(self):
        self.driver.find_element(selector.icecream_counter[0], selector.icecream_counter[1]).click()
        self.driver.find_element(selector.icecream_counter[0], selector.icecream_counter[1]).click()
        time.sleep(1)

    def get_ice_cream(self):
        return self.driver.find_element(selector.icecream_number[0], selector.icecream_number[1]).is_displayed()

    def order_a_taxi(self):
        self.driver.find_element(selector.order_taxi_button[0], selector.order_taxi_button[1]).click()
        time.sleep(45)

    def get_a_taxi(self):
        return self.driver.find_element(selector.order_taxi_button[0], selector.order_taxi_button[1]).is_enabled()

    def get_driver_modal(self):
        return self.driver.find_element(selector.driver_modal[0], selector.driver_modal[1]).is_displayed()
