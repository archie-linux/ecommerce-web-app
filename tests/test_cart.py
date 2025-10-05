from selenium.webdriver.common.by import By


def test_add_item_to_cart(browser, product):
    expected_product = product

    add_cart = browser.find_element(By.ID, f"add_cart_{expected_product['id']}")
    add_cart.click()

    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    page_source = browser.page_source
    product_quantity = browser.find_element(By.NAME, 'quantity')

    assert expected_product['title'] in page_source
    assert str(expected_product['price']) in page_source
    assert product_quantity.get_attribute('value') == '1'
