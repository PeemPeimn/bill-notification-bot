import os
import sys
import logging

from time import sleep
from dotenv import load_dotenv
from google_calendar import get_event_text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

logging.basicConfig(level=logging.INFO)
logging.info("Starting...")

load_dotenv(".env", override=True)

logging.info("Getting event from calendar")
text = get_event_text()

FACEBOOK_USERNAME = os.getenv("FACEBOOK_USERNAME")
FACEBOOK_PASSWORD = os.getenv("FACEBOOK_PASSWORD")
FACEBOOK_PIN = os.getenv("FACEBOOK_PIN")
FACEBOOK_CHAT_ID = os.getenv("FACEBOOK_CHAT_ID")

options = webdriver.ChromeOptions()
options.add_argument('--disable-popup-blocking')
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--remote-allow-origins=*")
options.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)
if len(sys.argv) > 1:
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

logging.info("Logging in to Facebook...")
driver.get('https://www.facebook.com/')
driver.find_element(By.ID, "email").send_keys(FACEBOOK_USERNAME)
driver.find_element(By.ID, 'pass').send_keys(FACEBOOK_PASSWORD)
driver.find_element(By.NAME, "login").click()

logging.info("Going to chat...")
chat_url = 'https://www.facebook.com/messages/t/' + FACEBOOK_CHAT_ID
driver.get(chat_url)
driver.get(chat_url)

logging.info("Trying to enter PIN...")

driver.find_element(
    By.XPATH, '//input[@autocomplete="one-time-code"]').send_keys(FACEBOOK_PIN)

logging.info("Finding text box...")
element = driver.find_element(By.XPATH, '//div[@aria-placeholder="Aa"]')
for part in text.split('\n'):
    element.send_keys(part)
    ActionChains(driver).key_down(Keys.SHIFT).key_down(
        Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
element.send_keys(Keys.ENTER)

logging.info("SUCCESS!!!!")
sleep(5)
