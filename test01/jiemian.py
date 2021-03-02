import sys
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QInputDialog


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.btn = QPushButton("输入年限", self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.ShowDialog)

        self.btn = QPushButton("输入年限", self)
        self.btn.move(630, 20)
        self.btn.clicked.connect(self.ShowDialog)


        self.le = QLineEdit(self)
        self.le.move(180, 22)

        self.setWindowTitle("房贷利率计算器")
        self.show()

    def ShowDialog(self):
        text, ok = QInputDialog.getText(self, "Input Dialog", "Enter your name:")
        if ok:
            self.le.setText(str(text))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
