# _*_ coding: utf-8 _*_

import urllib.request
import logging

logging.basicConfig(level=logging.DEBUG)

url = "http://pp.myapp.com/ma_icon/0/icon_9997_1470306881/96"
data = urllib.request.urlopen(url).read()
f = open("f:/data/test.jpg", "wb")
f.write(data)
f.close()
