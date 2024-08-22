import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_items():
    # Fetch items from the SQLite database
    conn = sqlite3.connect('grocery_items.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM groceries')
    items = cursor.fetchall()
    conn.close()
    return [item[0] for item in items]

def login_to_blinkit(driver):
    try:
        driver.get("https://blinkit.com/")
        
        # Find and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[3]/div[1]/div'))
        )
        login_button.click()
        
        # Enter the phone number or email
        phone_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/div/div/div/div/div/form/div/input'))
        )
        phone_input.send_keys("7379883995")
        
        # Click the button to receive the OTP
        send_otp_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/div/div/div/form/button'))
        )
        send_otp_button.click()
        
        # Wait for the user to input the OTP manually
        # otp = input("Enter the OTP received in your email: ")
        
        # Find the OTP input field and submit the OTP
        # otp_input = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter OTP']"))
        # )
        # otp_input.send_keys(otp)
        
        # Click the verify button to complete the login
        # verify_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Verify')]")
        # verify_button.click()
        
        time.sleep(20)
        print("Successfully logged in!")
        
    except Exception as e:
        print(f"An error occurred during login: {e}")

def add_to_cart(items):
    # Set up Selenium WebDriver
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get("https://blinkit.com/")

        location_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@class='btn location-box mask-button' and contains(text(), 'Detect my location')]"))
        )
        location_button.click()
        time.sleep(2)

        # login_to_blinkit(driver)
        time.sleep(2)

        search_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div[1]/header/div[2]/a/div[2]/div'))
        )
        search_button.click()
        
        for item in items:
            try:
                # Wait for the search box to appear and interact with it
                
                search_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@class='SearchBarContainer__Input-sc-hl8pft-3 irVxjq' and @placeholder='Search for atta dal and more']"))
                )
                search_box.clear()
                search_box.send_keys(item)
                search_box.send_keys(Keys.RETURN)
                
                # Define the XPath for the "Add to Cart" button
                add_button_xpath = "//div[@class='AddToCart__UpdatedButtonContainer-sc-17ig0e3-0 lmopxc' and text()='ADD']"
                
                '''add_to_cart_button = WebDriverWait(driver,  10).until(
                    EC.element_to_be_clickable((By.XPATH, add_button_xpath))
                )
                add_to_cart_button.click()'''
                # Scroll the page and look for the "Add to Cart" button
                for _ in range(10):  # Scroll up to 10 times (adjust as necessary)
                    try:
                        # Wait for the add button to be present
                        add_to_cart_button = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, add_button_xpath))
                        )
                        
                        # Scroll the page to the "Add to Cart" button
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_to_cart_button)
                        
                        # Wait until the button is clickable and click it
                        WebDriverWait(driver, 20).until(
                            EC.element_to_be_clickable((By.XPATH, add_button_xpath))
                        )
                        add_to_cart_button.click()
                        print(f"Added {item} to the cart.")
                        break  # Break the loop once the item is added

                    except Exception as e:
                        # Scroll down if the button wasn't found
                        driver.execute_script("window.scrollBy(0, 300);")
                        time.sleep(1)  # Give time for new elements to load '''

            except Exception as e:
                print(f"Could not add {item} to the cart. Error: {e}")
            
            # Pause between adding items
            time.sleep(2)
    
    finally:
        # Close the browser
        driver.quit()

# Fetch grocery items from the database
grocery_items = fetch_items()

# Add items to the cart
add_to_cart(grocery_items)
