import codecs
fileObj = codecs.open( "live.html", "r", "utf_8_sig" )
text = fileObj.read() # или читайте по строке
fileObj.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(text, 'html.parser')
#print(soup)

import lxml.html
from lxml import etree
#tree=etree.HTML(text)
#r = tree.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]')
#print(r.div)
#html=soup.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]')

from lxml.html.soupparser import fromstring
tree = fromstring(text)
#ttt=etree.tostring(tree)
#zzz=etree.parse(ttt)
#ch=tree.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]')
for ch in tree.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]'):
    print(ch.text)

"""
import lxml.html
from lxml import etree
parse=etree.parse(text)
#xp1 = etree.XPath('.//div[@class=\"lt-sport-title lt-showmore\"]')
#html = lxml.html.fromstring(''.join(text))
#print(''.join(text))
#html=html.xpath('.//div[@class=\"lt-sport-title lt-showmore\"]')
#print(html)
#print(lxml.html.tostring(html))
"""
