

import socket
import json
import threading
from Connexion_dataBase import connexion
from notification import notif_system
from config import PORT



class Reception(threading.Thread):
    """
    UDP network receiver running in a separate daemon thread.

    This class listens on a predefined UDP port (PORT) and processes
    incoming JSON messages from peers. When a message is received, it:

    1. Decodes the JSON payload.
    2. Displays a system notification with the message type and action.
    3. Applies the changes to the local database according to the message content.

    Supported message types:
    - "utilisateur": updates the users table (INSERT, UPDATE, DELETE).
    - "donnee": updates the data table (INSERT, UPDATE, DELETE).

    Attributes:
        PORT (int): UDP port to listen on (default 55300).

    """


    def __init__(self):

        """
        Initializes the Reception thread as a daemon.
        """
        super().__init__(daemon=True)

    def run(self):
        """
        Main loop of the thread that listens on the UDP port.

        Receives incoming messages, decodes the JSON data, displays
        a system notification, and applies the message to the database.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", PORT))

        print("Écoute réseau démarrée")

        while True:
            data, addr = sock.recvfrom(8192)
            msg = json.loads(data.decode())
            print("Message reçu :", msg)

            notif_system(
                "Message reçu",
                f"{msg['type']} / {msg['action']}"
            )

            self.apply(msg)

    def appliquer(self, msg):
        """
        Apply a received message to the local database.

        Args:
            msg (dict): A dictionary containing the message type, action, and payload.

        Supported types:
            - "utilisateur": updates the users table (INSERT, UPDATE, DELETE)
            - "donnee": updates the data table (INSERT, UPDATE, DELETE)

        Exceptions:
            Any database exceptions are caught and printed.
        """

        conn = connexion()
        cur = conn.cursor()

        try:
            if msg["type"] == "utilisateur":
                p = msg["payload"]

                if msg["action"] in ("INSERT", "UPDATE"):
                    cur.execute("""
                        INSERT INTO utilisateurs (nom_utilisateur, mot_de_passe, role)
                        VALUES (%s,%s,%s)
                        ON CONFLICT (nom_utilisateur)
                        DO UPDATE SET mot_de_passe=%s, role=%s
                    """, (
                        p["nom"], p["mdp"], p["role"],
                        p["mdp"], p["role"]
                    ))

                elif msg["action"] == "DELETE":
                    cur.execute(
                        "DELETE FROM utilisateurs WHERE nom_utilisateur=%s",
                        (p["nom"],)
                    )

            elif msg["type"] == "donnee":
                p = msg["payload"]

                if msg["action"] == "INSERT":
                    cur.execute("""
                        INSERT INTO donnees (date, heure, de, a, descriptif)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (
                        p["date"], p["heure"], p["de"],
                        p["a"], p["descriptif"]
                    ))

                elif msg["action"] == "UPDATE":
                    cur.execute("""
                        UPDATE donnees
                        SET date=%s, heure=%s, de=%s, a=%s, descriptif=%s
                        WHERE id=%s
                    """, (
                        p["date"], p["heure"], p["de"],
                        p["a"], p["descriptif"], p["id"]
                    ))

                elif msg["action"] == "DELETE":
                    cur.execute(
                        "DELETE FROM donnees WHERE id=%s",
                        (p["id"],)
                    )

            conn.commit()

        except Exception as e:
            print("Erreur sync réseau :", e)

        cur.close()
        conn.close()




