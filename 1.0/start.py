import json
import os
from PyQt5.QtWidgets import QWidget,QPushButton,QFrame,QListWidget
from PyQt5.QtCore import pyqtSignal

class Start(QWidget):
    '''
    开始界面
    '''
    LoadPlugin=pyqtSignal(str)
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.panel=QFrame(self)
        self.panel.move(0,0)

        self.buttongroups=[]
        self.selfstartingplugins=[] #自启动插件

        self.ui=QFrame(self)
        self.pluginlist=QListWidget(self.ui)
        self.pluginlist.itemClicked.connect(self.load_plugin)
        self.set_pluginlist()

    def resizeEvent(self, a0) -> None:
        self.panel.resize(32,self.height())
        cury=self.panel.height()-self.panel.width()
        for index,button in enumerate(self.buttongroups):
            button.resize(self.panel.width(),self.panel.width())
            button.move(0,cury)
            cury-=button.height()
        self.ui.resize(self.width()-self.panel.width(),self.height())
        self.ui.move(self.panel.width(),0)
        self.pluginlist.resize(self.ui.width(),self.ui.height())

    def set_pluginlist(self):
        '''
        获取所有的插件
        '''
        self.pluginlist.clear()
        for i in os.listdir('plugins'):
            config=json.load(open(f'plugins/{i}/config.json',encoding='utf-8'))
            self.pluginlist.addItem(i)
            if config['self_starting']:
                self.selfstartingplugins.append(i)

    def load_plugin(self):
        '''
        加载插件
        '''
        name=self.pluginlist.currentItem().text()
        self.LoadPlugin.emit(name)