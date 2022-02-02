from PyQt5.QtWidgets import QWidget,QPushButton
from PyQt5.QtCore import pyqtSignal

class TaskBar(QWidget):
    '''
    标题栏
    '''
    StartUI=pyqtSignal()
    PluginButtonBind=pyqtSignal(str)
    def __init__(self,parent=None) -> None:
        super().__init__(parent)
        self.start=QPushButton("开始",self)
        self.start.move(0,0)
        self.start.clicked.connect(self.StartUI.emit)

        self.buttongroups=[]    #按钮群

    def resizeEvent(self, a0) -> None:
        self.start.resize(self.height(),self.height())
        curx=self.start.height()    #当前位置
        for index,button in enumerate(self.buttongroups):
            button.resize(button.width(),self.height())
            button.move(curx,0)
            curx+=button.width()

    def add_button(self,name):
        '''
        往按钮群中添加按钮
        '''
        button=QPushButton(name,self)
        button.clicked.connect(lambda:self.PluginButtonBind.emit(name))
        button.show()
        self.buttongroups.append(button)
        self.resizeEvent(None)

    def pop_button(self,name):
        '''
        删除按钮
        '''
        for index,button in enumerate(self.buttongroups):
            if button.text()==name:
                button.close()
                self.buttongroups.pop(index)
                break
        self.resizeEvent(None)