import json
import sys,os
from plugin import Plugin

from subwidget import SubWidget
sys.path.append(os.getcwd()+'\\plugins')
from PyQt5.QtWidgets import QWidget,QApplication
from start import Start

from taskbar import TaskBar

class Core(QWidget):
    '''
    启动器核心
    '''
    def __init__(self) -> None:
        super().__init__()
        self.config={    #配置信息
            'username':'Player'
        }

        self.resize(1000,618)
        self.setWindowTitle("MCDesktop")

        self.start=Start(self)
        self.start.hide()
        self.start.LoadPlugin.connect(self.load_plugin)

        self.taskbar=TaskBar(self)  #任务栏
        self.taskbar.StartUI.connect(self.startui)
        self.taskbar.PluginButtonBind.connect(self.pluginbuttonbind)

        self.loaded_plugin={}   #已加载的插件
        self.setMouseTracking(True)

        self.load_selfstarting_plugin()

    def load_selfstarting_plugin(self):
        '''
        加载自启动插件
        '''
        for name in self.start.selfstartingplugins:
            self.load_plugin(name)

    def resizeEvent(self, a0) -> None:
        self.taskbar.resize(self.width(),32)
        self.start.resize(self.width(),self.height()-self.taskbar.height())
        self.taskbar.move(0,self.start.height())

        for key,val in self.loaded_plugin.items():
            if hasattr(val,'ismax') and val.ismax:
                val.resize(self.width(),self.height()-self.taskbar.height())

    def startui(self):
        '''
        开始界面
        '''
        if self.start.isHidden():   #打开
            self.start.raise_() #置于最上层
            self.start.move(0,0)
            self.start.show()
        else:   #关闭
            self.start.hide()

    def load_plugin(self,name):
        '''
        加载插件
        '''
        if not self.start.isHidden():
            self.startui()
        if name not in self.loaded_plugin:
            plugin=__import__(name)
            config=json.load(open(f'plugins/{name}/config.json',encoding='utf-8'))
            if config['type']=='app':   #作为应用
                widget=plugin.__dict__[config['main']](self,self)
                self.set_subwidget(widget,name)
            elif config['type']=='back':    #后台
                main=plugin.__dict__[config['main']](self,self)
                #防止搞错
                self.loaded_plugin[name]=main

    def set_subwidget(self,widget,name):
        subwidget=SubWidget(self,widget,name,widget.windowTitle())
        subwidget.Close.connect(self.close_plugin)
        subwidget.MaxorNormal.connect(self.plugin_maxornormal)
        subwidget.SepWin.connect(self.sep_subwidget)
        subwidget.move(0,0)
        widget.show()
        subwidget.show()
        self.loaded_plugin[name]=subwidget
        self.taskbar.add_button(name)
        self.taskbar.raise_()   #置于最上层,防止subwidget太大导致taskbar无法使用

    def close_plugin(self,name):
        '''
        关闭插件
        '''
        self.loaded_plugin[name].close()
        self.loaded_plugin.pop(name)
        self.taskbar.pop_button(name)

    def pluginbuttonbind(self,name):
        '''
        与插件绑定的按钮的点击事件
        '''
        subwidget=self.loaded_plugin[name]
        if subwidget.isHidden():
            subwidget.raise_()
            self.taskbar.raise_()
            subwidget.show()
        else:
            subwidget.hide()

    def plugin_maxornormal(self,name):
        '''
        设置插件最大化或还原
        '''
        subwidget=self.loaded_plugin[name]
        if subwidget.ismax: #还原
            subwidget.ismax=not subwidget.ismax
            subwidget.resize(*subwidget.normalsize)
        else:   #最大化
            subwidget.ismax=not subwidget.ismax
            subwidget.resize(self.width(),self.height()-self.taskbar.height())
            subwidget.move(0,0)

    def sep_subwidget(self,name):
        '''
        独立窗口
        '''
        subwidget=self.loaded_plugin[name]
        subwidget.widget.setParent(None)
        subwidget.widget.show()
        self.close_plugin(name)

if __name__=='__main__':
    app=QApplication(sys.argv)
    core=Core()
    core.show()
    sys.exit(app.exec_())