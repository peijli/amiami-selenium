import sys
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def query_product(product: str, credentials: dict[str, str]):
    # Initialize driver
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(chrome_options=options,
                              executable_path="C:/chromedriver_win32/chromedriver.exe")

    # Open product listing page
    driver.get("https://www.amiami.com/eng/detail/?gcode=" + product)
    # while len(driver.find_elements_by_class_name("item-detail__error")) != 0:
    #     driver.navigate.refresh()
    #     print("Refreshing webpage")
    filtered = []
    while len(filtered) == 0:  # multiple queries may be needed
        driver.implicitly_wait(60)
        print("Page opened")
        elem_list = driver.find_elements_by_class_name("btn-cart")
        filtered = list(filter(lambda element: element.get_attribute("style") == "", elem_list))
    print(filtered[0].text)
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
    # explicit wait
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
    print(confirm.text)

    if sys.argv[1] == "action":
        confirm.click()


if __name__ == '__main__':

    if len(sys.argv) < 2:
        sys.argv.extend("test")

    # Use for private testing
    # if (sys.argv[1])

    with open("config.json") as file_config:
        config = json.load(file_config)
        credentials = config['credentials']
        if sys.argv[1] == "action":
            products = config["actionItems"]
        else:  # testing
            products = config["testItems"]

        for product in products:
            query_product(product, credentials)

        print("Operations completed")
