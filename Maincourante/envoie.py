#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: Envoie
   :platform: Unix, Windows
   :synopsis: Module For Sends data to others post.
.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitiers.fr>
"""

import socket
import json
from config import PEERS, PORT


class Envoie:
    """
    Network sender for partial database updates.
    """

    @staticmethod
    def send(msg_type: str, action: str, payload: dict):
        """
        Send a UDP message to all peers.

        Args:
            msg_type (str): Message type (donnee, utilisateur, sync)
            action (str): INSERT, UPDATE, DELETE, REQUEST, RESPONSE
            payload (dict): Data payload
        """
        message = {
            "type": msg_type,
            "action": action,
            "payload": payload
        }

        data = json.dumps(message).encode("utf-8")

        for peer in PEERS:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data, (peer, PORT))
                sock.close()
            except Exception as e:
                print(f"[SEND] Failed to send to {peer}: {e}")

