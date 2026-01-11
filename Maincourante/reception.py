#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: reception
   :platform: Unix, Windows
   :synopsis: UDP network receiver module.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitiers.fr>
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
    UDP receiver running in a background thread that listens for incoming UDP messages,
    processes them, and applies the changes to the local database. It supports both full 
    synchronization requests and partial data updates from peer machines.

    The receiver runs in a separate thread, listens for messages on a specified UDP port,
    and emits a signal when the database has been updated.

    """
    data_changed = pyqtSignal()

    def __init__(self):
        """
        Initializes the Reception object and its background thread.

        Sets up the listening thread which runs independently from the main application
        to handle incoming UDP messages.
        """
        super().__init__()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """
        Starts the background UDP listening thread.

        This method is called to initiate the listening process for incoming messages.
        The `run` method is executed in a separate thread.
        """
        self.thread.start()

    def run(self):
        """
        Main loop that listens for incoming UDP messages and processes them.

        This method listens on the predefined UDP port, decodes the incoming JSON messages, 
        and applies the changes to the database by calling the `apply` method.

        If the message type is "sync" and the action is "REQUEST", it requests a full 
        synchronization and sends the local database data to the peer. Otherwise, it processes 
        partial updates (INSERT, UPDATE, DELETE) for the "donnee" type.
        """
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

            # Notify system about the received message
            notif_system(
                "Network update",
                f"{msg['type']} / {msg['action']}"
            )

            self.apply(msg)

    def apply(self, msg: dict):
        """
        Processes the received message and applies the corresponding action to the local database.

        Depending on the type and action in the received message, this method will:
        - Handle full synchronization requests (sync)
        - Perform partial updates (INSERT, UPDATE, DELETE) for the "donnee" type.

        Args:
            msg (dict): The received message containing the type, action, and payload.

        Supported message types and actions:
            - "sync" -> "REQUEST": Initiates a full sync request. Sends a response with local database data.
            - "donnee" -> "INSERT": Inserts new data into the database.
            - "donnee" -> "UPDATE": Updates existing data in the database.
            - "donnee" -> "DELETE": Deletes data from the database.

        Returns:
            None
        """
        msg_type = msg["type"]
        action = msg["action"]
        payload = msg["payload"]

        # ---------- FULL SYNC REQUEST ----------
        if msg_type == "sync" and action == "REQUEST":
            from synchronisation import Synchro
            s = Synchro()
            data = s.export_database()  # Export local database data
            Envoie.send("sync", "RESPONSE", data)  # Send the data to the peer
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
            self.data_changed.emit()  # Emit signal that data has changed

        except Exception as e:
            conn.rollback()
            print("[RECEPTION] Error:", e)

        finally:
            cur.close()
            conn.close()
