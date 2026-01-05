#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: notification
   :platform: Unix, windows
   :synopsis: module pour notifier le poste à la reception de nouveau message.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""

import platform
import subprocess

def notify_system(title, message):
    
    """ 
    Affiche une notification système avec un titre et un message.

    Cette fonction adapte le mécanisme de notification en fonction
    du système d'exploitation détecté :

    - **Linux** : utilisation de ``notify-send`` et ``paplay``
    - **Windows** : utilisation de ``win10toast`` et ``winsound``
    - **Autres systèmes** : affichage dans la sortie standard

    :param title: Titre de la notification.
    :type title: str
    :param message: Contenu du message à afficher.
    :type message: str
    :raises Exception: Toute exception levée lors de l'envoi de la notification
                       est interceptée et affichée dans la console.
    """
    os_name = platform.system().lower()

    try:
        if "linux" in os_name:
            subprocess.Popen(["notify-send", title, message])
            subprocess.Popen(["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"])

        elif "windows" in os_name:
            from win10toast import ToastNotifier
            toaster = ToastNotifier()
            toaster.show_toast(title, message, duration=5)

            import winsound
            winsound.MessageBeep()

        else:
            print(f"[NOTIF] {title} : {message}")

    except Exception as e:
        print("Erreur notification :", e)
        print(f"[NOTIF] {title} : {message}")
