
# Creating a routine that appends files to the output file
import os

from PyPDF2 import PdfFileWriter, PdfFileReader


def append_pdf(input,output):
    [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]




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


def mergePdf(s):
    output = PdfFileWriter()

    # Appending two pdf-pages from two different files
    #
    # append_pdf(PdfFileReader(open("SamplePage2.pdf","rb")),output)

    # Writing all the collected pages to a file
    #
    path = "./patents/" + MPK.replace('/', '_') + '/' + s + '/'
    flst = os.listdir(path=path)
    print(s+'-'+str(len(flst)))
    for f in flst:
        print(f)
        append_pdf(PdfFileReader(open(path+f, "rb")), output)
    output.write(open('./merget/'+MPK.replace('/', '_')+'('+s+').pdf', "wb"))

if choice == 3:
    for c in choices:
        mergePdf(c)
else:
    mergePdf(choices[choice])



