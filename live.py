import codecs
from lxml.html.soupparser import fromstring
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import cx_Oracle
import time
from datetime import datetime
import socket

timeOut = 100
socket.setdefaulttimeout(timeOut)

aHref = []
bSize = 4000


dataToday=datetime.today().strftime("%d.%m.%Y")

def deleteSymbolUnless(sPar):
    return sPar.replace('\n', '').replace('\xa0', '').replace('-', '').strip()

def connectURL(url):
    print(url)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webByte = urlopen(req).read()
    return fromstring(webByte)


def connectDB():
    try:
        global connectionDB
        global cursorDB
        connectionDB = cx_Oracle.connect('colvir/main082018@cbsmain')
        cursorDB = connectionDB.cursor()
        print('Logon success')
    except cx_Oracle.DatabaseError as info:
        print('Logon  Error:', info)


def mod_table_ol(idRow, nameCol, value, nameRow=None):
    text = 'select s2 from z_025_temp_ol where id=' + str(idRow)
    cursorDB.execute(text)
    text=None
    if nameCol=='s1':
        if not cursorDB.fetchone():
            text = "insert into z_025_temp_ol (id," + nameCol + ",s4) values(" + str(idRow) + ",:s, ''" + nameRow + "'')"
    elif nameCol=='s2':
        if cursorDB.fetchone()[0] is None:
            text = "update z_025_temp_ol set " + nameCol + "=:s where id=" + str(idRow)
    elif nameCol=='s3':
        if cursorDB.fetchone():
            text = "update z_025_temp_ol set " + nameCol + "=:s where id=" + str(idRow)
    if text is not None:
        text = "begin execute immediate '" + text + "' using '" + value + "'; end;"
        try:
            cursorDB.execute(text)
            connectionDB.commit()
        except:
            print(text)


def liveTablePage():
    tree = connectURL('https://olimp.kz/index.php?page=table_live')
    # Список ставок
    for lTable in tree.xpath('//div[@class=\"lt-match\"]'):
        DataId = lTable.get('data-id')
        cText = ''
        for lBet in lTable.xpath('.//text()'):
            cRow = deleteSymbolUnless(lBet)
            if len(cRow) > 0:
                cText += cRow + ';'
        mod_table_ol(DataId, 's1', cText)


def betPage():
    # aHref=['42851758']
    text = "select id from z_025_temp_ol where dbms_lob.substr(s1,10,1)>='" + dataToday + "'"
    print(text)
    cursorDB.execute(text)
    # for ch in aHref:
    for ch in cursorDB.fetchall():
        tree = connectURL('https://olimp.kz/index.php?page=line&action=2&live[]=' + str(ch[0]) + '&sid[]=1')
        # Стаки
        cText = ''
        for lTable in tree.xpath('.//span[@class=\"googleStatIssue\"]'):
            for lKoefs in lTable.xpath('.//text()'):
                cRow = deleteSymbolUnless(lKoefs)
                if len(cRow) > 0:
                    cText += cRow + ';'
        mod_table_ol(ch[0], 's2', cText)


def resultPage():
    tree = connectURL('https://olimp.kz/index.php?page=result')
    # Результаты
    for lTable in tree.xpath('.//table[@class=\"koeftable\"]'):
        for lTr in lTable.xpath('.//tr'):
            cId = lTr.xpath('.//td/div[@id]')
            try:
                ch = cId[len(cId) - 1].get('id')[1:]
                # print(ch)
                cText = ''
                for lKoefs in lTr.xpath('.//text()'):
                    cRow = deleteSymbolUnless(lKoefs)
                    if len(cRow) > 0:
                        cText += cRow + ';'
                mod_table_ol(ch, 's3', cText)
            except:
                pass

def livePage():
    tree = connectURL('https://olimp.kz/betting')
    # Список ставок
    for lTable in tree.xpath('//tr/td[@data-sport]'):
        DataSport = lTable.get('data-sport')
        NameSport = lTable.xpath('.//a/b')[0].text
        for lSport in lTable.xpath('//tr[@data-sport=\"' + DataSport + '\"]'):
            DataId = lSport.xpath('.//td/input/@value')[0]
            cText = ''
            for lBet in lSport.xpath('.//text()'):
                cRow = deleteSymbolUnless(lBet)
                if len(cRow) > 0:
                    cText += cRow + ';'
            print(cText)
            mod_table_ol(DataId, 's1', cText, NameSport)


connectDB()
time.sleep(100)
livePage()
#liveTablePage()
# print(time.ctime())
betPage()
resultPage()
