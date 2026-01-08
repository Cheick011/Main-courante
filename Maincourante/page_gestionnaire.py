
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version Nov 12 09:51:19 2025

@author1: adja
@author1: Marème

"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView
from PyQt5.QtGui import QIcon, QKeySequence
from Connexion_dataBase import connexion
from datetime import datetime

class GestionPage(QMainWindow):
    TITRE_FENETRE = "Page gestionnaire"
 
  
    def __init__(self): 
        super().__init__()

        # paramétrage de la fenêtre
        self.setWindowTitle(GestionPage.TITRE_FENETRE)
        self.resize(900, 600)
        
        # ===== MENU =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        
        self.__help = self.__menuBar.addMenu('&Apropos')
        self.__seetings = self.__menuBar.addMenu('&Parametres')

        # ===== ACTIONS =====
        self.__action_apropos = QAction(QIcon('actions/stock_search.png'), 'A propos', self)
        self.__action_add_line = QAction(QIcon('actions/list-add.png'), 'Ajouter une ligne', self)
        self.__action_save = QAction(QIcon('actions/document-save.png'), 'Enregistrer les modifications', self)
       
        
        self.__help.addAction(self.__action_apropos)
        self.__seetings.addAction(self.__action_add_line)
        self.__seetings.addAction(self.__action_save)
        
        # ===== CONNEXION AUX FONCTIONS =====
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
       
        
        self.__titre= QLabel("Profil: Gestionnaire")
        self.__Deconnecter=QPushButton("Déconnexion")
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        self.__Deconnecter.clicked.connect(self.deconnecter)
        
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white;")
        
        # ===== BLOC CONTENEUR DU TABLEAU =====
        self.__bloc_tableau_conteneur = QWidget()
        self.__bloc_tableau_conteneur_lay = QHBoxLayout()
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

        self.load_table_from_db()
       
    # ================== FONCTIONS ==================
    
   
    def load_table_from_db(self):
       try:
          conn = connexion()
          cur = conn.cursor()
          cur.execute("SELECT date, heure, de, a, descriptif FROM donnees;")
          rows = cur.fetchall()

          self.__bloc_tableau.setRowCount(0)
          for row_data in rows:
              row = self.__bloc_tableau.rowCount()
              self.__bloc_tableau.insertRow(row)
              for col, value in enumerate(row_data):
                  self.__bloc_tableau.setItem(row, col, QTableWidgetItem(str(value)))
       except:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les données : ")
       finally:
         cur.close()
         conn.close() 


    def a_propos(self):       
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunication promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')
    
    def  add_line(self):
        self.__row = self.__bloc_tableau.rowCount()
        self.__bloc_tableau.insertRow(self.__row)
        
        self.__now = datetime.now()
        self.__bloc_tableau.setItem(self.__row, 0, QTableWidgetItem(self.__now.strftime("%Y-%m-%d")))
        self.__bloc_tableau.setItem(self.__row, 1, QTableWidgetItem(self.__now.strftime("%H:%M:%S")))

        
    def save_modif(self):
      try:
        conn = connexion()
        cur = conn.cursor()
        for row in range(self.__bloc_tableau.rowCount()):
          
            date = self.__bloc_tableau.item(row, 0).text() if self.__bloc_tableau.item(row, 0) else ""
            heure = self.__bloc_tableau.item(row, 1).text() if self.__bloc_tableau.item(row, 1) else ""
            de = self.__bloc_tableau.item(row, 2).text() if self.__bloc_tableau.item(row, 2) else ""
            a = self.__bloc_tableau.item(row, 3).text() if self.__bloc_tableau.item(row, 3) else ""
            description = self.__bloc_tableau.item(row, 4).text() if self.__bloc_tableau.item(row, 4) else ""

            cur.execute("""
                INSERT INTO donnees (date, heure, de, a, descriptif)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE
                SET date=EXCLUDED.date, heure=EXCLUDED.heure,
                    de=EXCLUDED.de, a=EXCLUDED.a, descriptif=EXCLUDED.descriptif;
            """, (date, heure, de, a, description))
        
        conn.commit()
        QMessageBox.information(self, "Enregistrement", "Les modifications ont été enregistrées")
      except:
        QMessageBox.critical(self, "Erreur", "Impossible de sauvegarder")
      finally:
        cur.close()
        conn.close()

        
    def deconnecter(self): 
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
    window = GestionPage()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
