#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: communication
   :platform: Unix, windows
   :synopsis: module pour manager la communication avec les autres machines du réseau multicast

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""

from .synchronisation import SyncManager
from .multicast import MulticastReceiver, MulticastSender


class CommunicationModule:
    """
    Module de communication réseau basé sur le multicast.

    Cette classe centralise la gestion des communications réseau,
    incluant la réception des messages multicast, l'envoi de mises
    à jour et les demandes de synchronisation complète.
    """

    def __init__(self):
        """
        Initialise le module de communication.

        Crée une instance de gestion de synchronisation ainsi qu’un
        récepteur multicast chargé de traiter les messages entrants.
        """
        self.sync = SyncManager()
        self.receiver = MulticastReceiver(self.sync)

    def start(self):
        """
        Démarre le module de communication.

        Lance le récepteur multicast afin de commencer l’écoute
        des messages entrants sur le réseau.
        """
        self.receiver.start()
        print(" Module de communication démarré")

    def send_update(self, action, table, payload):
        """
        Envoie une mise à jour via le réseau multicast.

        :param action: Type d'action à effectuer (ex. ``INSERT``, ``UPDATE``, ``DELETE``).
        :type action: str
        :param table: Nom de la table concernée par la mise à jour.
        :type table: str
        :param payload: Données associées à la mise à jour.
        :type payload: dict
        """
        MulticastSender.send_update(action, table, payload)

    def request_full_sync(self):
        """
        Demande une synchronisation complète des données.

        Envoie une requête multicast afin de déclencher un envoi
        complet des données depuis les autres nœuds du réseau.
        """
        MulticastSender.request_full_sync()