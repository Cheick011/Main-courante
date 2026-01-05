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
    Classe utilitaire pour l'envoi de messages en multicast.

    Cette classe fournit des méthodes statiques permettant
    d'envoyer différents types de messages (mise à jour,
    synchronisation complète) à l'ensemble des nœuds du réseau.
    """

    def __init__(self):
        """
        Initialise l'émetteur multicast.

        Aucun état interne n'est conservé, les méthodes sont
        principalement utilisées de manière statique.
        """
        super().__init__()
        

    @staticmethod
    def send_message(msg_dict):
       """
        Envoie un message multicast brut.

        :param msg_dict: Message à envoyer sous forme de dictionnaire.
        :type msg_dict: dict
        """
        data = json.dumps(msg_dict).encode()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        sock.sendto(data, (MULTICAST_GRP, PORT))

    @staticmethod
    def send_update(action, table, payload):
       """
        Envoie une mise à jour de données aux autres nœuds.

        :param action: Type d'action (``INSERT``, ``UPDATE``, ``DELETE``).
        :type action: str
        :param table: Nom de la table concernée.
        :type table: str
        :param payload: Données associées à la mise à jour.
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
        Envoie une requête de synchronisation complète.

        Cette requête demande aux autres nœuds du réseau
        d'envoyer l'intégralité de leurs données.
        """
        MulticastSender.send_message({"type": "full_sync_request"})

    @staticmethod
    def send_full_sync_data(data):
       """
        Envoie les données complètes pour une synchronisation globale.

        :param data: Ensemble des données à synchroniser.
        :type data: dict
        """
        MulticastSender.send_message({
            "type": "full_sync_data",
            "payload": data
        })


class MulticastReceiver(threading.Thread):
   """
    Récepteur multicast exécuté dans un thread dédié.

    Cette classe écoute en continu les messages multicast,
    les interprète et déclenche les actions appropriées
    via le gestionnaire de synchronisation.
    """

    def __init__(self, sync_manager: SyncManager):
       """
        Initialise le récepteur multicast.

        :param sync_manager: Gestionnaire de synchronisation des données.
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
        Traite une demande de synchronisation complète.

        Récupère l'ensemble des données depuis la base de données
        locale et les diffuse aux autres nœuds via le multicast.
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
