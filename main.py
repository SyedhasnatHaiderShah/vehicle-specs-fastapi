import sys
import os
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--incognito")
chrome_options.add_argument('--disable-gpu') if os.name == 'nt' else None # Windows workaround
chrome_options.add_argument("--verbose")
chrome_options.add_argument('--headless')

import time ,requests
from selenium import webdriver
from fake_useragent import UserAgent

from fastapi import FastAPI

app = FastAPI()


@app.get("/{chassis}")
def root(chassis : str):
    Data = getData(chassis);
    return Data;

def getData(chassis):
    start_time = time.time()
    print(chassis)
    ua = UserAgent()
    userAgent = ua.random
    chrome_options.add_argument(f'user-agent={userAgent}')
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()) , options=chrome_options )

    #pip3 install 2captcha-python
    page_url = "https://www.vin-decoder.com/JTNBF4HK4K3038560"
    browser.get(page_url)
    site_key_element = browser.find_element(By.CSS_SELECTOR,'[data-sitekey]')
    print(site_key_element.get_attribute('data-sitekey'))
    site_key = site_key_element.get_attribute("data-sitekey")
    method = "userrecaptcha"
    key = "a5f0f37f5f053f2df94e9875a50b6801"
    print("solve")
    while 1:
        try:
            url = "http://2captcha.com/in.php?key={}&method={}&googlekey={}&pageurl={}".format(key,method,site_key,page_url)
            print(url)
            response = requests.get(url)
            break
        except:
            time.sleep(5)
    print("Done 1")
    if response.text[0:2] != 'OK':
        quit('Service error. Error code:' + response.text)
    captcha_id = response.text[3:]
    print(captcha_id)
    token_url = "http://2captcha.com/res.php?key={}&action=get&id={}".format(key,captcha_id)
    while True:
        time.sleep(2)
        response = requests.get(token_url)
        print(response)
        if response.text[0:2] == 'OK':
            break
    print('All Done')
    print("response :" , response.text);
    captha_results = response.text[3:]
    browser.execute_script("document.querySelector('#g-recaptcha-response').textContent='"+captha_results+"'")
    browser.find_element(By.ID,"searchbtn").click()
    time.sleep(5)
    Data = browser.find_element(By.XPATH,'/html/body/div[3]/div/div').text.split('\n')
    Car_Specs = {'VERSION':''}
    a = 0
    for i in range(int(len(Data)/2)):
        Car_Specs[Data[a]]=Data[a+1]
        a+=2
    print(Car_Specs)
    if(Car_Specs['VERSION'] == ''):
        Car_Specs['VERSION'] = Car_Specs['MODEL'].replace(")","").split("(")[-1]
    print(Car_Specs['VERSION'])

    return {"Data": Car_Specs , "Time_Taken" :(time.time() - start_time)}
