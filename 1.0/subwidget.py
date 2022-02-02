from tkinter import Y
from PyQt5.QtWidgets import QWidget,QFrame,QPushButton,QLabel
from PyQt5.QtCore import pyqtSignal

class SubWidget(QWidget):
    '''
    将具有parent的widget进行修饰,
    使其拥有与独立窗口一样的属性
    '''
    Close=pyqtSignal(str)
    MaxorNormal=pyqtSignal(str)
    SepWin=pyqtSignal(str)
    def __init__(self, parent,widget,name,title) -> None:
        super().__init__(parent)
        self.name=name
        self.titlebar=QFrame(self)  #标题栏
        self.titlebar.move(0,0)
        self.titlebar.setStyleSheet('QFrame{background-color:rgb(255,255,255)}')
        #图片以后再弄吧
        self.closebutton=QPushButton('关闭',self.titlebar)
        self.closebutton.clicked.connect(lambda:self.Close.emit(self.name))

        self.maxbutton=QPushButton('最大化',self.titlebar)
        self.maxbutton.clicked.connect(self.maxornormal)

        self.minbutton=QPushButton('最小化',self.titlebar)
        self.minbutton.clicked.connect(self.hide)

        self.sepbutton=QPushButton('独立',self.titlebar)
        self.sepbutton.clicked.connect(lambda:self.SepWin.emit(self.name))

        self.titlebar_buttons=[self.closebutton,self.maxbutton,self.minbutton,self.sepbutton]
        #标题
        self.title=QLabel(self.titlebar)
        self.title.setText(name)
        self.title.setGeometry(0,0,self.titlebar.width(),self.titlebar.height())

        self.widget=widget
        self.widget.setParent(self)
        self.widget.move(0,32)

        self.resize(widget.width(),widget.height()+32)
        self.normalsize=(self.width(),self.height())    #正常大小
        self.ismax=False    #是否是最大化

        self.setMouseTracking(True)
        self.ismove=False   #是否鼠标移动
        self.lastmousepos=None  #上一次鼠标位置

    def resizeEvent(self, a0) -> None:
        if not self.ismax:
            self.normalsize=(self.width(),self.height())
        self.titlebar.resize(self.width(),32)
        self.widget.move(0,32)
        self.widget.resize(self.width(),self.height()-32)
        curx=self.titlebar.width()-self.titlebar_buttons[0].width()
        for index,button in enumerate(self.titlebar_buttons):
            button.resize(button.width(),self.titlebar.height())
            button.move(curx,0)
            curx-=button.width()

    def maxornormal(self):
        if self.ismax:
            self.maxbutton.setText('最大化')
        else:
            self.maxbutton.setText('还原')
        self.MaxorNormal.emit(self.name)

    def mousePressEvent(self, a0) -> None:
        self.ismove=True
        self.lastmousepos=(a0.windowPos().x(),a0.windowPos().y())

    def mouseReleaseEvent(self, a0) -> None:
        x,y=a0.windowPos().x(),a0.windowPos().y()
        if self.lastmousepos==None:
            self.lastmousepos=(x,y)
        if not self.ismax:  #最大化时不能移动
            dx,dy=x-self.lastmousepos[0],y-self.lastmousepos[1] #计算偏移
            self.move(int(self.x()+dx),int(self.y()+dy))
        self.lastmousepos=(x,y)

    def mouseMoveEvent(self, a0) -> None:
        self.ismove=False