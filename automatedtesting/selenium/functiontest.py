from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://www.saucedemo.com/'

# Start the browser and login with standard_user
def login(user, password):
    print('Starting the browser...' + url)
    # options = ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome()
    print('Browser started successfully. Navigating to the demo page to login.')
    driver.get(url)
    
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'user-name'))
    )
    username_input.send_keys(user)
    
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'password'))
    )
    password_input.send_keys(password)
    
    login_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'login-button'))
    )
    login_button.click()
    
    print(f'User: {user}')
    return driver


# Add all items to the cart
def add_items_to_cart(driver):
    
    shop_items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'inventory_item'))
    )
    
    items_added = []
    
    # Click the "Add to Cart" button
    for item in shop_items:
        add_to_cart_button = item.find_element(By.CLASS_NAME, 'btn_inventory')
        item_name = item.find_element(By.CLASS_NAME, 'inventory_item_name').text
        add_to_cart_button.click()
        items_added.append(item_name)

    print('Items added to the cart:')
    for item in items_added:
        print(item)

    return items_added

# Remove all items from the cart
def remove_items_from_cart(driver):
    # Click the cart icon to navigate to the cart page
    cart_icon = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'shopping_cart_link'))
    )
    cart_icon.click()

    # Wait for the cart items to be visible
    cart_items = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CLASS_NAME, 'cart_item'))
    )
    
    items_removed = []
    
    # Click the "Remove" button for each item
    for item in cart_items:
        remove_button = item.find_element(By.CLASS_NAME, 'cart_button')
        item_name = item.find_element(By.CLASS_NAME, 'inventory_item_name').text
        remove_button.click()
        items_removed.append(item_name)
        
    print('Items removed from the cart:')
    for item in items_removed:
        print(item)
        
    return items_removed

# Close the browser
def close_browser(driver):
    driver.quit()

def main():
    user = 'standard_user'
    password = 'secret_sauce'

    driver = login(user, password)
    items_added = add_items_to_cart(driver)
    items_removed = remove_items_from_cart(driver)
    close_browser(driver)

main()
