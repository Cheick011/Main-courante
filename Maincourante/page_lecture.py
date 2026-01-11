

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: page_lecture
   :platform: Unix, Windows
   :synopsis: Read-only interface for viewing main log entries in the
              SSF main log application.

This module provides the graphical interface for users with the
read-only profile. It allows users to:
- view all main log entries,
- refresh the table with the latest data from the database,
- log out of the application.

No modifications to the database are allowed from this interface.

.. moduleauthor:: Adja Diarietou Mbengue <adja.diarietou.mbengue@etu.univ-poitiers.fr>
.. moduleauthor:: Marème Mboup <mareme.mboup@etu.univ-poitiers.fr>
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView
from PyQt5.QtGui import QIcon, QKeySequence
from Connexion_dataBase import connexion


class ClientPage(QMainWindow):
     """
      Read-only main log window.

      This class implements the interface for users with read-only
      access. Users can consult the main log entries in a table,
      refresh the data, and disconnect from the application.
     """
     TITRE_FENETRE = "Main Courante"

    
     def __init__(self): 
        """
         Initializes the read-only client page.

         This method sets up the main window, menus, graphical layouts,
         signal connections, and loads the current main log entries
         from the database in read-only mode.
        """
        super().__init__()

        # ===== FENETRE =====
        self.setWindowTitle(ClientPage.TITRE_FENETRE)
        self.resize(900, 600)
        
        # ===== MENU =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        
        self.__help = self.__menuBar.addMenu('&Apropos')
        
        
        # ===== ACTIONS =====
        self.__action_apropos = QAction(QIcon('actions/icone_3.png'),'A propos', self)

        
        self.__help.addAction(self.__action_apropos)
        
        self.__action_apropos.triggered.connect(self.a_propos)
       
        
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
       
        
        self.__titre= QLabel("Profil: Lecture seule")
        self.__Deconnecter=QPushButton("Déconnexion")
        
      
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        self.__Deconnecter.clicked.connect(self.deconnexion)
        
       
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white;")

        
       
        # ===== BLOC CONTENEUR DU TABLEAU =====
        self.__bloc_tableau_conteneur = QWidget()
        self.__bloc_tableau_conteneur_lay = QVBoxLayout()
        self.__bloc_tableau_conteneur.setLayout(self.__bloc_tableau_conteneur_lay)
        self.__bloc_general_lay.addWidget(self.__bloc_tableau_conteneur)
         

        
       
        # ===== BLOC TABLEAU =====
        self.__bloc_tableau = QTableWidget() #TableWidget n’est pas censé recevoir un layout, ce n’est pas un conteneur.       
        self.__bloc_tableau.setColumnCount(5)
        self.__bloc_tableau.setHorizontalHeaderLabels(["Date", "Heure", "De", "À", "Description"])
        self.__bloc_tableau.verticalHeader().setVisible(False)        
        self.__bloc_tableau.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.__bloc_tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__bloc_tableau.horizontalHeader().setStretchLastSection(True) 
        self.__bloc_tableau_conteneur_lay.addWidget(self.__bloc_tableau)

        
        self.lecture_seule()
        self.actualiser()  

        
# ================== FONCTIONS ==================
             
     def a_propos(self):
         
      """
      Displays application information.

      This function shows a message box with details about the project,
      the development context, and its authors.
      """

      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunications promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')
    
     def lecture_seule(self):
        """
        Sets the main log table to read-only mode.

        This function disables editing for all cells of the QTableWidget.
        """
        self.__bloc_tableau.setEditTriggers( QTableWidget.NoEditTriggers)

     def actualiser(self):
        """
        Refreshes the main log table with the latest data from the database.

        This function retrieves all entries from the 'donnees' table
        ordered by ID and populates the table. Existing rows are reused
        or new rows are inserted as needed.

        :raises Exception: If loading data from the database fails.
        """
        try:
            conn = connexion()
            cur = conn.cursor()
            cur.execute("SELECT date, heure, de, a, descriptif FROM donnees ORDER BY id;")
            rows = cur.fetchall()

            for row_index, row_data in enumerate(rows):
                if row_index >= self.__bloc_tableau.rowCount():
                    self.__bloc_tableau.insertRow(row_index)
                for col_index, value in enumerate(row_data):
                    self.__bloc_tableau.setItem(row_index, col_index, QTableWidgetItem(str(value)))

        except:
             QMessageBox.critical(self, "Erreur", "Impossible de charger les données")
        finally:
             cur.close()
             conn.close()

        
     def deconnexion(self):
        """
        Handles logout of the read-only user.

        A confirmation dialog is displayed before closing the client window.
        """

        self.__rep = QMessageBox.question(
            self,
            "Déconnexion",
            "Voulez-vous vous déconnecter ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if self.__rep == QMessageBox.Yes:
            self.close()     
    
        
  
# ================== MAIN ==================    
def main():
    application = QApplication(sys.argv)
    window = ClientPage()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
