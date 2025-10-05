import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestData:
    def __init__(self, email, password, expected_url):
        self.url = 'http://127.0.0.1:5000'
        self.email = email
        self.password = password
        self.expected_url = expected_url


@pytest.fixture()
def test_data(request):
    test_data = TestData(request.param[0], request.param[1], request.param[2])
    return test_data


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome() 

    yield driver

    driver.quit()


@pytest.mark.parametrize('test_data', [
    ['test5@test.xyz', 'test5', 'http://127.0.0.1:5000/products'],
    ['invalid_user@test.xyz', 'invalid', 'http://127.0.0.1:5000/login']
    ], indirect=True)
def test_login(browser, test_data):
    browser.get(test_data.url)
    email = browser.find_element(By.ID, "email")
    password = browser.find_element(By.ID, "password")
    login_button = browser.find_element(By.ID, "submit")

    email.send_keys(test_data.email)
    password.send_keys(test_data.password)
    login_button.click()

    current_url = browser.current_url
    assert test_data.expected_url == current_url

    if 'products' in current_url:
        logout = browser.find_element(By.ID, "logout")
        logout.click()