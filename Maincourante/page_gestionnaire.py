#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version Nov 12 09:51:19 2025

@author: adja

"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView
from PyQt5.QtGui import QIcon, QKeySequence

class GestionPage(QMainWindow):
    TITRE_FENETRE = "Page gestionnaire"
    TOOLTIP_BOUTON_DEC = "Déconnecter vous de votre session"
    TOOLTIP_BOUTON_AC = "Accéder aux dernières mises à jour" 
  
    def __init__(self): 
        super().__init__()

        # paramétrage de la fenêtre
        self.setWindowTitle(GestionPage.TITRE_FENETRE)
        self.resize(900, 600)
        
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        
        self.__help = self.__menuBar.addMenu('&Apropos')
        self.__seetings = self.__menuBar.addMenu('&Parametres')
        
        
        
        self.__action_apropos = QAction(QIcon('actions/stock_search.png'), 'A propos', self)
        self.__action_add_line = QAction(QIcon('actions/list-add.png'), 'Ajouter une ligne', self)
        self.__action_save = QAction(QIcon('actions/document-save.png'), 'Enregistrer les modifications', self)
       
        
        self.__help.addAction(self.__action_apropos)
        self.__seetings.addAction(self.__action_add_line)
        self.__seetings.addAction(self.__action_save)
        
        
        self.__action_apropos.triggered.connect(self.a_propos)
        self.__action_apropos.triggered.connect(self.add_line)
        self.__action_apropos.triggered.connect(self.save_modif)
        
        #creation  bloc général
        self.__bloc_general = QWidget() 
        self.__bloc_general_lay = QVBoxLayout()
        self.__bloc_general.setLayout(self.__bloc_general_lay)
        self.setCentralWidget(self.__bloc_general)
        
        #creation bloc haut
        
        self.__bloc_haut = QGroupBox() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_haut) 
       
        
        self.__titre= QLabel("Profil: Gestionnaire")
        self.__Actualiser=QPushButton("Actualiser")
        self.__Deconnecter=QPushButton("Déconnecter")
        
        self.__Deconnecter.setToolTip(GestionPage.TOOLTIP_BOUTON_DEC)
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        

        self.__Actualiser.setToolTip(GestionPage.TOOLTIP_BOUTON_AC)
        self.__Actualiser.setStyleSheet("background-color: violet; color: white")
        self.__Actualiser.setFixedSize(120, 30)
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__Actualiser)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white;")
        
        # création d’un bloc pour centrer le tableau
        self.__bloc_tableau_conteneur = QWidget()
        self.__bloc_tableau_conteneur_lay = QHBoxLayout()
        self.__bloc_tableau_conteneur.setLayout(self.__bloc_tableau_conteneur_lay)

        self.__bloc_general_lay.addWidget(self.__bloc_tableau_conteneur)
         

        # le tableau
        self.__bloc_tableau = QTableWidget() #TableWidget n’est pas censé recevoir un layout, ce n’est pas un conteneur.
       
       
        self.__row =  self.__bloc_tableau.rowCount()
        self.__bloc_tableau.insertRow(self.__row)
        self.__bloc_tableau.setColumnCount(5)
        self.__bloc_tableau.setHorizontalHeaderLabels(["Date", "Heure", "De", "À", "Description"])
        self.__bloc_tableau.verticalHeader().setVisible(False)
        
        #self.__bloc_tableau.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.__bloc_tableau.setItem(self.__row, 0, QTableWidgetItem("12/11/2025"))
        self.__bloc_tableau.setItem(self.__row, 1, QTableWidgetItem("08:05"))
        self.__bloc_tableau.setItem(self.__row, 2, QTableWidgetItem(""))
        self.__bloc_tableau.setItem(self.__row, 3, QTableWidgetItem(""))
        self.__bloc_tableau.setItem(self.__row, 4, QTableWidgetItem("Début des opérations"))
        
        self.__bloc_tableau.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.__bloc_tableau.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__bloc_tableau.horizontalHeader().setStretchLastSection(True) 
        self.__bloc_tableau_conteneur_lay.addWidget(self.__bloc_tableau)

       

    def a_propos(self):       
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI RT promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')
    
    def  add_line(self):
        pass
    def save_modif(self):
        pass
    
    def deconnecter(self):
        
        #creer un message de confirmation pour la deconnexion
        reply = QMessageBox.question(self, 'Déconnexion','Voulez-vous vraiment vous déconnecter?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
        #Si l'utilisateur confirme,ferme la fenetre
            self.close()
     

def main():
    application = QApplication(sys.argv)
    window = GestionPage()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
