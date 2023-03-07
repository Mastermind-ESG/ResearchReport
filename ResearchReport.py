# -*- coding:utf-8 -*-
import pandas
from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'}
url = 'https://data.eastmoney.com/report/stock.jshtml'
stock_code = []
stock_name = []
pub_time = []
pub_title = []
pub_url = []

edge_options = Options()
edge_options.add_argument('--headless')
edge_options.add_argument('--disable-gpu')
service = Service('D:\edgedriver_win64\msedgedriver.exe')

bro = webdriver.Edge(options=edge_options, service=service)
bro.get(url)
page_text = bro.page_source
tree = etree.HTML(page_text)

for page in range(1, 1277):
    print(page)
    sleep(7)
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    tr_list = tree.xpath('//*[@id="stock_table"]/table/tbody/tr')

    for i in range(1, 51):
        label1 = '//*[@id="stock_table"]/table/tbody/tr[' + str(i) + ']/td[2]/a/text()'
        label2 = '//*[@id="stock_table"]/table/tbody/tr[' + str(i) + ']/td[3]/a/span/text()'
        label3 = '//*[@id="stock_table"]/table/tbody/tr[' + str(i) + ']/td[15]/text()'
        label4 = '//*[@id="stock_table"]/table/tbody/tr[' + str(i) + ']/td[5]/a/text()'
        label5 = '//*[@id="stock_table"]/table/tbody/tr[' + str(i) + ']/td[5]/a/@href'

        td1 = tr_list[i-1].xpath(label1)
        stock_code.append(td1[0])
        td2 = tr_list[i-1].xpath(label2)
        stock_name.append(td2[0])
        td3 = tr_list[i-1].xpath(label3)
        pub_time.append(td3[0])
        td4 = tr_list[i-1].xpath(label4)
        pub_title.append(td4[0])
        tmp = tr_list[i-1].xpath(label5)[0]
        td5 = 'https://pdf.dfcfw.com/pdf/H3_' + tmp[13:33] + '_1.pdf'
        pub_url.append(td5)

    print(stock_code)
    # print(stock_name)
    # print(pub_time)
    # print(pub_title)
    # print(pub_url)

    try:
        next_page = bro.find_element(By.XPATH, '//*[@id="stock_table_pager"]/div[1]/a[text()="下一页"]')
        next_page.click()
    except:
        print("Nothing found")

df = pandas.DataFrame({'股票代码': stock_code, '股票简称': stock_name, '报告时间': pub_time, '报告标题': pub_title, 'url': pub_url})
df.to_csv('data.csv', mode="w", encoding='gb18030', errors='ignore')

bro.quit()