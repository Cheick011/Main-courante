import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QComboBox
from PyQt5.QtGui import QIcon, QKeySequence
from gestionnairepy import GestionPage


class AdminPage(QMainWindow):
    TITRE_FENETRE = "Page administrateur"

    
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

        #création du bloc haut
        self.__bloc_haut = QWidget() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_haut)
        self.__bloc_haut.setFixedHeight(60)

       
        self.__titre= QLabel("Profil: Administrateur")
        
        self.__gestion=QPushButton("Page Gestion")
        self.__gestion.setToolTip(AdminPage.TOOLTIP_BOUTON_GES)
        self.__gestion.setStyleSheet("background-color: violet; color: white")
        self.__gestion.setFixedSize(120, 30)
        
        self.__Deconnecter=QPushButton("Déconnexion")
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
        #self.__create_user.setStyleSheet("background-color: #1E3A5F; color: white")
        
        
      
        
       
        
    def valider(self):
      pass
    def deconnexion(self):
      pass
    def bouton_gestion(self):
      pass
    def creer_utilisateur(self):
      pass
    def a_propos(self):          
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI RT promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
