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
