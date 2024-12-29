from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import json
import configparser

config = configparser.RawConfigParser()
config.read('config.cfg')

login_dict = dict(config.items('Login'))

# Your Instagram credentials
username = login_dict.get('email')
password = login_dict.get('password')

# Initialize Selenium WebDriver
driver = webdriver.Chrome()  # Adjust if necessary for your browser
driver.get("https://www.instagram.com/accounts/login/")

# Login to Instagram
time.sleep(3)  # Wait for the page to load
driver.find_element(By.NAME, "username").send_keys(username)
driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)

time.sleep(10)  # Wait for login to complete

# Function to unfollow a user
def unfollow_user(user):
    try:
        driver.get(f"https://www.instagram.com/{user}/")

        # Check if the account exists
        if "Sorry, this page isn't available." in driver.page_source:
            print(f"Account {user} no longer exists.")
            error_username.append([user, 'no longer exists'])
            return

        print(f"Preparing {user}.")
        # Check if the account is already unfollowed
        try:
            follow_button = WebDriverWait(driver,6).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))  # 'Follow' button
            if follow_button.text == 'Follow':
                print(f"Account {user} is already unfollowed." )
                error_username.append([user, 'already unfollowed'])
                return
            else:
                print(f"{user} is ready to unfollow.")
        except NoSuchElementException:
            error_username.append([user, 'user not found'])
            print(f"Error handling user {user}")
            pass

        # Attempt to click the 'Following' button
        try:
            following_button = WebDriverWait(driver,1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="button"]')))
            following_button.click()
            time.sleep(3)  # Wait for potential confirmation dialog

            # Check for confirmation dialog and click 'Unfollow' if present
            try:
                confirm_button = driver.find_element(By.XPATH, "//button[text()='Unfollow']")
                confirm_button.click()
                print(f"Confirmed and unfollowed {user}")
            except NoSuchElementException:
                print(f"Unfollowed {user} without confirmation")

        except NoSuchElementException:
            error_username.append([user,'button not found'])
            print(f"No 'Requested' button found for {user}, might not be following.")

    except Exception as e:
        error_username.append([user,'user not found'])
        print(f"Error handling user {user}: {e}")

# List of usernames (replace this with the list extracted from JSON)
usernames = []
error_username = []

# Load JSON data
file_dict = dict(config.items('File'))
file_path = file_dict.get('file_path')
with open(file_path, 'r') as file:
    data = json.load(file)

    # Extract usernames from JSON
    for entry in data['relationships_follow_requests_sent']:
        for item in entry['string_list_data']:
            usernames.append(item['value'])

#Loop through the usernames and unfollow
for user in usernames:
    unfollow_user(user)

# Close the browser
driver.quit()
