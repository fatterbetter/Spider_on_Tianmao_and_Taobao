
import inspect
import gzip
from qtui import Ui_Form
from PyQt5 import QtWidgets, QtGui, QtCore, QtNetwork, QtWebKit, QtPrintSupport
from PyQt5.QtWebKitWidgets import QWebPage
from PyQt5.QtWidgets import QInputDialog
import sys
import requests
import re
import os
from lxml import _elementpath

# 注意，该程序不会运行，cookie已经删了
class myqt(QtWidgets.QWidget, Ui_Form):

    """docstring for myqt"""

    def __init__(self):
        super(myqt, self).__init__()
        self.setupUi(self)
        self.start()
        self.webView.page().setLinkDelegationPolicy(
            QWebPage.DelegateAllLinks)
        self.webView.linkClicked.connect(self.changeurl)
        self.pushButton.clicked.connect(self.start)

    def start(self):

        self.data = baidunews()
        for i in self.data[0]:
            self.listWidget.addItem(i[0])
        self.listWidget.itemClicked.connect(self.bindll)
        for i in self.data[1]:
            self.listWidget_2.addItem(i[0])
        self.listWidget_2.itemClicked.connect(self.bindee)

    def changeurl(self, ee):
        self.webView.load(ee)

    def bindll(self, item):
        ee = dict(self.data[0])[item.text()]
        self.webView.load(QtCore.QUrl(ee))

    def bindee(self, item):
        ee = dict(self.data[1])[item.text()]
        self.webView.load(QtCore.QUrl(ee))


def baidunews():
    headers = {'Host': 'www.baidu.com', 'Referer': 'http://www.baidu.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0', 'Cookie': '这里改成你自己登录后的cookie'}
    r = requests.get(
        'http://www.baidu.com/home/xman/data/newscontent', headers=headers)
    r.encoding = 'base64'
    aa = r.text
    aa = eval(aa)

    hotWords = aa['data']['hotWords']
    hotWords = [(i['key'], 'http://www.baidu.com/baidu?cl=3&tn=baidutop10&fr=top1000&wd=' + i['key'])
                for i in hotWords]
    imgNews = aa["data"]["imgNews"]
    imgNews = [(i['title'], i['url'].replace('%3A', ':')) for i in imgNews]
    return (imgNews, hotWords)

app = QtWidgets.QApplication(sys.argv)
aa = myqt()
aa.show()
sys.exit(app.exec_())
