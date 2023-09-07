
from selenium import webdriver

from bs4 import BeautifulSoup as bs
import pdfkit


url = input("Nhap url : ")
username = input("nhap tài khoản: ")
# password = input("nhap pass: ")
apiName = url.split('/#')
split_url = url.split('https://')
password = "mobio%21%40%23456"
url_sub = "https://" + username + ":" + password + "@" + split_url[1]

edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--headless")
driver = webdriver.Edge(edge_options)
driver.get(url_sub)

driver.implicitly_wait(100)


html = driver.page_source

soup = bs(html, 'html.parser')
#
for a in soup.find_all('link'):
    a['href'] = a['href'].replace('assets', apiName[0] + '/assets')
for b in soup.find_all('link'):
    b['href'] = b['href'].replace('vendor', apiName[0] + '/vendor')

body = soup.find('div', {'id': apiName[1]})

head = soup.find('head')

result = str(head) + str(body)
# print(result)
with open(apiName[1]+".html", "w", encoding="UTF-8") as f:
    f.write(result)
#
pdfkit.from_file("api-Comment-UpdateComment.html", "output2.pdf")
