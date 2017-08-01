# -*- coding: utf-8 -*-
import csv
import os
import re
import urllib

import pdfkit
import requests
import time

from PyPDF2 import PdfFileReader
from bs4 import BeautifulSoup
from fpdf import FPDF

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


def createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def getDir(MPK, tp):
    return './patents/' + MPK.replace('/', '_') + '/' + tp + '/'


def loadPatent(MPK, tp, link, number):
    print(number + '(' + tp + ')')
    directory = getDir(MPK, tp)
    createDir(directory)
    try:
        loadPage(link, directory + number + '.pdf')
    except:
        print("Ошибка загрузки: " + number)


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


if choice == 3:
    for c in choices:
        loadPages(c)
else:
    loadPages(choices[choice])

# loadPage(url1, './patents/1.pdf')
# loadPage(url2, './patents/2.pdf')

# скачать картинку
# urllib.urlretrieve("http://www.gunnerkrigg.com//comics/00000001.jpg", "00000001.jpg")
