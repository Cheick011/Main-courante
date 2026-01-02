import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication

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
    TOOLTIP_BOUTON_GES = "Accéder à la page gestionnaires"
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Page Admin")
        self.resize(900, 600)
        
        self.__bloc_general = QWidget() 
        self.__bloc_general_lay = QVBoxLayout()
        self.__bloc_general.setLayout(self.__bloc_general_lay)
        self.setCentralWidget(self.__bloc_general)
        
        self.__bloc_haut = QGroupBox() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_haut) 
       
        self.__titre= QLabel("Profil: Administrateur")
        
        self.__gestion=QPushButton("Page Gestion")
        self.__gestion.setToolTip(AdminPage.TOOLTIP_BOUTON_GES)
        self.__gestion.setStyleSheet("background-color: violet; color: white")
        #self.__gestion.setFixedSize(120, 30)
        
        self.__Deconnecter=QPushButton("Déconnexion")
        self.__Deconnecter.setToolTip(AdminPage.TOOLTIP_BOUTON_DEC)
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        #self.__Deconnecter.setFixedSize(120, 30)
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        self.__bloc_haut_lay.addWidget(self.__gestion)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white")
        
        self.__bloc_create_users = QGroupBox("Création des compte utilisateurs") 
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
       
        self.__bloc_gestion_droits = QGroupBox("Gestion des droits d'utilisateurs") 
        self.__bloc_gestion_droits_lay = QFormLayout()
        self.__bloc_gestion_droits.setLayout(self.__bloc_gestion_droits_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_gestion_droits)
        
        self.__label_adja = QLabel("Adja")
        self.__label_cheikh = QLabel("Cheikh")
        
        self.__combobox_adja= QComboBox()
        self.__combobox_adja.addItems(["lecture", "gestion", "admin" ])
        self.__combobox_cheikh= QComboBox()
        self.__combobox_cheikh.addItems(["lecture", "gestion", "admin" ])
        
        self.__bloc_gestion_droits_lay.addRow(self.__label_adja, self.__combobox_adja)
        self.__bloc_gestion_droits_lay.addRow(self.__label_cheikh, self.__combobox_cheikh)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
