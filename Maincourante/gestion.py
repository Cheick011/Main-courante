from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class GestionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Page Gestionnaire")
        self.setGeometry(300, 300, 400, 200)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Bienvenue Gestionnaire !"))
        self.setLayout(layout)
