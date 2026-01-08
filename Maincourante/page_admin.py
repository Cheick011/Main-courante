#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 13:10:13 2026

@authors: adja, Marème

"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QTextEdit,QMenuBar,QMenu,QToolBar,QWidget, QAction, QMessageBox, QLineEdit,QFormLayout,QVBoxLayout,QHBoxLayout, QPushButton, QGroupBox, QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView, QComboBox
from PyQt5.QtGui import QIcon, QKeySequence
from page_gestionnaire import GestionPage
from Connexion_dataBase import connexion


class AdminPage(QMainWindow):
    TITRE_FENETRE = "Page administrateur"

    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Page Admin")
        self.resize(900, 600)
         
        # ===== Menu =====
        self.__menuBar = QMenuBar()
        self.setMenuBar(self.__menuBar)
        self.__help = self.__menuBar.addMenu('&Apropos')
        
         # ===== Actions ===== 
        self.__action_apropos = QAction(QIcon('actions/stock_search.png'),'A propos', self)
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
   Charge tous les utilisateurs depuis la base de données
   et les affiche dans le bloc de gestion des droits.
      """
      try:
        conn = connexion()
        cur = conn.cursor()
        cur.execute("SELECT nom_utilisateur,mot_de_passe, role FROM utilisateurs;")
        rows = cur.fetchall()
        
        # Vider l'affichage actuel
        for i in reversed(range(self.__bloc_gestion_droits_lay.count())):
            widget = self.__bloc_gestion_droits_lay.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        # Ajouter tous les utilisateurs
        for nom, mdp, role in rows:
            user_widget = self.creer_widget_utilisateur(nom, mdp, role)
            self.__bloc_gestion_droits_lay.addWidget(user_widget)

      except Exception as e:
        QMessageBox.critical(self, "Erreur", f"Impossible de charger les utilisateurs : {e}")
       
      finally:
        cur.close()
        conn.close()

    def creer_utilisateur(self):
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
            except Exception as e:
              QMessageBox.critical(self, "Erreur", f"Impossible de supprimer : {e}")
            finally:
              cur.close()
              conn.close()

            widget.deleteLater()

    def valider(self):
      try:
        from Connexion_dataBase import connexion
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
                ON CONFLICT (nom_utilisateur) DO UPDATE
                SET mot_de_passe = EXCLUDED.mot_de_passe,
                    role = EXCLUDED.role;
            """, (nom, mdp, role))
        
        conn.commit()
        QMessageBox.information(self, "Validation", "Les utilisateurs ont été enregistrés avec succès.")
        
      except:
        QMessageBox.critical(self, "Erreur", "Impossible de sauvegarder les utilisateurs")
        
      finally:
        cur.close()
        conn.close()


    def bouton_gestion(self):
        self.page_gestion = GestionPage()
        self.page_gestion.show()
        self.close()

    def deconnexion(self):
        self.__rep = QMessageBox.question(
            self,
            "Déconnexion",
            "Voulez-vous vous déconnecter ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if self.__rep == QMessageBox.Yes:
            self.close()      
    
    def a_propos(self):          
      QMessageBox.information(self,'A propos','Cette application a été développé par un groupe de 4 étudiants en BUT2 FI Réseaux et Télécommunications promotion 2025-2026 dans le cadre de leur SAÉ "Développer des applications communicantes"')

# ================== MAIN ==================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AdminPage()
    window.show()
    sys.exit(app.exec_())
