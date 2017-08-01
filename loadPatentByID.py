# -*- coding: utf-8 -*-
import csv
import os
import re
import urllib

import pdfkit
import requests
import time
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import csv

from PyPDF2 import PdfFileReader
from bs4 import BeautifulSoup
from fpdf import FPDF

choices = ['Реестр изобретений', 'Реестр заявок на выдачу патента на изобретение',
           'Реестр полезных моделей']

pid = input('Введите id\n')


def loadPage(url, path):
    html = requests.get(url).text
    if (str(html).find('Превышен допустимый предел количества просмотров документов из реестра в день.') != -1):
        print('Превышен допустимый предел количества просмотров документов из реестра в день.')
        exit()

    dl = 1
    while (str(html).find('Слишком быстрый просмотр документов.') != -1):
        time.sleep(dl)
        dl += 1
        print('to speed')
        html = requests.get(url).text

    if str(html).find('ФАКСИМИЛЬНЫЕ ИЗОБРАЖЕНИЯ') != -1:
        imgs = set()
        soup = BeautifulSoup(html, "lxml")
        for img in soup.findAll('img', {'class': 'FaxPage'}):
            imgs.add(img.parent['href'])
        i = 0
        imageList = []
        dly = 1
        complete = False
        while not complete:
            try:
                i = 0
                for img in sorted(imgs):
                    imgPath = "./tmp/" + str(i) + ".gif"
                    urllib.request.urlretrieve(img, imgPath)
                    imageList.append(imgPath)
                    i += 1
                    time.sleep(1)

                complete = True
            except:
                print('to speed')
                time.sleep(dly)
                dly += 1

        pdf = FPDF()
        # imagelist is the list with all image filenames
        for image in imageList:
            pdf.add_page()
            pdf.image(image, 10, 10, 200, 300)
        pdf.output(path)
    else:
        time.sleep(2)
        pdfkit.from_url(url, path)


'''
def loadPages(s):
    cnt = 0
    with open('loads/' + MPK.replace('/', '_') + '(' + s + ').csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        for row in spamreader:
            if (len(row) > 0):
                cnt += 1

    with open('loads/' + MPK.replace('/', '_') + '(' + s + ').csv', 'r') as csvfile:
        pos = 0
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        for row in spamreader:
            #print(row)
            if (len(row) > 0):
                pos += 1
                print(str(pos) + "/" + str(cnt))
                time.sleep(1)
                loadPatent(MPK, s, row[1], row[0])
'''


def loadPatentByID(s):
    driver = webdriver.Chrome('C:\\Program Files\\SeleniumUtils\\chromedriver.exe')
    fipshref = 'http://www1.fips.ru/wps/portal/!ut/p/c5/jY5BDoIwFESP1G9pEJctxrYKFYFqYUNINAYi0AVB5fTCAURnlpM3eShHU9tyqO5lX3Vt-UAG5W4hJY3Ega_giEMA6ilNd3sXA3emPXMLn1NB1gEAV7EPkjCCBWcYpPMPDV9C4Qd9QQZIkdSeDd-9CUZ_SOvxhMMxgX5LXyrNHKWi6HqONaNMbxJtJyafX5eM533BSYmuuSHbaD1Y8fwAG_rMsA!!/dl3/d3/L0lDU0lKSmdwcGlRb0tVUWtnQSEhL29Pb2dBRUlRaGpFQ1VJZ0FFQUl5RkFNaHdVaFM0TFVFQVVvIS80QzFiOVdfTnIwZ0NVZ3hFbVJDVXdpSkg0QSEhLzdfSUlBUEhLRzEwTzJNMDBBOE5VQUZKNjJHUzUvRHpzWUozMzAzMDE4MC8zNjExOTg1MTI1NzYvYWNOYW1lL3RyZWVCYWNr/'
    driver.get(fipshref)

    driver.find_element_by_link_text(s).click()
    # выбор патентов по МПК
    time.sleep(1)
    select = Select(driver.find_element_by_xpath('//*[@id="searchPar"]'))
    select.select_by_visible_text("Номер регистрации")

    input = driver.find_element_by_xpath('//*[@id="textfield3"]')
    input.send_keys(pid)

    main_window_handle = None
    while not main_window_handle:
        main_window_handle = driver.current_window_handle

    driver.find_element_by_xpath('//*[@id="imageField2"]').click()
    time.sleep(1)

    signin_window_handle = None
    while not signin_window_handle:
        for handle in driver.window_handles:
            if handle != main_window_handle:
                signin_window_handle = handle
                break
    driver.switch_to.window(signin_window_handle)

    link = ""
    for e in driver.find_elements_by_tag_name('a'):
        if e.text != "":
            link = e.get_attribute("href")
            break
    driver.close()
    driver.switch_to.window(main_window_handle)
    driver.close()
    loadPage(link, './patents/fromId/' + pid + '.pdf')


# 1110966

loadPatentByID(choices[0])


# loadPage(url1, './patents/1.pdf')
# loadPage(url2, './patents/2.pdf')

# скачать картинку
# urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")
