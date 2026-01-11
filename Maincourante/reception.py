#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: reception
   :platform: Unix, Windows
   :synopsis:

UDP network receiver module.

This module defines the Reception class, responsible for listening to
incoming UDP messages from peer machines, applying database updates,
handling full synchronization responses, and notifying the GUI when
data changes.

Compatible with Linux and Windows.
"""
import socket
import json
import threading
from PyQt5.QtCore import QObject, pyqtSignal

from Connexion_dataBase import connexion
from notification import notif_system
from config import PORT
from envoie import Envoie


class Reception(QObject):
    """
    UDP receiver running in a background thread.
    """

    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        self.thread.start()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", PORT))

        print(f"[NETWORK] Listening on port {PORT}")

        while True:
            data, _ = sock.recvfrom(8192)

            try:
                msg = json.loads(data.decode())
            except Exception:
                continue

            notif_system(
                "Network update",
                f"{msg['type']} / {msg['action']}"
            )

            self.apply(msg)

    def apply(self, msg: dict):
        msg_type = msg["type"]
        action = msg["action"]
        payload = msg["payload"]

        # ---------- FULL SYNC REQUEST ----------
        if msg_type == "sync" and action == "REQUEST":
            from synchronisation import Synchro
            s = Synchro()
            data = s.export_database()
            Envoie.send("sync", "RESPONSE", data)
            return

        # ---------- PARTIAL UPDATE ----------
        conn = connexion()
        cur = conn.cursor()

        try:
            if msg_type == "donnee":

                if action == "INSERT":
                    cur.execute("""
                        INSERT INTO donnees (date, heure, de, a, descriptif)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (
                        payload["date"],
                        payload["heure"],
                        payload["de"],
                        payload["a"],
                        payload["descriptif"]
                    ))

                elif action == "UPDATE":
                    cur.execute("""
                        UPDATE donnees
                        SET date=%s, heure=%s, de=%s, a=%s, descriptif=%s
                        WHERE id=%s
                    """, (
                        payload["date"],
                        payload["heure"],
                        payload["de"],
                        payload["a"],
                        payload["descriptif"],
                        payload["id"]
                    ))

                elif action == "DELETE":
                    cur.execute(
                        "DELETE FROM donnees WHERE id=%s",
                        (payload["id"],)
                    )

            conn.commit()
            self.data_changed.emit()

        except Exception as e:
            conn.rollback()
            print("[RECEPTION] Error:", e)

        finally:
            cur.close()
            conn.close()
        
