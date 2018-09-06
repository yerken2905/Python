import codecs
from lxml.html.soupparser import fromstring
from urllib.request import Request, urlopen
from urllib.parse import urlencode
import cx_Oracle
import time
from datetime import datetime
import socket

timeout = 100
socket.setdefaulttimeout(timeout)

aHref=[]
bSize=4000
#data=datetime.today().strftime("%d.%m.%Y")

def delUnLessSym(sPar):
    return sPar.replace('\n','').replace('\xa0','').replace('-','').lstrip()

def connect_oracle():
    try:
        global my_connection
        global ocursor
        my_connection=cx_Oracle.connect('yerken/1@xe')
        ocursor=my_connection.cursor()
        print('Logon success')
    except cx_Oracle.DatabaseError as info:
        print('Logon  Error:',info)

def mod_table_result(idRow, nameCol,  value):
    text='select * from z_025_temp_ol where id='+str(idRow)
    ocursor.execute(text)
    #print(text)
    if ocursor.fetchone():
        text="update z_025_temp_ol set " + nameCol + "=:s where id=" + str(idRow)
        text="begin execute immediate '"+text+ "' using '"+value+"'; end;"
        ocursor.execute(text)
        my_connection.commit()
    '''
    while len(value) > 0:
        text="insert into z_025_temp_result (sresult) values (:s)"
        text="begin execute immediate '"+text+ "' using '"+value[0:bSize]+"'; end;"
        value=value[bSize:]
        ocursor.execute(text)
    my_connection.commit()
    '''

def mod_table_ol(idRow, nameCol,  value):
    text='select * from z_025_temp_ol where id='+str(idRow)
    ocursor.execute(text)
    #print(text)
    if ocursor.fetchone():
        text="update z_025_temp_ol set " + nameCol + "=:s where id=" + str(idRow)
    elif nameCol=='s1':
        text="insert into z_025_temp_ol (id,"+nameCol+") values("+ str(idRow) + ",:s)"
    else:
        text=None
    if text is not None:
        text="begin execute immediate '"+text+ "' using '"+value+"'; end;"
        ocursor.execute(text)
        my_connection.commit()

def first_page():
    url='https://olimp.kz/index.php?page=table_live'
    print(url)
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    tree = fromstring(web_byte)
    #Список ставок
    for lTable in tree.xpath('//div[@class=\"lt-match\"]'):
        DataId=lTable.get('data-id')
        #print(DataId)
        aHref.append(DataId)
        cText=''
        for lBet in lTable.xpath('.//text()'):
            cRow=delUnLessSym(lBet)
            if len(cRow)>0:
                cText+=cRow+';'
        mod_table_ol(DataId, 's1', cText)

def bet_page():
    #aHref=['42851758']
    print('bet_page')
    text='select id from z_025_temp_ol'
    ocursor.execute(text)
    #for ch in aHref:
    for ch in ocursor.fetchall():
        url='https://olimp.kz/index.php?page=line&action=2&live[]='+str(ch[0])+'&sid[]=1'
        print(url)
        req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        tree = fromstring(web_byte)
        # Стаки
        cText=''
        for lTable in tree.xpath('.//span[@class=\"googleStatIssue\"]'):
            for lKoefs in lTable.xpath('.//text()'):
                cRow=delUnLessSym(lKoefs)
                if len(cRow)>0:
                    cText+=cRow+';'
        #print(ch,cText)
        mod_table_ol(ch[0], 's2', cText)

def result_page():
    url='https://olimp.kz/index.php?page=result'
    print(url)
    req=Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    tree = fromstring(web_byte)
    # Результаты
    for lTable in tree.xpath('.//table[@class=\"koeftable\"]'):
        for lTr in lTable.xpath('.//tr'):
            cId=lTr.xpath('.//td/div[@id]')
            try:
                ch=cId[len(cId)-1].get('id')[1:]
                #print(ch)
                cText=''
                for lKoefs in lTr.xpath('.//text()'):
                    cRow=delUnLessSym(lKoefs)
                    if len(cRow)>0:
                        cText+=cRow+';'
                mod_table_ol(ch, 's3', cText)
            except:
                pass

connect_oracle()
#time.sleep(100)
first_page()
#print(time.ctime())
bet_page()
result_page()
