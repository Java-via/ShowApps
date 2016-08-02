# _*_ coding: utf-8 _*_

from bs4 import BeautifulSoup
import urllib.request
import logging

logging.basicConfig(level=logging.DEBUG)


def parse(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html5lib")
    # logging.debug("soup is %s", soup.get_text)
    # f = codecs.open("f:/soup.txt", "a", "utf-8")
    # f.write(str(soup.prettify()))
    # logging.debug("write over")
    # f.close()
    # _div = soup.find_all("div", class_="com-container")
    _desc_soup = soup.find("div", class_="det-app-data-info")
    logging.debug("description is %s", _desc_soup.get_text().strip())


if __name__ == "__main__":
    parse("http://sj.qq.com/myapp/detail.htm?apkName=air.tv.douyu.android")
