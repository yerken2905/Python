import codecs
from lxml.html.soupparser import fromstring
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import cx_Oracle
import time
import socket

timeout = 100
socket.setdefaulttimeout(timeout)

aHref=[]

def connect_oracle():
    try:
        global my_connection
        global ocursor
        my_connection=cx_Oracle.connect('colvir/main082018@cbsmain')
        ocursor=my_connection.cursor()
        print('Logon success')
    except cx_Oracle.DatabaseError as info:
        print('Logon  Error:',info)

def mod_table(idRow, nameCol,  value):
    text='select * from z_025_temp_ol where id='+str(idRow)
    ocursor.execute(text)
    print(text)
    if ocursor.fetchone():
        text="update z_025_temp_ol set " + nameCol + "='" + value + "' where id=" + str(idRow)
        #print(text)
    else:
        text="insert into z_025_temp_ol (id,"+nameCol+") values("+ str(idRow) + ",'"+ value +"')"
        #print(text)
    ocursor.execute(text)
    my_connection.commit()

def first_page():
    url='https://olimp.kz/index.php?page=table_live'
    print(url)
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    tree = fromstring(web_byte)
    sHref=[]
    #Список ставок
    for lTable in tree.xpath('//div[@class=\"lt-match\"]'):
        DataId=lTable.get('data-id')
        #print(DataId)
        aHref.append(DataId)
        cText=''
        for lBet in lTable.xpath('.//text()'):
            cRow=lBet.replace('\n','').replace('\xa0','')
            if len(cRow)>1:
                #print(cRow)
                cText+=cRow+';'
        mod_table(DataId, 's1', cText)

print(aHref)

def second_page():
    for ch in aHref:
        url='https://olimp.kz/index.php?page=line&action=2&live[]='+ch+'&sid[]=1'
        print(url)
        req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        tree = fromstring(web_byte)
        # Стаки
        cText=''
        for lTable in tree.xpath('.//span[@class=\"googleStatIssue\"]'):
            for lKoefs in lTable.xpath('.//text()'):
                cRow=lKoefs.replace('\n','').replace('\xa0','').replace('-','')
                if len(cText)>1:
                    #print(cRow)
                    cText+=cRow+';'
        mod_table(ch, 's2', cText)


connect_oracle()
print(time.ctime())
time.sleep(100)
first_page()
print(time.ctime())
second_page()
