import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Client")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue Client !"))
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClientPage()
    window.show()
    sys.exit(app.exec_())
