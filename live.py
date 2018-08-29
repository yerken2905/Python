import codecs
fileObj = codecs.open( "live.htm", "r", "utf_8_sig" )
text = fileObj.read() # или читайте по строке
fileObj.close()

#import lxml.html
#from lxml import etree

from lxml.html.soupparser import fromstring
tree = fromstring(text)
for ch in tree.xpath('.//td[@class=\"liveMainSport forLiveFilter\"]'):
    for ch1 in ch.xpath('.//a/b'):
        print(ch1.text)
    for ch2 in ch.xpath('..[@data-sport]'):
        print(ch2.text)
        --print(ch.xpath('@data-sport/text()'))
#    print(ch.xpath('[@data-sport]'))
#nsports=1
#for nSports in range(1,10,1):
#    ch=tree.xpath('.//td[@data-sport=\"'+str(nSports)+'\"]/a/b')
#    print(ch[0].text)
