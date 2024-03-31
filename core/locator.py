from __future__ import annotations

import allure
from playwright.sync_api import Locator as PlaywrightLocator

from core.driver import Driver
from core.exceptions import CustomBrokenException

DEFAULT_TIMEOUT = 5_000  # ms


class Locator:
    """
    Present locators on pages
    """
    name: str = ""                   # overriden in class Block and __init__
    xpath: str = None
    block_xpath: str = ""           # overriden in class Block
    parent: PlaywrightLocator = None       # overriden in class Block
    webelement: PlaywrightLocator = None

    def __init__(self, name: str, xpath: str):
        self.xpath = xpath
        self.name = name
        # self.webelement = Driver().page.locator(self.block_xpath + self.xpath)

    def _use_current_page_context(self):
        # renew webelement with the page where it is used on
        if self.parent:
            self.webelement = self.parent.locator(self.block_xpath + self.xpath)
        else:
            self.webelement = Driver().page.locator(self.block_xpath + self.xpath)

    def click(self, wait_for_new_page: bool = False, wait_for_new_tab: bool = False):
        self._use_current_page_context()

        with allure.step(f'Click on {self.name}'):
            # record new opened tab into context
            if wait_for_new_tab:
                with Driver().browser.contexts[0].expect_page() as _:
                    self.webelement.first.click(timeout=DEFAULT_TIMEOUT)
                # update page context to new page
                Driver().switch_to_tab(-1)
            # navigate to another url on the same tab
            else:
                self.webelement.first.click(timeout=DEFAULT_TIMEOUT)

            # wait for new page to be loaded
            if wait_for_new_page:
                Driver().page.wait_for_load_state('domcontentloaded')

    def text(self) -> str:
        self._use_current_page_context()
        return "".join(self.webelement.first.all_text_contents())

    def is_on_page(self) -> bool:
        self._use_current_page_context()
        with allure.step(f'Check if element {self.name} is on page'):
            self.wait_for_displayed(timeout=DEFAULT_TIMEOUT)
            return self.webelement.first.is_visible()

    def get_attribute(self, attribute) -> str:
        self._use_current_page_context()
        return self.webelement.first.get_attribute(attribute, timeout=DEFAULT_TIMEOUT)

    def wait_for_displayed(self, timeout=DEFAULT_TIMEOUT):
        self._use_current_page_context()
        try:
            self.webelement.first.wait_for(timeout=timeout, state="visible")
        except:
            raise CustomBrokenException(f"Element {self.name} with xpath={self.block_xpath+self.xpath} is not visible")


class Input(Locator):
    def input(self, string: str):
        self._use_current_page_context()
        with allure.step(f'Input "{string}" into {self.name}'):
            self.webelement.first.fill(string, timeout=DEFAULT_TIMEOUT)

    def value(self) -> str:
        self._use_current_page_context()
        with allure.step(f'Get value from {self.name}'):
            return self.webelement.first.input_value(timeout=DEFAULT_TIMEOUT)
