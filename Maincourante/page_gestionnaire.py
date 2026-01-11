
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: page_gestionnaire
   :platform: Unix, Windows
   :synopsis: Manager interface for viewing and modifying the main log
              entries of the SSF main log application.

This module provides the graphical manager page of the application.
It allows users with the manager role to:
- view main log entries,
- add new entries with current date and time,
- modify existing entries,
- save changes to the database,
- synchronize data with other workstations over the network.

.. moduleauthor:: Adja Diarietou Mbengue <adja.diarietou.mbengue@etu.univ-poitiers.fr>
.. moduleauthor:: Marème Mboup <mareme.mboup@etu.univ-poitiers.fr>
"""


import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QGroupBox, QPushButton, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QSizePolicy, QHeaderView, QMessageBox, QAction, QMenuBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from datetime import datetime
from Connexion_dataBase import connexion
from envoie import Envoie



class GestionPage(QMainWindow):
    """
    Main manager window.

    This class implements the graphical interface used by managers
    to consult and update the main log entries. Users can add new rows,
    modify existing entries, save changes to the local database, and
    synchronize updates with other connected machines.
    """

    TITRE_FENETRE = "Page gestionnaire"

    def __init__(self):
        """
        Initializes the manager page interface.

        This method sets up the main window, menus, graphical layouts,
        signal connections, and loads the current main log entries
        from the database.
        """
        super().__init__()
        self.setWindowTitle(GestionPage.TITRE_FENETRE)
        self.resize(900, 600)

        # ===== MENU =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        self.__help = self.__menuBar.addMenu('&Apropos')
        self.__settings = self.__menuBar.addMenu('&Paramètres')

        self.__action_apropos = QAction(QIcon('actions/icone_3.png'), 'A propos', self)
        self.__action_add_line = QAction(QIcon('actions/icone_1.png'), 'Ajouter une ligne', self)
        self.__action_save = QAction(QIcon('actions/icone_2.png'), 'Enregistrer les modifications', self)

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
        """
        Loads main log entries from the database into the table.

        This function retrieves all rows from the 'donnees' table
        and populates the QTableWidget with the data. The entry ID is
        stored in the Qt.UserRole of the first cell of each row.

        :raises Exception: If a database connection or query fails.
        """

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
                       
                        item.setData(Qt.UserRole, id_donnee)
                    self.__bloc_tableau.setItem(row, col, item)
        except:
            QMessageBox.critical(self, "Erreur", "Impossible de charger les données ")
        finally:
            cur.close()
            conn.close()

    def a_propos(self):
        
        """
        Displays application information.

       This function shows a message box with information about
       the project and its development context.
        """
        QMessageBox.information(self, 'A propos',
                                'Cette application a été développée par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunication, SAÉ 2025-2026.')

    def add_line(self):
   
        """
        Adds a new row to the main log table.

        The new row is initialized with the current date and time.
        The row ID is initially set to None until saved to the database.
        """
        row = self.__bloc_tableau.rowCount()
        self.__bloc_tableau.insertRow(row)
        now = datetime.now()
        date_item = QTableWidgetItem(now.strftime("%Y-%m-%d"))
        date_item.setData(Qt.UserRole, None)  # ID initialisé à None
        self.__bloc_tableau.setItem(row, 0, date_item)
        self.__bloc_tableau.setItem(row, 1, QTableWidgetItem(now.strftime("%H:%M:%S")))

    def save_modif(self):
        """
        Saves modifications to the database and sends updates over the network.

        This function iterates through all rows of the table, inserting
        new entries or updating existing ones based on the stored ID.
        After database operations, each change is sent to other workstations
        using the network synchronization system.

        :raises Exception: If a database or network error occurs.
        """

        try:
            conn = connexion()
            cur = conn.cursor()

            for row in range(self.__bloc_tableau.rowCount()):
                date_item = self.__bloc_tableau.item(row, 0)
                heure_item = self.__bloc_tableau.item(row, 1)
                de_item = self.__bloc_tableau.item(row, 2)
                a_item = self.__bloc_tableau.item(row, 3)
                desc_item = self.__bloc_tableau.item(row, 4)

         
                if not date_item or not heure_item:
                    continue

                date = date_item.text()
                heure = heure_item.text()
                de = de_item.text() if de_item else ""
                a = a_item.text() if a_item else ""
                descriptif = desc_item.text() if desc_item else ""

                id_donnee = date_item.data(Qt.UserRole)

                if id_donnee is None:
               
                    cur.execute("""
                        INSERT INTO donnees (date, heure, de, a, descriptif)
                        VALUES (%s,%s,%s,%s,%s)
                        RETURNING id
                    """, (date, heure, de, a, descriptif))
                    id_donnee = cur.fetchone()[0]
                    date_item.setData(Qt.UserRole, id_donnee)
                    action = "INSERT"
                else:
                  
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
        """
        Handles manager logout.

        A confirmation dialog is displayed before closing the manager window.
        """
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
