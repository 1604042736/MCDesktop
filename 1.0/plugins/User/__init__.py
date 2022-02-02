from PyQt5.QtWidgets import QLabel,QLineEdit,QPushButton

from plugin import Plugin

class UserUI(Plugin):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.resize(500,309)
        self.setWindowTitle('用户')
        self.username_label=QLabel('用户名:',self)
        self.username_label.move(0,0)
        self.username_label.resize(40,16)
        self.username=QLineEdit(self.core.config['username'],self)
        self.username.move(40,0)
        self.username.resize(128,16)

class User(Plugin):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.user=QPushButton('用户')
        self.add_start_button(self.user)
        self.user.clicked.connect(lambda:self.open_widget(UserUI(*args)))