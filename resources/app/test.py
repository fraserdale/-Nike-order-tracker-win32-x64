from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


##############################################
orders = []
emails = []
locale = "gb"
##############################################

locale = open(dir_path + "/locale.txt","r").read()

open(dir_path + "/output.txt","w").write("")
shit = open(dir_path + "/input.txt","r").read().replace("\n",":").split(":")

for x in range(0, int(len(shit)),2):
    orders.append(shit[x])
    emails.append(shit[x+1])

if locale.lower() == "gb":
    url = "https://secure-store.nike.com/gb/en_gb/orders/?loginForm&orderId="
elif locale.lower() == "us":
    url = "https://secure-store.nike.com/us/en_us/orders/?loginForm&orderId="
else:
    print("region not correct. try again")
    quit()

for i in range (int(len(orders))):
    orderNo = orders[i]
    email = emails[i]

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url + orderNo)
    time.sleep(2)
    driver.find_element_by_id('guestsEmail').send_keys(email)
    buttons = driver.find_elements_by_xpath("//*[contains(text(), 'Submit')]")
    for btn in buttons:
        btn.click()

    try:
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "status")))
        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        time.sleep(1)
        status = soup.find_all("div", class_="status")[0].text
        status = status.strip('\n')
        if status == "PREPARING TO SHIP":
            edd = (((soup.find_all("div", class_="edd")[0]).text).strip())[-10:]
            open(dir_path + "/output.txt","a").write("Order: " + orderNo + " | Status: " + status + " : Estimated Delivery: " + edd + "\n")
            print("writing")
        else:
            open(dir_path + "/output.txt","a").write("Order: " + orderNo + " | Status: " + status + "\n")
            print("writing")
    except TimeoutException:
        open(dir_path + "/output.txt","a").write("Not able to login, wrong email + orderID or wrong region. us or gb only")


