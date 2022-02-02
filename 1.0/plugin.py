from PyQt5.QtWidgets import QWidget

class Plugin(QWidget):
    '''
    插件
    '''
    def __init__(self, core,parent=None) -> None:
        super().__init__(parent)
        self.core=core

    def add_start_button(self,button):
        '''
        在开始侧边栏添加按钮
        '''
        button.setParent(self.core.start.panel)
        self.core.start.buttongroups.append(button)
        self.core.start.resizeEvent(None)

    def open_widget(self,widget):
        '''
        打开widget
        '''
        if not self.core.start.isHidden():
            self.core.startui()
        self.core.set_subwidget(widget,widget.windowTitle())