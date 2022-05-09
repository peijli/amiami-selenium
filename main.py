"""
Copyright (C) 2022 Gensoukyou Wolverines
----------------------------------------------
"And we shall FIGHT BACK!"

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# import directives
import sys
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def query_product(product: str, credentials: dict[str, str], driver_path: str):
    """
    Attempts to purchase a product with the ID specified as a string.
    Note all the timeouts are set to 60 seconds to account for lags in Amiami's servers.
    TODO: convert this into a class with individual functions!
    """

    # Initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    # Not specifying executable_path results in weird errors on Windows
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path=driver_path)

    # Open product listing page
    driver.get("https://www.amiami.com/eng/detail/?gcode=" + product)
    # The following code DOES NOT work in handling error pages
    # while len(driver.find_elements_by_class_name("item-detail__error")) != 0:
    #     driver.navigate.refresh()
    #     print("Refreshing webpage")
    filtered = []

    # There must be a more elegant way for this, but here's what's going on.
    # There is no single button element for adding an item to cart.
    # Instead, separate <span> and <button> elements are created for all possible states of this field,
    # all with the attribute 'class="btn-cart"'
    # However, only the element corresponding to the actual state of an item would be displayed
    # while all other elements are appended with the style attribute "display: none;"
    # We need to find the particular valid button where the 'style="display: none;"' and click on it
    # A further complication is that all those <span> and <button> elements will tend to be the last elements
    # on a product's catalog page that gets updated upon a GET request.
    # So multiple find_element and filter calls may be needed to locate a valid button.
    while len(filtered) == 0:
        driver.implicitly_wait(60)
        # print("Page opened")
        elem_list = driver.find_elements_by_class_name("btn-cart")
        filtered = list(filter(lambda element: element.get_attribute("style") == "", elem_list))
    # print(filtered[0].text)
    filtered[0].click()

    # Advance through cart page
    cart = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "cart")))
    cart.submit()

    # log in with provided credentials
    email_field = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys(credentials["email"])
    driver.find_element_by_name("password").send_keys(credentials["password"])
    driver.find_element_by_class_name("btn-submit").click()

    # 1. Rearrangement Options
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "flow-list")))
    elem_list = driver.find_elements_by_class_name("btn-submit")
    elem_list[0].click()

    # 2. Payment & shipping
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.ID, 'shipping-method1')))
    driver.execute_script("document.getElementById('shipping-method19').click()")
    driver.find_element_by_class_name("btn-submit").click()

    # 3. Review
    WebDriverWait(driver, 60).until(
        EC.text_to_be_present_in_element((By.CLASS_NAME, 'section-title'), "Confirm your order"))
    confirm = driver.find_element_by_class_name("btn-submit")
    # print(confirm.text)
    if sys.argv[1] == "action":
        confirm.click()  # only confirm the order during real, operational runs of the bot


if __name__ == '__main__':

    print("""
    Copyright (C) 2022 Gensoukyou Wolverines 
    This program comes with ABSOLUTELY NO WARRANTY; 
    This is free software, and you are welcome to redistribute it
    under certain conditions
    """)

    # Set default argument
    if len(sys.argv) < 2:
        sys.argv.extend("test")

    # Identify appropriate configuration file to read
    config_fn = ""
    if sys.argv[1] == "action":
        config_fn = "config_private.json"
    else:  # for testing purposes
        config_fn = "config.json"

    with open(config_fn) as file_config:
        # Read from configuration files
        config = json.load(file_config)
        credentials = config['credentials']
        driver_path = config['driverPath']
        if sys.argv[1] == "action":
            products = config["actionItems"]
        else:  # testing
            products = config["testItems"]

        for product in products:
            query_product(product, credentials, driver_path)

        print("Operations completed")
