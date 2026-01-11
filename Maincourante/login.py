"""
Module d’authentification
========================

.. module:: auth
   :platform: Python / PyQt5 / PostgreSQL
   :synopsis: Gestion de l’authentification de l’application Main courante spéléologue
.. moduleauthor:: Gatlin ALLOHO <gatlin.alloho@etu.univ-poitiers.fr>

"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt

import psycopg2
from psycopg2.extras import DictCursor

from page_admin import AdminPage
from page_gestionnaire import GestionPage
from page_lecture import ClientPage
from reception import Reception

class LoginWindow(QWidget):
    """
    Fenêtre principale d’authentification.

    Cette classe fournit l’interface graphique permettant à un utilisateur
    de saisir ses identifiants et de se connecter à l’application.

    """
    def __init__(self):
        """
        Initialise la fenêtre de connexion.

        Cette méthode crée et configure l’interface graphique :
        - mise en page de la fenêtre,
        - champs de saisie pour l’identifiant et le mot de passe,
        - bouton de connexion.
        """
        super().__init__()

        self.setWindowTitle("Authentification - Main courante spéléologue")
        self.resize(600, 400)  # La fenêtre peut s’agrandir

        # --- Layout principal (centrage) ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

        # --- Widget interne FIXE ---
        content = QWidget()
        content.setFixedSize(400, 300)  # Le contenu NE CHANGE PAS DE TAILLE

        palette = content.palette()
        palette.setColor(QPalette.Window, QColor("#1e1e2f"))
        palette.setColor(QPalette.WindowText, QColor("#f0f0f0"))
        content.setPalette(palette)
        content.setAutoFillBackground(True)

        inner_layout = QVBoxLayout()
        inner_layout.setAlignment(Qt.AlignCenter)
        content.setLayout(inner_layout)

        main_layout.addWidget(content)

        # --- Titre ---
        title = QLabel("Authentification")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(title)

        subtitle = QLabel("Main courante spéléologue")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        inner_layout.addWidget(subtitle)

        # --- Champ identifiant ---
        self.username = QLineEdit()
        self.username.setPlaceholderText("Identifiant")
        self.username.setStyleSheet("""
            QLineEdit {
                background-color: #2e2e3e;
                border: 1px solid #4c4c6d;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }
        """)
        inner_layout.addWidget(self.username)

        # --- Champ mot de passe ---
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: #2e2e3e;
                border: 1px solid #4c4c6d;
                border-radius: 6px;
                padding: 6px;
                color: white;
            }
        """)
        inner_layout.addWidget(self.password)

        # --- Bouton connexion ---
        login_btn = QPushButton("SE CONNECTER")
        login_btn.setFont(QFont("Arial", 10, QFont.Bold))
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
            }
        """)
        login_btn.clicked.connect(self.login)
        inner_layout.addWidget(login_btn)

        # --- Message ---
        warning = QLabel(" Ne confiez vos mots de passe à personne")
        warning.setFont(QFont("Arial", 9, QFont.StyleItalic))
        warning.setAlignment(Qt.AlignCenter)
        warning.setStyleSheet("color: #ff7777;")
        inner_layout.addWidget(warning)

    def login(self):
        """
        Traite la demande de connexion de l’utilisateur.

        Cette méthode :
        - récupère les identifiants saisis,
        - établit une connexion à la base PostgreSQL,
        - vérifie l’authentification de l’utilisateur,
        - récupère son rôle,
        - lance le thread de communication réseau,
        - ouvre la page correspondant au rôle de l’utilisateur.
        """
        user = self.username.text()
        pwd = self.password.text()

        try:
            conn = psycopg2.connect(
                dbname="spelo_app",
                user="admin",
                password="admin",
                host="localhost"
                
            )
            conn.autocommit = True
            cursor = conn.cursor(cursor_factory=DictCursor)
        except Exception as e:
            QMessageBox.critical(self, "Erreur DB", f"Impossible de se connecter : {e}")
            return

        query = "SELECT role FROM utilisateurs WHERE nom_utilisateur=%s AND mot_de_passe=%s"
        cursor.execute(query, (user, pwd))
        result = cursor.fetchone()
        cursor.close()
        conn.close()


        if not result:
            QMessageBox.warning(self, "Erreur", "Identifiant ou mot de passe incorrect")
            return

        role = result["role"]

        if role == "admin":
            self.page = AdminPage()
            recv_thread = Reception()  # Crée l’objet thread
            recv_thread.start()
        elif role == "gestionnaire":
            self.page = GestionPage()
            recv_thread = Reception()  # Crée l’objet thread
            recv_thread.start()
        else:
            self.page = ClientPage()
            recv_thread = Reception()  # Crée l’objet thread
            recv_thread.start()

        self.page.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
