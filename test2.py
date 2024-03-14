import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QToolBar, QStatusBar
from PyQt6.QtGui import QIcon, QAction


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Editor')
        self.setWindowIcon(QIcon('./assets/editor.png'))

        self.setGeometry(0, 0, 1400, 800)

        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
