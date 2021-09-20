from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from jsonParsing import jsonParsing

loginPage = "https://aule.univpm.it/agendastudenti/index.php?view=login&include=login&_lang=it"


class driver():
    def __init__(self):
        self.options = Options()
        self.options.add_argument("user-agent=S1099321_BookingBot")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=self.options)

def loadInfo():
    with open("info.json", "r") as f:
        j = json.load(f)
        f.close()
    return j

if __name__ == "__main__":
    info = loadInfo()
    d = driver()
    d.driver.get(loginPage)
    #LOGIN
    try:
        ID = "username"
        d.driver.find_element_by_id(ID).send_keys(info["Username"])
    except NoSuchElementException as e:
        print("ERROR: No element found with " + ID + "!\n " + str(e))
    try:
        ID = "password"
        d.driver.find_element_by_id(ID).send_keys(info["Password"])
    except NoSuchElementException as e:
        print("ERROR: No element found with " + ID + "!\n " + str(e))
    try:
        ID = "info_privacy"
        elem = d.driver.find_element_by_id(ID)
        # Click with JS
        d.driver.execute_script("arguments[0].click();", elem)
    except NoSuchElementException as e:
        print("ERROR: No element found with " + ID + "!\n " + str(e))
    try:
        ID = "info_easylesson"
        elem = d.driver.find_element_by_id(ID)
        # Click with JS
        d.driver.execute_script("arguments[0].click();", elem)
    except NoSuchElementException as e:
        print("ERROR: No element found with " + ID + "!\n " + str(e))
    
    # Submit Login Form
    d.driver.find_element_by_id("btn-login").click()

    # Navigate to booking
    d.driver.find_element_by_xpath("/html/body/div[4]/div[4]/div[3]/div/div[2]/div[1]/div/div[6]/div/div[2]/div[2]/ul/li[1]/a").click()

    # Get available lessons
    elem = d.driver.find_element_by_xpath("/html/body/div[4]/div[4]/script[3]")
    with open("lessons.json", "w") as f:
        html = elem.get_attribute("innerHTML")
        start = html.find("JSON.parse('")
        end = html.find("var empty_msg")
        f.write(html[start + 12:end - 8])
        f.close()

    j = jsonParsing()
    new_lectures = j.run()
    print(new_lectures)
    
    for l in new_lectures:
        x = d.driver.find_element_by_id(str(l))
        x.click()
        d.driver.execute_script("$.magnificPopup.close();")
    d.driver.close()