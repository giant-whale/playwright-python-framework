import allure
import pytest
from core.driver import Driver


def is_mobile(request) -> bool:
    markers = request.node.own_markers
    if [mark for mark in markers if mark.name.lower() == 'mobile']:
        return True
    else:
        return False


@pytest.fixture(autouse=True)
def driver(request):
    with allure.step('Driver setup'):
        mobile = is_mobile(request=request)
        webdriver = Driver(mobile=mobile)

    yield webdriver

    with allure.step('Driver teardown'):
        try:
            webdriver.quit()
        finally:
            webdriver.__class__._instances = {}
