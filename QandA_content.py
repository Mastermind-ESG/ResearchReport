import pandas
from lxml import etree
from time import sleep
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

edge_options = Options()
# 使用无头模式
edge_options.add_argument('--headless')
# 禁用GPU，防止无头模式出现莫名的BUG
edge_options.add_argument('--disable-gpu')
# Webdriver
service = Service('D:\edgedriver_win64\msedgedriver.exe')
# 访问网页
bro = webdriver.Edge(service = service)

content = []
links = pandas.read_csv("data1.csv", encoding='gb18030')['调研内容']
for url in links:
    bro.get(url)
    sleep(4)
    page_text = bro.page_source
    tree = etree.HTML(page_text)
    label = '//*[@id="main_content"]/text()'
    temp = tree.xpath(label)
    con_str = ' '.join(temp)
    content.append(con_str)
    print('ok')

df = pandas.DataFrame({'调研内容':content})
df.to_csv('content.csv', encoding='gb18030', errors='ignore')
bro.quit()