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
    Displays a system notification with a title and message.

    This function adapts the notification mechanism depending
    on the detected operating system:

    - **Linux**: uses ``notify-send`` and ``paplay``
    - **Windows**: uses ``win10toast`` and ``winsound``
    - **Other systems**: prints to the standard output

    :param title: Notification title.
    :type title: str
    :param message: Content of the message to display.
    :type message: str
    :raises Exception: Any exception raised while sending the notification
                       is caught and printed to the console.
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
