import allure

from core.locator import Locator
from core.page import Page


class YahooMainPageMobile(Page):
    BASE_PAGE_URL = "https://www.yahoo.com/"

    menu_button = Locator('Menu Button', '//*[@id="_yb_sidenav-btn"]')
    menu_popup = Locator('Menu Popup', '//*[@id="_yb_sidenav-btn"]/../div/div')

    @staticmethod
    def is_menu_displayed():
        # page adds "style="display: flex" attribute, this is the only way to check if menu is displayed
        with allure.step('Check if menu is opened'):
            opened_menu_class = 'display: flex'
            attributes = YahooMainPageMobile.menu_popup.get_attribute("style")
            if opened_menu_class in attributes:
                return True
            else:
                return False
