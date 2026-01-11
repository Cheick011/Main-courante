

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: page_admin
   :platform: Unix, Windows
   :synopsis: Administration interface for managing user accounts in the
              SSF main log application.

This module provides the graphical administration page of the application.
It allows administrators to create, update and delete user accounts,
assign roles (reader, manager, administrator) and synchronize user data
between multiple workstations over the local network.

.. moduleauthor:: Adja Diarietou Mbengue <adja.diarietou.mbengue@etu.univ-poitiers.fr>
.. moduleauthor:: Marème Mboup <mareme.mboup@etu.univ-poitiers.fr>
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QComboBox
from PyQt5.QtGui import QIcon, QKeySequence
from page_gestionnaire import GestionPage
from Connexion_dataBase import connexion
from envoie import Envoie


class AdminPage(QMainWindow):
    """
    Main administration window.

    This class implements the graphical interface used by administrators
    to manage application user accounts, including account creation,
    role management, deletion and synchronization with other machines.
    """
   
    TITRE_FENETRE = "Page administrateur"

    def __init__(self):
        
        """
         Initializes the administrator page.
   
        This method sets up the main window, menus, graphical layouts,
        signal connections and loads existing users from the database.
        """
        super().__init__()
        
        self.setWindowTitle("Page Admin")
        self.resize(900, 600)
         
        # ===== Menu =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        self.__help = self.__menuBar.addMenu('&Apropos')
        
         # ===== Actions ===== 
        self.__action_apropos = QAction(QIcon('actions/icone_3.jpeg'),'A propos', self)
        self.__help.addAction(self.__action_apropos)
        self.__action_apropos.triggered.connect(self.a_propos)
        
        # ===== Bloc général =====
        self.__bloc_general = QWidget() 
        self.__bloc_general_lay = QVBoxLayout()
        self.__bloc_general.setLayout(self.__bloc_general_lay)
        self.setCentralWidget(self.__bloc_general)

         # ===== Haut =====
        self.__bloc_haut = QWidget() 
        self.__bloc_haut_lay = QHBoxLayout()
        self.__bloc_haut.setLayout(self.__bloc_haut_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_haut)
        self.__bloc_haut.setFixedHeight(60)
        self.__bloc_haut.setStyleSheet("background-color: #1E3A5F; color: white")

       
        self.__titre= QLabel("Profil: Administrateur")
        
        self.__gestion=QPushButton("Page Gestion")
        self.__gestion.setStyleSheet("background-color: violet; color: white")
        self.__gestion.setFixedSize(120, 30)
        
        self.__Deconnecter=QPushButton("Déconnexion")
        self.__Deconnecter.setStyleSheet("background-color: violet; color: white")
        self.__Deconnecter.setFixedSize(120, 30)
        
        self.__bloc_haut_lay.addWidget(self.__titre)
        self.__bloc_haut_lay.addWidget(self.__gestion)
        self.__bloc_haut_lay.addWidget(self.__Deconnecter)
        
        # ===== Création utilisateur =====
        self.__bloc_create_users = QGroupBox("Création des comptes utilisateurs") 
        self.__bloc_create_users_lay = QFormLayout()
        self.__bloc_create_users.setLayout(self.__bloc_create_users_lay)    
        self.__bloc_general_lay.addWidget(self.__bloc_create_users)
        
        
        self.__lineedit_nom = QLineEdit()
        self.__lineedit_mdp = QLineEdit()
        self.__lineedit_mdp.setEchoMode(QLineEdit.Password)
 
        
        self.__label_nom = QLabel("Nom d'utilisateur")
        self.__label_mdp = QLabel("Mot de passe")
       
        self.__bloc_create_users_lay.addRow(self.__label_nom, self.__lineedit_nom)
        self.__bloc_create_users_lay.addRow(self.__label_mdp, self.__lineedit_mdp)
       
        self.__create_user=QPushButton("Créer l'utilisateur")
        self.__bloc_create_users_lay.addWidget(self.__create_user)

        # ===== Gestion des droits =====
        self.__bloc_gestion_droits = QGroupBox("Gestion des comptes utilisateurs")
        self.__bloc_gestion_droits_lay = QVBoxLayout()
        self.__bloc_gestion_droits.setLayout(self.__bloc_gestion_droits_lay)
        self.__bloc_general_lay.addWidget(self.__bloc_gestion_droits)

        # ===== Bouton valider =====
        self.__valider = QPushButton("Valider")
        self.__valider.setFixedSize(120, 40)
        self.__valider.setStyleSheet("background-color: #1E3A5F; color: white")
        self.__bloc_general_lay.addWidget(self.__valider)

        # ===== Connexions =====
        self.__create_user.clicked.connect(self.creer_utilisateur)
        self.__Deconnecter.clicked.connect(self.deconnexion)
        self.__gestion.clicked.connect(self.bouton_gestion)
        self.__valider.clicked.connect(self.valider)
        
        self.load_utilisateurs_from_db()


        
    # ================== FONCTIONS ==================

    def load_utilisateurs_from_db(self):
   
      """
        Loads all users from the database.

        This method retrieves all user accounts stored in the PostgreSQL
        database and displays them in the user management section
        of the administration interface.

        :raises Exception: If a database connection or query error occurs.
      """

      try:
        conn = connexion()
        cur = conn.cursor()
        cur.execute("SELECT nom_utilisateur,mot_de_passe, role FROM utilisateurs;")
        rows = cur.fetchall()
        
        for i in reversed(range(self.__bloc_gestion_droits_lay.count())):
            widget = self.__bloc_gestion_droits_lay.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        
        for nom, mdp, role in rows:
            user_widget = self.creer_widget_utilisateur(nom, mdp, role)
            self.__bloc_gestion_droits_lay.addWidget(user_widget)

      except :
        QMessageBox.critical(self, "Erreur", "Impossible de charger les utilisateurs ")
       
      finally:
        cur.close()
        conn.close()

    def creer_utilisateur(self):
  
        """
       Creates a user entry in the administration interface.

        This method validates the username and password input fields
        and adds a new user widget to the user management area.

        :raises ValueError: If the username or password field is empty.
        """

        nom = self.__lineedit_nom.text().strip()
        mdp = self.__lineedit_mdp.text().strip()

        if nom == "" or mdp == "":
            QMessageBox.warning(
                self,
                "Erreur",
                "Veuillez remplir le nom d'utilisateur et le mot de passe"
            )
            return

        user_widget = self.creer_widget_utilisateur(nom,mdp)
        self.__bloc_gestion_droits_lay.addWidget(user_widget)

        self.__lineedit_nom.clear()
        self.__lineedit_mdp.clear()

        QMessageBox.information(
            self,
            "Utilisateur créé",
            f"L'utilisateur {nom} a été ajouté"
        )

    def creer_widget_utilisateur(self, nom, mdp, role="lecteur"):
        """
         Creates a graphical widget representing a user account.

         The widget allows the administrator to modify the user's password,
         change the assigned role and delete the account.

         :param nom: Username.
         :type nom: str
         :param mdp: User password.
         :type mdp: str
         :param role: User role (lecteur, gestionnaire, admin).
         :type role: str
         :return: Configured user widget.
         :rtype: QWidget
        """

        self.__widget = QWidget()
        self.__layout = QHBoxLayout(self.__widget)

        self.__label = QLabel(nom)
        
        self.__mdp_edit = QLineEdit()
        self.__mdp_edit.setText(mdp)
        #self.__mdp_edit.setEchoMode(QLineEdit.Password)  
    

        self.__combo = QComboBox()
        self.__combo.addItems(["lecteur", "gestionnaire", "admin"])
        self.__combo.setCurrentText(role)

        self.__bouton_suppr = QPushButton()
        self.__bouton_suppr.setIcon(QIcon("actions/bouton_supp.png"))
        self.__bouton_suppr.setFixedSize(30, 30)
        self.__bouton_suppr.setStyleSheet("background-color: transparent")
        self.__bouton_suppr.clicked.connect(
            lambda: self.supprimer(self.__widget, nom)
        )

        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__combo)
        self.__layout.addWidget(self.__bouton_suppr)
      
        
        self.__widget.nom = nom
        self.__widget.mdp_edit = self.__mdp_edit
        self.__widget.combo = self.__combo 

        return self.__widget

    def supprimer(self, widget, nom):
        """
        Deletes a user account after confirmation.

        This method displays a confirmation dialog, removes the user
        from the database and deletes the associated widget from the interface.

        :param widget: User widget to remove.
        :type widget: QWidget
        :param nom: Username to delete.
        :type nom: str
        """

        self.__reponse = QMessageBox.question(
            self,
            "Suppression",
            f"Voulez-vous vraiment supprimer l'utilisateur {nom} ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if self.__reponse == QMessageBox.Yes:
            try:
              conn = connexion()
              cur = conn.cursor()
              cur.execute("DELETE FROM utilisateurs WHERE nom_utilisateur=%s;", (nom,))
              conn.commit()
            except :
              QMessageBox.critical(self, "Erreur", "Impossible de supprimer ")
            finally:
              cur.close()
              conn.close()

            widget.deleteLater()

    def valider(self):
        
        """
        Saves and synchronizes user accounts.

        This method inserts or updates all user accounts displayed
        in the interface into the local database and sends the updates
        to other connected machines over the network.

        :raises Exception: If a database or network synchronization error occurs.
        """

        try:
            conn = connexion()
            cur = conn.cursor()

            for i in range(self.__bloc_gestion_droits_lay.count()):
                widget = self.__bloc_gestion_droits_lay.itemAt(i).widget()
                if not hasattr(widget, "nom"):
                    continue

                nom = widget.nom
                mdp = widget.mdp_edit.text()
                role = widget.combo.currentText()

                if not nom or not mdp or not role:
                    continue

                cur.execute("""
                    INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, role)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (nom_utilisateur)
                    DO UPDATE SET
                        mot_de_passe = EXCLUDED.mot_de_passe,
                        role = EXCLUDED.role;
                """, (nom, mdp, role))

                  # ================== F ==================
                Envoie.send(
                    "utilisateur",  # type
                    "UPDATE",       # action
                    {
                        "nom": nom,
                        "mdp": mdp,
                        "role": role
                    }                # payload
                )

            conn.commit()

        

            QMessageBox.information(
                self,
                "Validation",
                "Utilisateurs enregistrés et synchronisés"
            )

            self.load_utilisateurs_from_db()

        except:
            QMessageBox.critical(self, "Erreur", "Erreur sauvegarde ")

        finally:
            cur.close()
            conn.close()


    def bouton_gestion(self):
      
        """
        Opens the manager page.

        This method closes the administration page and displays
        the manager interface.
        """

        self.page_gestion = GestionPage()
        self.page_gestion.show()
        self.close()

    def deconnexion(self):

        """
         Handles administrator logout.

         A confirmation dialog is displayed before closing
         the administration window.
        """

        self.__rep = QMessageBox.question(
            self,
            "Déconnexion",
            "Voulez-vous vous déconnecter ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if self.__rep == QMessageBox.Yes:
            self.close()      
    
    def a_propos(self): 
        """
        Displays application information.

        This method shows a dialog containing general information
        about the application and its development context.
        """

        QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunications promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')

# ================== MAIN ==================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
