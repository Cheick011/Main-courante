# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QComboBox
from PyQt5.QtGui import QIcon, QKeySequence

   # def __init__(self):
    #    super().__init__()
      #  self.setWindowTitle("Page Admin")
     #   self.setGeometry(300, 300, 400, 200)
       # layout = QVBoxLayout()
     #   layout.addWidget(QLabel("Bienvenue Admin !"))
      #  self.setLayout(layout)
class AdminPage(QMainWindow):
    TITRE_FENETRE = "Page administrateur"
    TOOLTIP_BOUTON_DEC = "Déconnecter vous de votre session"
    TOOLTIP_BOUTON_GES = "Accéder à la page gestionnaire"
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Page Admin")
        self.resize(900, 600)
         
        #Definition barre de menu
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        
        self.__help = self.__menuBar.addMenu('&Apropos')
        
        #création des actions  
        self.__action_apropos = QAction(QIcon('actions/stock_search.png'),'A propos', self)

        
        self.__help.addAction(self.__action_apropos)
        
        self.__action_apropos.triggered.connect(self.a_propos)
        
        #création du bloc général
        
        self.__bloc_general = QWidget() 
        self.__bloc_general_lay = QVBoxLayout()
        self.__bloc_general.setLayout(self.__bloc_general_lay)
        self.setCentralWidget(self.__bloc_general)
        
        self.__bloc_haut = QWidget() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_haut)
        self.__bloc_haut.setFixedHeight(50)

       
        self.__titre= QLabel("Profil: Administrateur")
        
        self.__gestion=QPushButton("Page Gestion")
        self.__gestion.setToolTip(AdminPage.TOOLTIP_BOUTON_GES)
        self.__gestion.setStyleSheet("background-color: violet; color: white")
        self.__gestion.setFixedSize(120, 30)
        
        self.__Deconnecter=QPushButton("Déconnexion")
        self.__Deconnecter.setToolTip(AdminPage.TOOLTIP_BOUTON_DEC)
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__gestion)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white")
        
        self.__bloc_create_users = QGroupBox("Création des comptes utilisateurs") 
        self.__bloc_create_users_lay = QFormLayout()
        self.__bloc_create_users.setLayout(self.__bloc_create_users_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_create_users)
        
        
        
        self.__lineedit_nom = QLineEdit()
        self.__lineedit_mdp = QLineEdit()
       
        
        self.__label_nom = QLabel("Nom d'utilisateur")
        self.__label_mdp = QLabel("Mot de passe")
       
        self.__bloc_create_users_lay.addRow(self.__label_nom, self.__lineedit_nom)
        self.__bloc_create_users_lay.addRow(self.__label_mdp, self.__lineedit_mdp)
       
        self.__create_user=QPushButton("Créer l'utilisateur")
        self.__bloc_create_users_lay.addWidget(self.__create_user)
        self.__create_user.clicked.connect(self.creer_utilisateur)
        #self.__create_user.setStyleSheet("background-color: #1E3A5F; color: white")
        
        #Création des listes d'utilisateurs
        
        self.__bloc_gestion_droits = QGroupBox("Gestion des droits d'utilisateurs") 
        self.__bloc_gestion_droits_lay = QVBoxLayout()
        self.__bloc_gestion_droits.setLayout(self.__bloc_gestion_droits_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_gestion_droits)
        
        #user adja
        self.__user_adja = QWidget()
        self.__user_adja_lay = QHBoxLayout()
        self.__user_adja.setLayout(self.__user_adja_lay)
        self.__bloc_gestion_droits_lay.addWidget(self.__user_adja)
        
        self.__label_adja = QLabel("Adja")
        self.__combobox_adja= QComboBox()
        self.__combobox_adja.addItems(["lecture", "gestion", "admin" ])
       
        self.__bouton_supp_adja= QPushButton()
        self.__bouton_supp_adja.setIcon(QIcon("actions/Capture d’écran 2026-01-01 à 16.08.03.png"))
        self.__bouton_supp_adja.setFixedSize(30, 30)
        self.__bouton_supp_adja.setToolTip("Supprimer cet utilisateur")
        self.__bouton_supp_adja.setStyleSheet("background-color: transparent")
        
        self.__user_adja_lay.addWidget(self.__label_adja)
        self.__user_adja_lay.addWidget(self.__combobox_adja)
        self.__user_adja_lay.addWidget(self.__bouton_supp_adja)
        
        #user cheikh
        self.__user_cheikh = QWidget()
        self.__user_cheikh_lay = QHBoxLayout()
        self.__user_cheikh.setLayout(self.__user_cheikh_lay)
        self.__bloc_gestion_droits_lay.addWidget(self.__user_cheikh)
        
        self.__label_cheikh = QLabel("Cheikh")
        self.__combobox_cheikh= QComboBox()
        self.__combobox_cheikh.addItems(["lecture", "gestion", "admin" ])
        
        self.__bouton_supp_cheikh= QPushButton()
        self.__bouton_supp_cheikh.setFixedSize(30, 30)
        self.__bouton_supp_cheikh.setIcon(QIcon("actions/Capture d’écran 2026-01-01 à 16.08.03.png"))
        self.__bouton_supp_cheikh.setToolTip("Supprimer cet utilisateur")
        self.__bouton_supp_cheikh.setStyleSheet("background-color: transparent")
        
        
        self.__user_cheikh_lay.addWidget(self.__label_cheikh)
        self.__user_cheikh_lay.addWidget(self.__combobox_cheikh)
        self.__user_cheikh_lay.addWidget(self.__bouton_supp_cheikh)
        
        #user gatlin
        self.__user_gatlin = QWidget()
        self.__user_gatlin_lay = QHBoxLayout()
        self.__user_gatlin.setLayout(self.__user_gatlin_lay)
        self.__bloc_gestion_droits_lay.addWidget(self.__user_gatlin)
        
        self.__label_gatlin = QLabel("Gatlin")
        self.__combobox_gatlin= QComboBox()
        self.__combobox_gatlin.addItems(["lecture", "gestion", "admin" ])
        
        self.__bouton_supp_gatlin= QPushButton()
        self.__bouton_supp_gatlin.setFixedSize(30, 30)
        self.__bouton_supp_gatlin.setIcon(QIcon("actions/Capture d’écran 2026-01-01 à 16.08.03.png"))
        self.__bouton_supp_gatlin.setToolTip("Supprimer cet utilisateur")
        self.__bouton_supp_gatlin.setStyleSheet("background-color: transparent")
        
        self.__user_gatlin_lay.addWidget(self.__label_gatlin)
        self.__user_gatlin_lay.addWidget(self.__combobox_gatlin)
        self.__user_gatlin_lay.addWidget(self.__bouton_supp_gatlin)
        
        
        self.__valider=QPushButton("Valider")
        self.__bloc_general_lay.addWidget(self.__valider)
        self.__valider.setFixedSize(120, 30)
        self.__valider.setStyleSheet("background-color: #1E3A5F; color: white")
        
        # Boutons du haut
        self.__Deconnecter.clicked.connect(self.deconnexion)
        self.__gestion.clicked.connect(self.bouton_gestion)
        
        # Création utilisateur
        
        
        # Suppression utilisateurs
        self.__bouton_supp_adja.clicked.connect(self.supp_adja)
        self.__bouton_supp_cheikh.clicked.connect(self.supp_cheikh)
        self.__bouton_supp_gatlin.clicked.connect(self.supp_gatlin)
        
        # Validation des droits
        self.__valider.clicked.connect(self.valider)
        
    def valider(self):
        droits = {
            "Adja": self.__combobox_adja.currentText(),
            "Cheikh": self.__combobox_cheikh.currentText(),
            "Gatlin": self.__combobox_gatlin.currentText()
        }

        message = "Droits mis à jour :\n"
        for user, droit in droits.items():
            message += f"- {user} : {droit}\n"

        QMessageBox.information(self, "Validation", message)
        
    
   


    def supp_adja(self):
        rep = QMessageBox.question(
            self,
            "Suppression",
            "Voulez-vous vraiment supprimer l'utilisateur Adja ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self.__user_adja.hide()
            QMessageBox.information(self, "Suppression", "Utilisateur Adja supprimé")


    def supp_cheikh(self):
        rep = QMessageBox.question(
            self,
            "Suppression",
            "Voulez-vous vraiment supprimer l'utilisateur Cheikh ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self.__user_cheikh.hide()
            QMessageBox.information(self, "Suppression", "Utilisateur Cheikh supprimé")


    def supp_gatlin(self):
        rep = QMessageBox.question(
            self,
            "Suppression",
            "Voulez-vous vraiment supprimer l'utilisateur Gatlin ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self.__user_gatlin.hide()
            QMessageBox.information(self, "Suppression", "Utilisateur Gatlin supprimé")
    

    def deconnexion(self):
        rep = QMessageBox.question(
            self,
            "Déconnexion",
            "Voulez-vous vous déconnecter ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if rep == QMessageBox.Yes:
            self.close()
        
    def bouton_gestion(self):
        from gestionnairepy import GestionPage  # import ici pour éviter les imports circulaires
        self.page_gestion = GestionPage()
        self.page_gestion.show()
        self.close()  # ferme AdminPage

    
    def creer_utilisateur(self):
        nom = self.__lineedit_nom.text()
        mdp = self.__lineedit_mdp.text()
    
        if not nom or not mdp:
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez remplir tous les champs"
            )
            return
    
        QMessageBox.information(
            self,
            "Création utilisateur",
            f"L'utilisateur '{nom}' a été créé avec succès"
        )
    
        self.__lineedit_nom.clear()
        self.__lineedit_mdp.clear()
            
     
    def a_propos(self):          
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI RT promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())