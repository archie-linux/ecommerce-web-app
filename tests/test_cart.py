from selenium.webdriver.common.by import By
import json
import random

product_url = "http://127.0.0.1:5000/products"

def get_expected_product(product_id=random.randint(1,20)):
    expected_product = None
    product_id = product_id
    with open('./tests/test_data.json') as file:
        # Load the JSON data
        products = json.load(file)
        for product in products:
            if product['id'] == product_id:
                expected_product = product
                expected_product['id'] = str(expected_product['id'])

    return expected_product

def validate_cart_items(browser, expected_cart_items):
    page_source = browser.page_source

    for cart_item in expected_cart_items:
        assert cart_item['title'] in page_source.replace('&amp;', '&')
        assert str(cart_item['price']) in page_source

def delete_cart_item(browser, products):
    for product in products:
        item_quantity = browser.find_element(By.NAME, f"quantity_{product['id']}")
        browser.execute_script("arguments[0].value = '';", item_quantity)
        browser.execute_script("arguments[0].value = arguments[1];", item_quantity, '0')
        update_cart = browser.find_element(By.NAME, f"update_cart_{product['id']}")
        update_cart.click()

def test_add_item_to_cart(browser):
    # Add item to cart
    expected_product = get_expected_product()
    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product['id']}")
    add_cart.click()

    # View cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Verify cart item is added
    page_source = browser.page_source
    product_quantity = browser.find_element(By.NAME, f"quantity_{expected_product['id']}")

    assert expected_product['title'] in page_source
    assert str(expected_product['price']) in page_source
    assert product_quantity.get_attribute('value') == '1'

    # Clean up
    delete_cart_item(browser, [expected_product])

    browser.get(product_url)

def test_add_multiple_items_to_cart(browser):
    # Add Item to cart
    expected_product_1 = get_expected_product(random.randint(1,20))
    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product_1['id']}")
    add_cart.click()

    # View Cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Validate added cart item
    validate_cart_items(browser, expected_cart_items=[expected_product_1])

    # Continue shopping
    continue_shopping = browser.find_element(By.ID, "continue_shopping")
    continue_shopping.click()

    # Add another item to cart
    expected_product_2 = get_expected_product(random.randint(1,20))
    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product_2['id']}")
    add_cart.click()

    # View Cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Validate cart items are updated
    validate_cart_items(browser, expected_cart_items=[expected_product_1, expected_product_2])

    # Clean up
    delete_cart_item(browser, [expected_product_1, expected_product_2])

    browser.get(product_url)

def test_update_cart_item(browser):
    # Add item to cart
    expected_product = get_expected_product()
    expected_quantity = random.randint(1,5)

    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product['id']}")
    browser.execute_script("arguments[0].value = '';", item_quantity)
    browser.execute_script("arguments[0].value = arguments[1];", item_quantity, expected_quantity)

    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product['id']}")
    add_cart.click()

    # View cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    page_source = browser.page_source

    # Verify Item quantity.
    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product['id']}")
    assert item_quantity.get_attribute('value') == str(expected_quantity) # quantity input box
    assert str(expected_quantity) in page_source # quantity text

    # Update item quantity
    expected_quantity = random.randint(6,9)
    browser.execute_script("arguments[0].value = '';", item_quantity)
    browser.execute_script("arguments[0].value = arguments[1];", item_quantity, expected_quantity)
    update_cart = browser.find_element(By.NAME, f"update_cart_{expected_product['id']}")
    update_cart.click()

    page_source = browser.page_source

    # Verify updated quantity
    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product['id']}")
    assert item_quantity.get_attribute('value') == str(expected_quantity) # quantity input box
    assert str(expected_quantity) in page_source # quantity text

    # Clean up
    delete_cart_item(browser, [expected_product])

    browser.get(product_url)

def test_delete_cart_item(browser):
    expected_product = get_expected_product()
    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product['id']}")
    add_cart.click()

    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Delete cart item by setting item quantity to 0
    delete_cart_item(browser, [expected_product])

    # Verify item removed from
    page_source = browser.page_source
    assert 'Your cart is empty.' in page_source

    browser.get(product_url)

def test_cart_checkout(browser):
    # Add Item to cart
    expected_product_1 = get_expected_product(random.randint(1,20))
    expected_quantity_1 = random.randint(1,5)

    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product_1['id']}")
    browser.execute_script("arguments[0].value = '';", item_quantity)
    browser.execute_script("arguments[0].value = arguments[1];", item_quantity, expected_quantity_1)

    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product_1['id']}")
    add_cart.click()

    # Add another item to cart
    expected_product_2 = get_expected_product(random.randint(1,20))
    expected_quantity_2 = random.randint(1,5)

    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product_2['id']}")
    browser.execute_script("arguments[0].value = '';", item_quantity)
    browser.execute_script("arguments[0].value = arguments[1];", item_quantity, expected_quantity_2)

    add_cart = browser.find_element(By.NAME, f"add_cart_{expected_product_2['id']}")
    add_cart.click()

    # View Cart
    view_cart = browser.find_element(By.NAME, "view_cart")
    view_cart.click()

    # Validate cart items are updated
    validate_cart_items(browser, expected_cart_items=[expected_product_1, expected_product_2])

    # Proceed to checkout
    checkout = browser.find_element(By.ID, "checkout")
    checkout.click()

    # Verify total amount
    expected_total_amount = expected_product_1['price'] * expected_quantity_1 + expected_product_2['price'] * expected_quantity_2
    page_source = browser.page_source
    assert str(round(expected_total_amount, 2)) in page_source

    # Navigate to view cart page
    browser.get('http://127.0.0.1:5000/view-cart')

    # Update cart items quantity
    expected_quantity_2 = random.randint(6,9)
    item_quantity = browser.find_element(By.NAME, f"quantity_{expected_product_2['id']}")
    browser.execute_script("arguments[0].value = '';", item_quantity)
    browser.execute_script("arguments[0].value = arguments[1];", item_quantity, expected_quantity_2)
    update_cart = browser.find_element(By.NAME, f"update_cart_{expected_product_2['id']}")
    update_cart.click()

    # Proceed to checkout again
    checkout = browser.find_element(By.ID, "checkout")
    checkout.click()

    # Verify total amount is updated accordingly
    expected_total_amount = expected_product_1['price'] * expected_quantity_1 + expected_product_2['price'] * (expected_quantity_2)
    page_source = browser.page_source
    assert str(round(expected_total_amount, 2)) in page_source

    # Clean up
    browser.get('http://127.0.0.1:5000/view-cart')
    delete_cart_item(browser, [expected_product_1, expected_product_2])

    browser.get(product_url)