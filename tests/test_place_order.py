from selenium.webdriver.common.by import By
import random

def test_place_order(browser):
    # Add item to cart
    product_id = random.randint(1,20)
    add_cart = browser.find_element(By.NAME, f"add_cart_{product_id}")
    add_cart.click()

    # View cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Proceed to checkout
    checkout = browser.find_element(By.ID, "checkout")
    checkout.click()

    # Submit Order details
    name = browser.find_element(By.NAME, "name")
    address = browser.find_element(By.NAME, "address")
    payment = browser.find_element(By.NAME, "payment")
    place_order = browser.find_element(By.NAME, "place_order")

    name.send_keys("Barbara Brooms")
    address.send_keys("4 Carver Road, Cranston, RI, 02920")
    payment.send_keys("debit")
    place_order.click()

    # Verify order placed.
    page_source = browser.page_source
    assert "Your order has been confirmed successfully." in page_source

    browser.get("http://127.0.0.1:5000/products")