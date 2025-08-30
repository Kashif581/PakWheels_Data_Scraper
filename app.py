# import dependencies
from selenium import webdriver # controls a browser (like Chrome, firefox, etc)
from selenium.webdriver.chrome.service import Service # ChromeDriver executable service used to run Chrome
from selenium.webdriver.chrome.options import Options # configure browser settings (e.g, headless mode, disable popups)
from selenium.webdriver.common.by import By # way to locate element
from selenium.webdriver.common.action_chains import ActionChains # simulate complex user actions(hover, drag & drop, key presses)
from selenium.webdriver.support.ui import WebDriverWait # wait dynamically for elements/conditions before interacting (avoid error)
from scraper import CarScraper
from sheets import GoogleSheetSaver
import time
from selenium.webdriver.support import expected_conditions as EC # Define conditions (e.g, 'element is clickable') to use with WebdriverWait
import os
import json




# path to chromedriver
driver_path = r"/usr/bin/chromedriver"
url = "https://www.pakwheels.com/"

options = Options()
# ignore errors
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")
options.add_argument("--ignore-start-errors")
options.add_argument("--start-maximized") # start with full screen
# prefs = {
#     "profile.default_content_setting_values.notifications": 2  # 1=Allow, 2=Block
# }
# options.add_experimental_option("prefs", prefs)




service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)



driver.get(url)

# Step 1: Hover over the parent dropdown to make submenu visible
used_cars_menu = driver.find_element(By.XPATH, "//li[@class='dropdown']/a[@title='Used Cars for sale in Pakistan']")
ActionChains(driver).move_to_element(used_cars_menu).perform()

# Step 2: Wait until the "Used Cars Search" link appears
used_cars_search = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//a[@title='Used Cars Search']"))
)

# Step 3: Click the link
used_cars_search.click()

# wait until car names are visible on the new page 
WebDriverWait(driver, 15).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, 'car-name'))
)


# ---------------------------------------Scrap the data---------------------------------------------


scraper = CarScraper(driver)

    
cars = scraper.get_cars_names()
prices = scraper.get_car_prices()
cities = scraper.get_car_cities()
specs = scraper.get_vehicle_specs()


# Get credentials from GitHub Secrets
creds_json = os.getenv("GOOGLE_SHEETS_CREDENTIALS") 

if creds_json is None:
    raise ValueError("Missing GOOGLE_SHEETS_CREDENTIALS env var")

# Parse JSON string into dict
creds_dict = json.loads(creds_json)

# Pass credentials dict to GoogleSheetSaver
sheet = GoogleSheetSaver(creds_dict, "PakWheelsCarData")
sheet.save_cars(cars, cities, prices, specs)


# print("Cars:", cars)
# print("Prices:", prices)
# print("Cities:", cities)
# print("Specs:", specs)


driver.quit()



















# ----------------------------------------------------------------------------------------------------


# cars_list = driver.find_elements(By.CLASS_NAME, 'car-name')
# print(len(cars_list))
# for car_name in cars_list:
#     print(car_name.text)

# price_details = driver.find_elements(By.CLASS_NAME, 'price-details')
# print(len(price_details))
# for price in price_details:
#     print(price.text)


# cities = driver.find_elements(By.CLASS_NAME, 'search-vehicle-info')
# for city in cities:
#     print(city.text)


# details = driver.find_elements(By.CLASS_NAME, 'search-vehicle-info-2')
# for detail in details:
#     print(detail.text)





# print(test)


