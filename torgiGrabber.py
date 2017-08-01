# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv

# МПК
hrefs = []
choice = -1
choices = ['Реестр изобретений', 'Реестр заявок на выдачу патента на изобретение',
           'Реестр полезных моделей']

MPK = input('Введите МПК\n')
inp = input('''Выберите базу:
0 - Реестр изобретений,	
1 - Реестр заявок на выдачу патента на изобретение,
2 - Реестр полезных моделей,
3 - Всё выше перечисленное
''')
flg = False
while not flg:
    try:
        choice = int(inp)
        if choice in range(4):
            flg = True
    except:
        pass
    if not flg:
        inp = input('''Выберите базу:
        0 - Реестр изобретений,	
        1 - Реестр заявок на выдачу патента на изобретение,
        2 - Реестр полезных моделей,
        3 - Всё выше перечисленное
        ''')


def getPatentLinks(driver):
    # получаем ссылки на патенты
    tableXPath = '//*[@id="mainContent"]/table/tbody/tr[1]/td/div[2]/table/tbody/tr[1]/td[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr/td/table'
    table = driver.find_element_by_xpath(tableXPath)
    tds = table.find_elements_by_tag_name('td')
    for td in tds:
        try:
            a = td.find_element_by_tag_name('a')
            href = a.get_attribute("href")
            if a.text != '':
                hrefs.append({'link': href, 'patent': a.text})
        except:
            pass


def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def nextPage(driver):
    pagerXpath = '//*[@id="mainContent"]/table/tbody/tr[1]/td/div[2]/table/tbody/tr[1]/td[2]/div[2]/div/table/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr/td/div/table/tbody/tr/td/table[2]'
    try:
        table = driver.find_element_by_xpath(pagerXpath)
        tds = table.find_elements_by_tag_name('td')
        pageNum = 0
        for td in tds:
            if isint(td.text):
                a = td.find_element_by_tag_name('a')
                href = a.get_attribute("href")
                if (pageNum != 0) and (int(td.text) == pageNum + 1):
                    a.click()
                    return True
                if href is None:
                    pageNum = int(a.text)

    except:
        pass
    return False


def loadAll(s):
    del hrefs[:]
    driver = webdriver.Chrome('C:\\Program Files\\SeleniumUtils\\chromedriver.exe')
    fipshref = 'http://www1.fips.ru/wps/portal/!ut/p/c5/jY5BDoIwFESP1G9pEJctxrYKFYFqYUNINAYi0AVB5fTCAURnlpM3eShHU9tyqO5lX3Vt-UAG5W4hJY3Ega_giEMA6ilNd3sXA3emPXMLn1NB1gEAV7EPkjCCBWcYpPMPDV9C4Qd9QQZIkdSeDd-9CUZ_SOvxhMMxgX5LXyrNHKWi6HqONaNMbxJtJyafX5eM533BSYmuuSHbaD1Y8fwAG_rMsA!!/dl3/d3/L0lDU0lKSmdwcGlRb0tVUWtnQSEhL29Pb2dBRUlRaGpFQ1VJZ0FFQUl5RkFNaHdVaFM0TFVFQVVvIS80QzFiOVdfTnIwZ0NVZ3hFbVJDVXdpSkg0QSEhLzdfSUlBUEhLRzEwTzJNMDBBOE5VQUZKNjJHUzUvRHpzWUozMzAzMDE4MC8zNjExOTg1MTI1NzYvYWNOYW1lL3RyZWVCYWNr/'
    driver.get(fipshref)

    driver.find_element_by_link_text(s).click()
    # выбор патентов по МПК
    time.sleep(1)
    select = Select(driver.find_element_by_xpath('//*[@id="searchPar"]'))
    select.select_by_visible_text("Индекс МПК")

    input = driver.find_element_by_xpath('//*[@id="textfield3"]')
    input.send_keys(MPK)

    driver.find_element_by_xpath('//*[@id="imageField2"]').click()
    time.sleep(1)
    getPatentLinks(driver)
    while nextPage(driver):
        getPatentLinks(driver)
        time.sleep(1)

    driver.close()

    with open('loads/' + MPK.replace('/', '_') + '(' + s + ').csv', 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        for href in hrefs:
            spamwriter.writerow([href['patent'], href['link']])

    print('Загружено: ' + str(len(hrefs)) + " ссылок")


if choice == 3:
    for c in choices:
        loadAll(c)
else:
    loadAll(choices[choice])
