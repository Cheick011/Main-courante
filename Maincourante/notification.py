#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: notification
   :platform: Unix, Windows
   :synopsis: Module pour notifier le système lors de la réception
              de nouveaux messages réseau ou événements importants.
"""

import platform
import subprocess


def notif_system(title: str, message: str):
    """
    Displays a system notification with a title and message.

    - Linux   : notify-send + paplay (si disponible)
    - Windows : win10toast + beep
    - Autres  : affichage console

    :param title: Notification title
    :param message: Notification content
    """

    os_name = platform.system().lower()

    try:
        # ===== LINUX =====
        if "linux" in os_name:
            subprocess.Popen(
                ["notify-send", title, message],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Son (optionnel)
            try:
                subprocess.Popen(
                    ["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                pass

        # ===== WINDOWS =====
        elif "windows" in os_name:
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except Exception:
                pass

            try:
                import winsound
                winsound.MessageBeep()
            except Exception:
                pass

        # ===== AUTRES OS =====
        else:
            print(f"[NOTIFICATION] {title} : {message}")

    except Exception as e:
        print("Erreur notification :", e)
        print(f"[NOTIFICATION] {title} : {message}")
