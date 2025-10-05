import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def browser():
    driver = webdriver.Chrome() 

    driver.get("http://127.0.0.1:5000")
    email = driver.find_element(By.ID, "email")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "submit")

    email.send_keys("test5@test.xyz")
    password.send_keys("test5")
    login_button.click()

    yield driver

    driver.quit()