from selenium import webdriver
from CloudcaptchaSolver import RecaptchaSolver
import time
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import cloudscraper

from requests_html import HTMLSession
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager

options = Options()

# Proxy details

# proxy_host = "res.proxy-seller.com"
# proxy_port = "10000"
# proxy_user = "5f88d977c59b8866"
# proxy_pass = "RNW78Fm5"

# Define custom options for the Selenium driver
# proxy_server_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
# print(proxy_server_url)
# options.add_argument(f'--proxy-server={proxy_server_url}')
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
# print(12345)
# Initialize the WebDriver options
# options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--no-proxy-server')
options.add_argument("--log-level=3")
options.add_argument("--incognito")

# options.add_argument("--headless")  # Run headlessly if needed
# options.add_argument("--disable-gpu")  # Disable GPU acceleration
# options.add_argument("start-maximized")
# options.add_argument("disable-infobars")
# options.add_argument("--disable-extensions")


options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(
    # service=ChromeService(ChromeDriverManager().install()),
    options=options
)

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)


try:
    # specify the target URL
    url = "https://opensea.io/rankings"

    # driver.get("https://www.google.com/recaptcha/api2/demo")
    # driver.get("https://www.zocdoc.com/")

    # recaptchaSolver = RecaptchaSolver(driver)
    response = scraper.get(url)

    # get the response status code
    print(f"The status code is {response.status_code}")

    # Perform CAPTCHA solving
    t0 = time.time()
    # driver.find_element(By.ID, "subACK").click()
    # driver.find_element(By.NAME, "submit").click()
    
    # recaptchaSolver.solveCaptcha()
    # time.sleep(random.uniform(100, 100))
    # driver.find_element(By.NAME, "patient-powered-search-input").send_keys('Dentist')
    # driver.find_element(By.NAME, "maxResult").clear()
    # driver.find_element(By.NAME, "maxResult").send_keys('100')
    # driver.find_element(By.CLASS_NAME, "sc-w1fnvw-5 SDjDR").click()
    print(f"Time to solve the captcha: {time.time() - t0:.2f} seconds")
    
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, 'emptable'))
    # )
    
    # driver.get("https://www.w3schools.com/html/html_tables.asp")
    # driver.get("https://www.wcb.ny.gov/icpocinq/icpocempsrch.jsp")
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    # table = soup.find("table",{"id":"emptable"}) # to select the right table
    
    # print("table")
    # print(table)
    # rows = table.find_all('tr')

    # # strip the header from rows
    # headers = rows[0]
    # header_text = []

    # # add the table header text to array
    # for th in headers.find_all('th'):
    #     header_text.append(th.text)

    # # init row text array
    # row_text_array = []

    # # loop through rows and add row text to array
    # for row in rows[1:]:
    #     row_text = []
    #     # loop through the elements
    #     for row_element in row.find_all(['th', 'td']):
    #         # append the array with the elements inner text
    #         row_text.append(row_element.text.replace('\n', '').strip())
    #     # append the text array to the row text array
    #     row_text_array.append(row_text)

    # with open("out.csv", "w") as f:
    #     wr = csv.writer(f)
    #     wr.writerow(header_text)
    #     for row_text_single in row_text_array:
    #         wr.writerow(row_text_single) 
        
except Exception as e:
    print(f"An error occurred: {e}")
    driver.quit()