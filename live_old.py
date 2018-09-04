
import codecs
fileObj = codecs.open( "live.htm", "r", "utf_8" )
text = fileObj.read() # или читайте по строке
fileObj.close()

#import lxml.html
#from lxml import etree

from lxml.html.soupparser import fromstring
tree = fromstring(text)
#Таблица
for lTable in tree.xpath('//div[@class=\"LTable\"]'):
    # Виды спорта
    for lSports in lTable.xpath('.//div[@class=\"lt-sport\"]'):
        print(lSports.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]')[0].text)
        #Cпорт
        for lSport in lSports.xpath('.//div[@class=\"lt-sport-content lt-hideable lt-hide\"]'):
            #Чемпионат
            for lChamp in lSport.xpath('.//div[@class=\"lt-champ\"]'):
                print(lChamp.xpath('.//div[@class=\"lt-champ-title lt-showmore\"]')[0].text)
                for lBet in lChamp.xpath('.//div[@class=\"lt-match\"]'):
                    #Ид
                    print(lBet.get('data-id'))
                    #Время
                    print(lBet.xpath('.//td[@class=\"lt-match_date\"]')[0].text);
                    #Команды
                    print(lBet.xpath(".//div/table/tbody/tr/td[@class=\"lt-commands\"]/a/text()")[0])
                    #Результат
                    print(lBet.xpath('.//div/table/tbody/tr/td[@class=\"lt-commands\"]/div')[0].text)

            
fileObj = codecs.open( "bet.htm", "r", "utf_8" )
text = fileObj.read() # или читайте по строке
fileObj.close()
tree = fromstring(text)
# Стаки
for lTable in tree.xpath('.//span[@class=\"googleStatIssue\"]'):
    for lKoefs in lTable.xpath('.//span/text()'):
        #lBet=lTable.xpath('.//span[@class=\"googleStatIssueName\"]')
        #print(lBet[0].text)
        print(lKoefs)



import requests
payload = {'page': 'line', 'action': '2','live[]': ['42796377'], 'sid[]': ['1']}
r = requests.get('https://olimp.kz/index.php?page=line&action=2&live[]=42796377&sid[]=1')
r1 = requests.get('https://olimp.kz/index.php',payload)
print(r1.url)
tree=fromstring(r.text)
print(r)
for lTable in tree.xpath('.//span[@class=\"googleStatIssue\"]'):
    for lKoefs in lTable.xpath('.//span/text()'):
        #lBet=lTable.xpath('.//span[@class=\"googleStatIssueName\"]')
        #print(lBet[0].text)
        print(lKoefs)

'''
import socket

timeout = 30
socket.setdefaulttimeout(timeout)

import sys
from urllib.request import Request, urlopen
url="https://olimp.kz/betting"
req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
web_byte = urlopen(req).read()
webpage = web_byte.decode('utf-8')
'''
