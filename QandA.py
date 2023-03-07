import pandas
from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
url = "https://data.eastmoney.com/jgdy/xx.html"
stock_code = []
stock_name = []
date = []
content = []

edge_options = Options()
# 使用无头模式
edge_options.add_argument('--headless')
# 禁用GPU，防止无头模式出现莫名的BUG
edge_options.add_argument('--disable-gpu')
# Webdriver
service = Service('D:\edgedriver_win64\msedgedriver.exe')

# 访问网页
bro = webdriver.Edge(service = service)
bro.get(url)

sleep(7)
try:
    index = bro.find_element(By.XPATH, '//*[@id="gotopageindex"]')  
    index.send_keys(Keys.CONTROL, "a")
    index.send_keys('6001')
    next_page = bro.find_element(By.XPATH, '//*[@id="dataview"]/div[3]/div[2]/form/input[2]')  
    next_page.click()
except:
    # 如果找不到，print something
    print("Nothing found")
for page in range(6001, 6501):
    print(page)
    sleep(7)
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    for i in range(1, 51):
        label1 = '//*[@id="dataview"]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[2]/a/text()'
        label2 = '//*[@id="dataview"]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[3]/a/span/text()'  
        label3 = '//*[@id="dataview"]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[13]/text()'
        label4 = '//*[@id="dataview"]/div[2]/div[2]/table/tbody/tr['+str(i)+']/td[4]/a[1]/@href'
        temp1 = tree.xpath(label1)
        temp2 = tree.xpath(label2)
        temp3 = tree.xpath(label3)
        temp4 = tree.xpath(label4)
        temp_url = 'https://data.eastmoney.com'+temp4[0]
        stock_code.append(temp1[0])
        stock_name.append(temp2[0])
        date.append(temp3[0])
        content.append(temp_url)
    print(stock_code)
    print(stock_name)
    print(date)
    print(content)
    try:
        temp = bro.find_element(By.XPATH, '//*[@id="dataview"]/div[3]/div[1]/a[text()="下一页"]') 
        temp.click()
    except:
        print("find nothing")

df = pandas.DataFrame({'股票代码':stock_code, '股票简称':stock_name, '调研日期':date, '调研内容':content})
df.to_csv('data1.csv', mode='w', encoding='gb18030', errors='ignore')
bro.quit()
        
        
        
