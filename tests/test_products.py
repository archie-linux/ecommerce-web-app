from selenium.webdriver.common.by import By
import requests
import random


def search_text(browser, search_text):
    search_input = browser.find_element(By.NAME, "query")
    search_button = browser.find_element(By.ID, "search")
    search_input.send_keys(search_text)
    search_button.click()


def validate_products(browser, expected_products):
    page_source = browser.page_source

    for product in expected_products:
        image_alt = product['title']
        image_xpath = f"//img[@alt=\"{image_alt}\"]"
        product_image = browser.find_element(By.XPATH, image_xpath)
        image_src = product_image.get_attribute('src')
        assert product['image'] == image_src
        assert product['title'] in page_source.replace('&amp;', '&')
        assert product['description'] in page_source.replace('&amp;', '&')
        assert str(product['price']) in page_source


def test_product_filter_by_categories(browser):
    categories = ["men's clothing", "jewelery", "electronics", "women's clothing"]
    category_name = random.choice(categories)
    categories = requests.get(f"https://fakestoreapi.com/products/category/{category_name}").json()
    expected_products = [products for products in categories]

    # filter by product category
    category = browser.find_element(By.NAME, category_name)
    category.click()

    validate_products(browser, expected_products)

def test_valid_search(browser):
    product_data = requests.get("https://fakestoreapi.com/products").json()
    product_name = "Cotton"
    expected_products = [product for product in product_data 
                        if product_name.lower() in product['title'].lower()]

    # search product
    search_text(browser, product_name)
    validate_products(browser, expected_products)


def test_invalid_search(browser):
    product_name = "shoes"
    search_text(browser, product_name)
    page_source = browser.page_source
    assert 'Product not found' in page_source
