
from selenium import webdriver

from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import pdfkit

url = input("Nhap url : ")
username = input("nhap tài khoản: ")
password = input("nhap pass: ")
replace_pass = {'!': '%21',
                '"': '%22',
                '#': '%23',
                '$': '%24',
                # '%': '%25',

                '&': "%26",
                "'": '%27',
                '(': '%28',
                ')': '%29',
                '*': '%2A',
                '+': '%2B',
                ',': '%2C',
                '-': '%2D',
                '.': '%2E',
                '/': '%2F',
                ':': '%3A',
                '<': '%3C',
                '=': '%3D',
                '>': '%3E',
                '?': '%3F',
                '@': '%40'}
for key, value in replace_pass.items():
    password = password.replace(key, value)

apiName = url.split('/#')
split_url = url.split('https://')
url_sub = "https://" + username + ":" + password + "@" + split_url[1]

url_sub2 = url_sub.split('/#')
edge_options = webdriver.ChromeOptions()
edge_options.add_argument("--headless")
driver = webdriver.Chrome(edge_options)
driver.get(url_sub)

timeout = 100
try:
    element_present = EC.presence_of_element_located((By.ID, apiName[1]))
    WebDriverWait(driver, timeout).until(element_present)
except TimeoutException:
    print("Timed out waiting for page to load")
finally:
    print("Page loaded")

html = driver.page_source

soup = bs(html, 'html.parser')
#
for a in soup.find_all('link'):
    a['href'] = a['href'].replace('assets', apiName[0] + '/assets')
for b in soup.find_all('link'):
    b['href'] = b['href'].replace('vendor', apiName[0] + '/vendor')
for c in soup.find_all('link'):
    c['href'] = c['href'].replace('css/', apiName[0] + '/css/')
for d in soup.find_all('link'):
    d['href'] = d['href'].replace('img/', apiName[0] + '/img/')


body = soup.find('div', {'id': apiName[1]})

head = soup.find('head')

result = str(head) + str(body)
print(url_sub)

with open(apiName[1] + ".html", "w", encoding="UTF-8") as f:
    f.write(result)
#
pdfkit.from_file(apiName[1] + ".html", apiName[1]+".pdf")


