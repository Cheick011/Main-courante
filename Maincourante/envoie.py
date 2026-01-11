import socket
import json
from config import PEERS, PORT


class Envoie:
    """
    UDP network sender to broadcast messages to configured peers.

    This class provides a static method to send structured JSON messages
    to all IPs defined in the PEERS configuration. Each message contains:

    """
    def __init__(self):
        """
        Initialization.
        """

    @staticmethod
    def send(msg_type: str, action: str, payload: dict):
        """
        Sends a structured JSON message to all known peers.

        Args:
            msg_type (str): The type of the message ("utilisateur" or "donnee").
            action (str): The action performed ("INSERT", "UPDATE", "DELETE").
            payload (dict): The data payload for the action.

        Exceptions:
            Any JSON encoding or network errors are caught and printed.
        """

        message = {
            "type": msg_type,
            "action": action,
            "payload": payload
        }

        try:
            data = json.dumps(message).encode("utf-8")
        except Exception as e:
            print("Erreur encodage JSON :", e)
            return

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for ip in PEERS:
            try:
                sock.sendto(data, (ip, PORT))
                print(f"Message envoyé à {ip}:{PORT}")
            except Exception as e:
                print(f"Erreur envoi vers {ip} :", e)

        sock.close()
