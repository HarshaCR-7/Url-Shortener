'''import feedparser
from dateutil import parser
feed = feedparser.parse("https://www.udayavani.com/feed")
item = feed.entries
print(item[4])
'''
from lxml import etree
import urllib.request
import xml.etree.ElementTree as ET

url = 'https://www.udayavani.com/feed'


document = urllib.request.urlopen(url).read()
# XML strings to etree
addressbook_root = etree.fromstring(document)
note_root = etree.fromstring(document)

# append the note
addressbook_root.append(note_root)

# print the new addressbook XML document
print(etree.tostring(addressbook_root))