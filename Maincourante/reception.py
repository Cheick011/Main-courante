
import socket
import json
import threading
from PyQt5.QtCore import QObject, pyqtSignal
from Connexion_dataBase import connexion
from notification import notif_system
from config import PORT
from envoie import Envoie
from synchronisation import synchro


class Reception(QObject):
    """
    UDP network receiver running in a background thread.

    This class listens for incoming UDP messages from peer machines,
    applies database updates, handles full synchronization requests,
    and notifies the graphical interface when data changes.
    """

    data_changed = pyqtSignal()

    def __init__(self):
        """
        Initializes the Reception object and its background thread.
        """
        super().__init__()
        self.thread = threading.Thread(target=self.run, daemon=True)

    def start(self):
        """
        Starts the background UDP listening thread.
        """
        self.thread.start()

    def run(self):
        """
        Main listening loop.

        Receives UDP messages, decodes JSON content, sends notifications,
        and applies the received actions to the local database.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", PORT))

        print(" Network listening started on port", PORT)

        while True:
            data, addr = sock.recvfrom(8192)

            try:
                msg = json.loads(data.decode("utf-8"))
            except json.JSONDecodeError:
                print("Invalid JSON received")
                continue

            print(" Message received:", msg)

            notif_system(
                "Network update received",
                f"{msg.get('type')} / {msg.get('action')}"
            )

            self.apply(msg)

    def apply(self, msg: dict):
        """
        Applies a received message to the local database.

        Args:
            msg (dict): Message containing 'type', 'action', and 'payload'.
        """
        msg_type = msg.get("type")
        action = msg.get("action")
        payload = msg.get("payload", {})

        # ---------- FULL SYNC ----------
        if msg_type == "sync":
            if action == "REQUEST":
                data = self.export_database()
                Envoie.send("sync", "RESPONSE", data)

            elif action == "RESPONSE":
                s = synchro()
                s.synchro_Complete(payload)
                self.data_changed.emit()

            return

        # ---------- PARTIAL UPDATE ----------
        conn = connexion()
        cur = conn.cursor()

        try:
            if msg_type == "utilisateur":
                if action in ("INSERT", "UPDATE"):
                    cur.execute("""
                        INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, role)
                        VALUES (%s,%s,%s)
                        ON CONFLICT (nom_utilisateur)
                        DO UPDATE SET
                            mot_de_passe = EXCLUDED.mot_de_passe,
                            role = EXCLUDED.role
                    """, (
                        payload["nom"],
                        payload["mdp"],
                        payload["role"]
                    ))

                elif action == "DELETE":
                    cur.execute(
                        "DELETE FROM utilisateurs WHERE nom_utilisateur=%s",
                        (payload["nom"],)
                    )

            elif msg_type == "donnee":
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
            print("Network sync error:", e)

        finally:
            cur.close()
            conn.close()

    def export_database(self) -> dict:
        """
        Exports the full local database content.

        Returns:
            dict: Dictionary containing all users and data.
        """
        conn = connexion()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, nom_utilisateur, mot_de_passe, role, date_creation
            FROM utilisateurs
        """)
        utilisateurs = [
            {
                "id": r[0],
                "nom_utilisateur": r[1],
                "mot_de_passe": r[2],
                "role": r[3],
                "date_creation": str(r[4])
            }
            for r in cur.fetchall()
        ]

        cur.execute("""
            SELECT id, date, heure, de, a, descriptif, id_utilisateur
            FROM donnees
        """)
        donnees = [
            {
                "id": r[0],
                "date": str(r[1]),
                "heure": str(r[2]),
                "de": r[3],
                "a": r[4],
                "descriptif": r[5],
                "id_utilisateur": r[6]
            }
            for r in cur.fetchall()
        ]

        cur.close()
        conn.close()

        return {
            "utilisateurs": utilisateurs,
            "donnees": donnees
        }
