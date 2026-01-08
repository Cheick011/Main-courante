#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
main.py
--------
Lance l'application de login pour la Main Courante Spéléologue.
"""

import sys
from PyQt5.QtWidgets import QApplication
from auth import LoginWindow  # Assure-toi que auth.py est dans le même dossier ou adapte le chemin

def main():
    """

    This function Launches the login application for the "Spéléologue Main Courante".

    This script initializes the PyQt5 application and opens the login window
    from the auth module. It serves as the entry point for the application.
    """

    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


