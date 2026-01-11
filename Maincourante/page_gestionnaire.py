#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GestionPage - Page du gestionnaire
Version : corrigée pour éviter duplication des lignes lors de la modification
Auteur : Adja & Marème
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QGroupBox, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QSizePolicy, QHeaderView, QMessageBox, QAction, QMenuBar
)
from PyQt5.QtCore import Qt
from datetime import datetime
from Connexion_dataBase import connexion
from envoie import Envoie



class GestionPage(QMainWindow):
    TITRE_FENETRE = "Page gestionnaire"

    def __init__(self):
        super().__init__()
        self.setWindowTitle(GestionPage.TITRE_FENETRE)
        self.resize(900, 600)

        # ===== MENU =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        self.__help = self.__menuBar.addMenu('&Apropos')
        self.__settings = self.__menuBar.addMenu('&Paramètres')

        self.__action_apropos = QAction('A propos', self)
        self.__action_add_line = QAction('Ajouter une ligne', self)
        self.__action_save = QAction('Enregistrer les modifications', self)

        self.__help.addAction(self.__action_apropos)
        self.__settings.addAction(self.__action_add_line)
        self.__settings.addAction(self.__action_save)

        self.__action_apropos.triggered.connect(self.a_propos)
        self.__action_add_line.triggered.connect(self.add_line)
        self.__action_save.triggered.connect(self.save_modif)

        # ===== BLOC GÉNÉRAL =====
        self.__bloc_general = QWidget()
        self.__bloc_general_lay = QVBoxLayout()
        self.__bloc_general.setLayout(self.__bloc_general_lay)
        self.setCentralWidget(self.__bloc_general)

        # ===== BLOC HAUT =====
        self.__bloc_haut = QGroupBox()
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)
        self.__bloc_general_lay.addWidget(self.__bloc_haut)

        self.__titre = QLabel("Profil: Gestionnaire")
        self.__Deconnecter = QPushButton("Déconnexion")
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        self.__Deconnecter.clicked.connect(self.deconnecter)

        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white;")

        # ===== BLOC TABLEAU =====
        self.__bloc_tableau = QTableWidget()
        self.__bloc_tableau.setColumnCount(5)
        self.__bloc_tableau.setHorizontalHeaderLabels(["Date", "Heure", "De", "À", "Description"])
        self.__bloc_tableau.verticalHeader().setVisible(False)
        self.__bloc_tableau.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__bloc_tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__bloc_tableau.horizontalHeader().setStretchLastSection(True)
        self.__bloc_general_lay.addWidget(self.__bloc_tableau)

        self.load_table_from_db()

    # ================== FONCTIONS ==================

    def load_table_from_db(self):
        """Charge le contenu de la table 'donnees' dans le tableau."""
        try:
            conn = connexion()
            cur = conn.cursor()
            cur.execute("SELECT id, date, heure, de, a, descriptif FROM donnees;")
            rows = cur.fetchall()

            self.__bloc_tableau.setRowCount(0)
            for row_data in rows:
                row = self.__bloc_tableau.rowCount()
                self.__bloc_tableau.insertRow(row)
                id_donnee = row_data[0]
                for col, value in enumerate(row_data[1:]):
                    item = QTableWidgetItem(str(value))
                    if col == 0:
                        # Stocke l'ID dans Qt.UserRole sur la première cellule
                        item.setData(Qt.UserRole, id_donnee)
                    self.__bloc_tableau.setItem(row, col, item)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les données : {e}")
        finally:
            cur.close()
            conn.close()

    def a_propos(self):
        QMessageBox.information(self, 'A propos',
                                'Cette application a été développée par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunication, SAÉ 2025-2026.')

    def add_line(self):
        """Ajoute une nouvelle ligne au tableau avec la date et l'heure actuelles."""
        row = self.__bloc_tableau.rowCount()
        self.__bloc_tableau.insertRow(row)
        now = datetime.now()
        date_item = QTableWidgetItem(now.strftime("%Y-%m-%d"))
        date_item.setData(Qt.UserRole, None)  # ID initialisé à None
        self.__bloc_tableau.setItem(row, 0, date_item)
        self.__bloc_tableau.setItem(row, 1, QTableWidgetItem(now.strftime("%H:%M:%S")))

    def save_modif(self):
        """Sauvegarde les modifications dans la DB et envoie via le réseau."""
        try:
            conn = connexion()
            cur = conn.cursor()

            for row in range(self.__bloc_tableau.rowCount()):
                date_item = self.__bloc_tableau.item(row, 0)
                heure_item = self.__bloc_tableau.item(row, 1)
                de_item = self.__bloc_tableau.item(row, 2)
                a_item = self.__bloc_tableau.item(row, 3)
                desc_item = self.__bloc_tableau.item(row, 4)

                # Ignore les lignes vides
                if not date_item or not heure_item:
                    continue

                date = date_item.text()
                heure = heure_item.text()
                de = de_item.text() if de_item else ""
                a = a_item.text() if a_item else ""
                descriptif = desc_item.text() if desc_item else ""

                id_donnee = date_item.data(Qt.UserRole)

                if id_donnee is None:
                    # INSERT
                    cur.execute("""
                        INSERT INTO donnees (date, heure, de, a, descriptif)
                        VALUES (%s,%s,%s,%s,%s)
                        RETURNING id
                    """, (date, heure, de, a, descriptif))
                    id_donnee = cur.fetchone()[0]
                    date_item.setData(Qt.UserRole, id_donnee)
                    action = "INSERT"
                else:
                    # UPDATE
                    cur.execute("""
                        UPDATE donnees
                        SET date=%s, heure=%s, de=%s, a=%s, descriptif=%s
                        WHERE id=%s
                    """, (date, heure, de, a, descriptif, id_donnee))
                    action = "UPDATE"

                # Envoi réseau
                Envoie.send(
                    "donnee",
                    action,
                    {
                        "id": id_donnee,
                        "date": date,
                        "heure": heure,
                        "de": de,
                        "a": a,
                        "descriptif": descriptif
                    }
                )

            conn.commit()
            QMessageBox.information(self, "Enregistrement", "Modifications enregistrées et synchronisées")
        except:
            conn.rollback()
            QMessageBox.critical(self, "Erreur", "Erreur sauvegarde ")
        finally:
            cur.close()
            conn.close()

    def deconnecter(self):
        rep = QMessageBox.question(self, "Déconnexion", "Voulez-vous vous déconnecter ?", QMessageBox.Yes | QMessageBox.No)
        if rep == QMessageBox.Yes:
            self.close()


# ================== MAIN ==================
def main():
    app = QApplication(sys.argv)
    window = GestionPage()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
