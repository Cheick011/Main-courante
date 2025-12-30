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
