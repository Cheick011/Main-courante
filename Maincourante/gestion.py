
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version Nov 12 09:51:19 2025

@author: adja

"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy
from PyQt5.QtGui import QIcon, QKeySequence

class GestionPage(QMainWindow):
    TITRE_FENETRE = "Main courante"
  
    def __init__(self): 
        super().__init__()

        # paramétrage de la fenêtre
        self.setWindowTitle(GestionPage.TITRE_FENETRE)
        self.resize(900, 600)
        
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
        self.__spéléologues=QLabel("Page gestionnaire")
        self.__Déconnecter=QPushButton("Déconnecter")
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__spéléologues)
        self.__bloc_haut_lay.addWidget(self.__Déconnecter)
        
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
        
        self.__bloc_bas = QGroupBox() 
        self.__bloc_bas_lay = QHBoxLayout()
        self.__bloc_bas.setLayout(self.__bloc_bas_lay)    
        self.__bloc_général_lay.addWidget(self.__bloc_bas) 
       
        self.__copyright= QLabel("Copyright BUT2 R&T")
        
        self.__bloc_bas_lay.addStretch()
        self.__bloc_bas_lay.addWidget(self.__copyright)
        self.__bloc_bas_lay.addStretch()

def main():
    application = QApplication(sys.argv)
    window = GestionPage()
    window.show()
    sys.exit(application.exec_())

if __name__ == '__main__':
    main()
