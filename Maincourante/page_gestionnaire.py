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
  
    def __init__(self): 
        super().__init__()

        # paramétrage de la fenêtre
        self.setWindowTitle(MainCourante.TITRE_FENETRE)
        self.resize(900, 600)

        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        
        self.__help = self.__menuBar.addMenu('&Apropos')
        
        self.__action_apropos = QAction(QIcon('actions/stock_search.png'), 'A propos', self)
        
        self.__help.addAction(self.__action_apropos)
        
        self.__action_apropos.triggered.connect(self.a_propos)
        
        #creation  bloc général
        self.__bloc_général = QWidget() 
        self.__bloc_général_lay = QVBoxLayout()
        self.__bloc_général.setLayout(self.__bloc_général_lay)
        self.setCentralWidget(self.__bloc_général)
        
        #creation bloc haut
        
        self.__bloc_haut = QGroupBox() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_général_lay.addWidget(self.__bloc_haut) 
       
        
        self.__titre= QLabel("Application spéléo-sauvetage")
        self.__gestionnaire=QLabel("Page gestionnaire")
        self.__Déconnecter=QPushButton("Déconnexion")

        self.__Déconnecter.setToolTip(GestionPage.TOOLTIP_BOUTON_DEC)
        self.__Déconnecter.setStyleSheet("background-color: violet; color: white")
    
        
       #connexion du bouton à la fonction de deconnexion
       
        self.__Déconnecter.clicked.connect(self.deconnecter)
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__gestionnaire)
        self.__bloc_haut_lay.addWidget(self.__Déconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white;")

        
        # création d’un bloc pour centrer le tableau
        self.__bloc_tableau_conteneur = QWidget()
        self.__bloc_tableau_conteneur_lay = QHBoxLayout()
        self.__bloc_tableau_conteneur.setLayout(self.__bloc_tableau_conteneur_lay)

        self.__bloc_général_lay.addWidget(self.__bloc_tableau_conteneur)
         

        # le tableau
        self.__bloc_tableau = QTableWidget() #TableWidget n’est pas censé recevoir un layout, ce n’est pas un conteneur.
       
       
        self.__bloc_tableau.setRowCount(5)
        self.__bloc_tableau.setColumnCount(4)
        self.__bloc_tableau.setHorizontalHeaderLabels(["Heure", "De", "À", "Description"])
        self.__bloc_tableau.verticalHeader().setVisible(False)
        self.__bloc_tableau.setFixedSize(600,380)
        #self.__bloc_tableau.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # stretch permet de placer le tableu au centre, on ajoute le tableau au layout du conteneur
        self.__bloc_tableau_conteneur_lay.addStretch()
        self.__bloc_tableau_conteneur_lay.addWidget(self.__bloc_tableau)
        self.__bloc_tableau_conteneur_lay.addStretch()
    
    def deconnecter(self):
        
        #creer un message de confirmation pour la deconnexion
        reply = QMessageBox.question(self, 'Déconnexion','Voulez-vous vraiment vous déconnecter?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
        #Si l'utilisateur confirme,ferme la fenetre
            self.close()
     def a_propos(self):
            
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI RT promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')
    

def main():
    application = QApplication(sys.argv)
    window = GestionPage()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
