from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


PATH = "C:\Program Files\chromedriver.exe"

driver = webdriver.Chrome(PATH)

driver.get("http://127.0.0.1:8000/register")

search = driver.find_element_by_name("email")
search.send_keys("PepsiMan@bepsi.com")

search = driver.find_element_by_name("username")
search.send_keys("CokeSucks")

search = driver.find_element_by_name("password1")
search.send_keys("Password123")

search = driver.find_element_by_name("password2")
search.send_keys("Password123")

bday = driver.find_element_by_name("birthday")
bday.clear()
bday.send_keys("04-04-1940")

checkbox = driver.find_element_by_name("accept_tos")
checkbox.click()
time.sleep(7)

submit_button = driver.find_element_by_id("subButton")
submit_button.click()


# submitForm = driver.find_element_by_("Submit")
# submitForm.click()


driver.quit()

