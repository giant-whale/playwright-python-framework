from playwright.sync_api import sync_playwright, Playwright


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Driver(metaclass=Singleton):

    def __init__(self, *args, **kwargs):
        self._playwright = sync_playwright().start()
        if kwargs.get("mobile"):
            self.browser = self._playwright.webkit.launch()
            parameters = self._playwright.devices["iPhone 14"]
        else:
            self.browser = self._playwright.chromium.launch()
            parameters = self._playwright.devices["Desktop Chrome"]
            parameters["viewport"] = {"width": 1920, "height": 1080}

        self.page = self.browser.new_page(**parameters)

    def quit(self):
        self.browser.close()
        self._playwright.stop()

    def switch_to_tab(self, tab_index: int):
        self.page = self.browser.contexts[0].pages[tab_index]
