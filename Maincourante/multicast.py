import socket
import struct
import json
import threading

from .config import MULTICAST_GRP, PORT
from .notification import notify_system
from .Connexion_dataBase import connexion
from .synchronisation import SyncManager


class MulticastSender:

    def __init__(self):
        super().__init__()
        

    @staticmethod
    def send_message(msg_dict):
        data = json.dumps(msg_dict).encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(data, (MULTICAST_GRP, PORT))

    @staticmethod
    def send_update(action, table, payload):
        MulticastSender.send_message({
            "type": "update",
            "action": action,
            "table": table,
            "payload": payload
        })

    @staticmethod
    def request_full_sync():
        MulticastSender.send_message({"type": "full_sync_request"})

    @staticmethod
    def send_full_sync_data(data):
        MulticastSender.send_message({
            "type": "full_sync_data",
            "payload": data
        })


class MulticastReceiver(threading.Thread):

    def __init__(self, sync_manager: SyncManager):
        super().__init__(daemon=True)
        self.sync_manager = sync_manager

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", PORT))

        mreq = struct.pack("4sl", socket.inet_aton(MULTICAST_GRP), socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        print(" En écoute multicast…")

        while True:
            data, _ = sock.recvfrom(8192)
            msg = json.loads(data.decode())

            print(" Message reçu :", msg)
            notify_system("Nouvelle information reçue", str(msg))

            if msg["type"] == "update":
                self.sync_manager.apply_update(msg)

            elif msg["type"] == "full_sync_data":
                self.sync_manager.apply_full_sync(msg["payload"])

            elif msg["type"] == "full_sync_request":
                self.handle_full_sync_request()

    def handle_full_sync_request(self):
        conn = connexion()
        cur = conn.cursor()

        cur.execute("SELECT * FROM utilisateurs ORDER BY id;")
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

        cur.execute("SELECT * FROM donnees ORDER BY id;")
        donnees = [
            {
                "id": r[0],
                "heure": str(r[1]),
                "de": r[2],
                "a": r[3],
                "descriptif": r[4],
                "date": str(r[5]),
                "id_utilisateur": r[6]
            }
            for r in cur.fetchall()
        ]

        cur.close()
        conn.close()

        MulticastSender.send_full_sync_data({
            "utilisateurs": utilisateurs,
            "donnees": donnees
        })
