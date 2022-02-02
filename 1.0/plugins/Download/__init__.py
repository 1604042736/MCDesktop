from PyQt5.QtCore import QThread,pyqtSignal
from PyQt5.QtWidgets import QStackedWidget,QWidget,QPushButton,QLabel,QListWidget,QVBoxLayout,QLineEdit
import sys, requests, json, os, shutil
from plugin import Plugin

class GetContent(QThread):
    Content=pyqtSignal(list)
    def __init__(self,t,version=None):
        super().__init__()
        self.t=t    #类型
        self.version=version

    def get_version(self):
        url = 'http://launchermeta.mojang.com/mc/game/version_manifest.json'
        r = requests.get(url)
        self.Content.emit([version['id'] for version in json.loads(r.content)['versions']])
        
    def get_forge(self):
        url = f'https://bmclapi2.bangbang93.com/forge/minecraft/{self.version}'
        r = requests.get(url)
        self.Content.emit([forge['version'] for forge in json.loads(r.content)])

    def get_optifine(self):
        url = f'https://bmclapi2.bangbang93.com/optifine/{self.version}'
        r = requests.get(url)
        self.Content.emit([optifine['mcversion'] + ' ' + optifine['type'] + ' ' + optifine['patch'] for optifine in json.loads(r.content)])

    def get_liteloader(self):
        url = f'https://bmclapi2.bangbang93.com/liteloader/list?mcversion={self.version}'
        r = requests.get(url)
        self.Content.emit([json.loads(r.content)['mcversion'] + ' ' + json.loads(r.content)['version']])
            
    def run(self):
        if self.t=='version':
            self.get_version()
        elif self.t=='forge':
            self.get_forge()
        elif self.t=='optifine':
            self.get_optifine()
        elif self.t=='liteloader':
            self.get_liteloader()

class Download(Plugin):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setWindowTitle('下载')
        self.resize(500,309)

        self.sw=QStackedWidget(self)
        self.w_choose=QWidget()
        self.le_name=QLineEdit(self.w_choose)
        self.pb_version=QPushButton('版本:未选择',self.w_choose)
        self.pb_forge=QPushButton('Forge:未选择',self.w_choose)
        self.pb_forge.setEnabled(False)
        self.pb_optifine=QPushButton('Optifine:未选择',self.w_choose)
        self.pb_optifine.setEnabled(False)
        self.pb_liteloader=QPushButton('Liteloader:未选择',self.w_choose)
        self.pb_liteloader.setEnabled(False)
        self.pb_download=QPushButton('下载',self.w_choose)
        self.pb_download.setEnabled(False)

        self.pb_version.clicked.connect(self.while_pb_version_clicked)
        self.pb_forge.clicked.connect(self.while_pb_forge_clicked)
        self.pb_optifine.clicked.connect(self.while_pb_optifine_clicked)
        self.pb_liteloader.clicked.connect(self.while_pb_liteloader_clicked)

        vbox=QVBoxLayout()
        vbox.addWidget(self.le_name)
        vbox.addWidget(self.pb_version)
        vbox.addWidget(self.pb_forge)
        vbox.addWidget(self.pb_optifine)
        vbox.addWidget(self.pb_liteloader)
        vbox.addWidget(self.pb_download)
        self.w_choose.setLayout(vbox)

        self.w_content=QWidget()
        self.lw_choose=QListWidget(self.w_content)
        self.lw_choose.itemClicked.connect(self.on_lw_choose_itemClicked)
        self.pb_yes=QPushButton('是',self.w_content)
        self.pb_yes.setEnabled(False)
        self.pb_yes.clicked.connect(self.on_pb_yes_clicked)
        self.pb_no=QPushButton('否',self.w_content)
        self.pb_no.clicked.connect(self.on_pb_no_clicked)

        vbox=QVBoxLayout()
        vbox.addWidget(self.lw_choose)
        vbox.addWidget(self.pb_yes)
        vbox.addWidget(self.pb_no)
        self.w_content.setLayout(vbox)

        self.sw.addWidget(self.w_choose)
        self.sw.addWidget(self.w_content)

        self.sw.setCurrentIndex(0)
        self.l_info=QLabel(self.w_choose)
        self.l_info.setGeometry(0,0,100,32)
        self.l_info.hide()
        self.l_info.raise_()

    def set_lw_choose_content(self,l):
        try:
            self.pb_yes.setEnabled(False)
            self.lw_choose.clear()
            for i in l:
                self.lw_choose.addItem(i)
            self.l_info.hide()
            self.sw.setCurrentIndex(1)
        except:
            pass

    def resizeEvent(self, a0) -> None:
        self.sw.resize(self.width(),self.height())

    def while_pb_version_clicked(self):
        self.choose='version'
        self.l_info.setText('正在获取版本')
        self.l_info.show()
        self.t=GetContent('version')
        self.t.Content.connect(self.set_lw_choose_content)
        self.t.start()
        

    def while_pb_forge_clicked(self):
        self.choose='forge'
        version=self.pb_version.text().split(':')[-1]
        self.l_info.setText('正在获取forge')
        self.l_info.show()
        self.t=GetContent('forge')
        self.t.Content.connect(self.set_lw_choose_content)
        self.t.start()

    def while_pb_optifine_clicked(self):
        self.choose='optifine'
        version=self.pb_version.text().split(':')[-1]
        self.l_info.setText('正在获取optifine')
        self.l_info.show()
        self.t=GetContent('optifine')
        self.t.Content.connect(self.set_lw_choose_content)
        self.t.start()
        

    def while_pb_liteloader_clicked(self):
        self.choose='liteloader'
        version=self.pb_version.text().split(':')[-1]
        self.l_info.setText('正在获取liteloader')
        self.l_info.show()
        self.t=GetContent('liteloader')
        self.t.Content.connect(self.set_lw_choose_content)
        self.t.start()

    def on_lw_choose_itemClicked(self):
        self.pb_yes.setEnabled(True)

    def on_pb_yes_clicked(self):
        #更新按钮文本
        if self.choose=='version':
            self.pb_version.setText(f'版本:{self.lw_choose.currentItem().text()}')
            self.pb_forge.setEnabled(True)
            self.pb_optifine.setEnabled(True)
            self.pb_liteloader.setEnabled(True)
            self.pb_download.setEnabled(True)
        elif self.choose=='forge':
            self.pb_forge.setText(f'Forge:{self.lw_choose.currentItem().text()}')
        elif self.choose=='optifine':
            self.pb_optifine.setText(f'OptiFine:{self.lw_choose.currentItem().text()}')
        elif self.choose=='liteloader':
            self.pb_liteloader.setText(f'Liteloader:{self.lw_choose.currentItem().text()}')
        self.sw.setCurrentIndex(0)

    def on_pb_no_clicked(self):
        self.sw.setCurrentIndex(0)