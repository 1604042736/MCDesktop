from PyQt5.QtWidgets import QPushButton

from plugin import Plugin

class Homepage(Plugin):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.setWindowTitle('主页')
        self.resize(500,309)
        self.move(0,0)
        self.startgame=QPushButton('开始游戏',self)