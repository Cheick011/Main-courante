#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: notification
   :platform: Unix, Windows
   :synopsis: Module pour notifier le système lors de la réception
              de nouveaux messages réseau ou événements importants.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitiers.fr>
"""

import platform
import subprocess


def notif_system(title: str, message: str):
    """
    Displays a system notification with a title and message.

    This function detects the operating system and displays a notification accordingly:
    - On Linux: Uses `notify-send` for the notification and `paplay` for a sound (if available).
    - On Windows: Uses the `win10toast` library to show a toast notification and `winsound` for a system beep.
    - On other platforms: Displays the notification in the console.

    Args:
        title (str): The title of the notification.
        message (str): The content of the notification.

    Returns:
        None

    Raises:
        Exception: If an error occurs during notification display, an exception is caught and logged.
    """

    # Determine the platform
    os_name = platform.system().lower()

    try:
        # ===== LINUX =====
        if "linux" in os_name:
            # Use 'notify-send' to show a notification on Linux
            subprocess.Popen(
                ["notify-send", title, message],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Play a sound if available (optional)
            try:
                subprocess.Popen(
                    ["paplay", "/usr/share/sounds/freedesktop/stereo/complete.oga"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                pass  # No sound played if the sound file is not found

        # ===== WINDOWS =====
        elif "windows" in os_name:
            try:
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)
            except Exception as e:
                pass  # Skip notification if win10toast fails

            try:
                import winsound
                winsound.MessageBeep()  # Play a default system beep
            except Exception as e:
                pass  # Skip sound if winsound fails

        # ===== OTHER OS (Mac, etc.) =====
        else:
            print(f"[NOTIFICATION] {title} : {message}")

    except Exception as e:
        print("Notification Error:", e)
        print(f"[NOTIFICATION] {title} : {message}")
