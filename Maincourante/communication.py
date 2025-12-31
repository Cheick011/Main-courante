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

    def __init__(self):
        self.sync = SyncManager()
        self.receiver = MulticastReceiver(self.sync)

    def start(self):
        self.receiver.start()
        print(" Module de communication démarré")

    def send_update(self, action, table, payload):
        MulticastSender.send_update(action, table, payload)

    def request_full_sync(self):
        MulticastSender.request_full_sync()
