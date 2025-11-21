from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ClientPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Client")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue Client !"))
        self.setLayout(layout)
