#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: mutlicast
   :platform: Unix, windows
   :synopsis: module pour la multidiffusion des informations entre les postes, l'envoie et la reception.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""

import socket
import struct
import json
import threading

from .config import MULTICAST_GRP, PORT
from .notification import notify_system
from .Connexion_dataBase import connexion
from .synchronisation import SyncManager


class MulticastSender:
   """
   Utility class for sending multicast messages.

   This class provides static methods to send different types of messages
   (update notifications, full synchronization requests)
   to all nodes on the network.
   """


    def __init__(self):
       """
       Initializes the multicast sender.
       No internal state is maintained; the methods are primarily
       used in a static manner.
       """
       super().__init__()
        

    @staticmethod
    def send_message(msg_dict):
       """
       Sends a raw multicast message.
       :param msg_dict: Message to send as a dictionary.
       :type msg_dict: dict
       """
       data = json.dumps(msg_dict).encode()
       sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
       sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
       sock.sendto(data, (MULTICAST_GRP, PORT))

    @staticmethod
    def send_update(action, table, payload):
       """
       Sends a data update to the other nodes.
       :param action: Type of action (``INSERT``, ``UPDATE``, ``DELETE``).
       :type action: str
       :param table: Name of the affected table.
       :type table: str
       :param payload: Data associated with the update.
       :type payload: dict
       """
       MulticastSender.send_message({
            "type": "update",
            "action": action,
            "table": table,
            "payload": payload
        })

    @staticmethod
    def request_full_sync():
       """
       Sends a full synchronization request.
       
       This request asks other nodes in the network
       to send all of their data.
       """
       MulticastSender.send_message({"type": "full_sync_request"})

    @staticmethod
    def send_full_sync_data(data):
       """
       Sends the complete data for a full synchronization.
       :param data: The set of data to synchronize.
       :type data: dict
       """
       MulticastSender.send_message({
            "type": "full_sync_data",
            "payload": data
        })


class MulticastReceiver(threading.Thread):
      """
      Multicast receiver running in a dedicated thread.
      This class continuously listens for multicast messages,
      processes them, and triggers the appropriate actions
      via the synchronization handler.
      """


    def __init__(self, sync_manager: SyncManager):
       """
       Initializes the multicast receiver.
       :param sync_manager: Data synchronization manager.
       :type sync_manager: SyncManager
       """
       super().__init__(daemon=True)
       self.sync_manager = sync_manager

    def run(self):
        """
        Lance la boucle d'écoute multicast.

        Cette méthode configure le socket UDP multicast,
        rejoint le groupe multicast et traite les messages reçus
        indéfiniment.
        """
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
       
       """
       Starts the multicast listening loop.
       This method sets up the UDP multicast socket,
       joins the multicast group, and processes incoming
       messages indefinitely.
       """
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
