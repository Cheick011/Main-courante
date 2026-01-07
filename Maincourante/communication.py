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
   Multicast-based network communication module.

   This class centralizes the management of network communications,
   including receiving multicast messages, sending updates,
   and handling full synchronization requests.
   
   """

    def __init__(self):
      """
      Initializes the communication module.

      Creates a synchronization manager instance as well as a multicast
      receiver responsible for handling incoming messages.
      """

      self.sync = SyncManager()
      self.receiver = MulticastReceiver(self.sync)

    def start(self):

      """
      Starts the communication module.

      Launches the multicast receiver to begin listening
      for incoming network messages.
      """

      self.receiver.start()
      print(" Module de communication démarré")

    def send_update(self, action, table, payload):

      """
      Sends an update over the multicast network.

      :param action: Type of action to perform (e.g. ``INSERT``, ``UPDATE``, ``DELETE``).
      :type action: str
      :param table: Name of the table affected by the update.
      :type table: str
      :param payload: Data associated with the update.
      :type payload: dict
      """

      MulticastSender.send_update(action, table, payload)

    def request_full_sync(self):
      """
      Requests a full data synchronization.

      Sends a multicast request to trigger a complete data
      transfer from the other nodes on the network.
      """
      MulticastSender.request_full_sync()
