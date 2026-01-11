#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: synchro
   :platform: Unix, Windows
   :synopsis: Network synchronization of Spelo application data.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitiers.fr>

This module allows a machine to fetch the complete database from other
machines on the network at startup or after a network interruption.
It ensures the local database is consistent with a responding peer.
"""

import socket
import json
from typing import Optional

from Connexion_dataBase import connexion
from config import PEERS, PORT


class Synchro:
    """
    Full synchronization manager.
    """

    def request_full_sync(self, peer_ip: str) -> Optional[dict]:
        """
        Request full database sync from a peer.

        Returns:
            dict or None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)

            message = {
                "type": "sync",
                "action": "REQUEST",
                "payload": None
            }

            sock.sendto(json.dumps(message).encode(), (peer_ip, PORT))
            data, _ = sock.recvfrom(65536)

            response = json.loads(data.decode())
            return response.get("payload")

        except Exception as e:
            print(f"[SYNC] Peer {peer_ip} unreachable: {e}")
            return None

        finally:
            sock.close()

    def apply_full_sync(self, data: dict):
        """
        Completely overwrite local database with received data.
        """
        if not data:
            print("[SYNC] No data received")
            return

        conn = connexion()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM donnees;")
            cur.execute("DELETE FROM utilisateurs;")

            for u in data.get("utilisateurs", []):
                cur.execute("""
                    INSERT INTO utilisateurs
                    (id, nom_utilisateur, mot_de_passe, role, date_creation)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    u["id"],
                    u["nom_utilisateur"],
                    u["mot_de_passe"],
                    u["role"],
                    u["date_creation"]
                ))

            for d in data.get("donnees", []):
                cur.execute("""
                    INSERT INTO donnees
                    (id, date, heure, de, a, descriptif, id_utilisateur)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    d["id"],
                    d["date"],
                    d["heure"],
                    d["de"],
                    d["a"],
                    d["descriptif"],
                    d["id_utilisateur"]
                ))

            conn.commit()
            print("[SYNC] Full synchronization applied")

        except Exception as e:
            conn.rollback()
            print("[SYNC] Error:", e)

        finally:
            cur.close()
            conn.close()

    def start_sync(self):
        """
        Run full sync once at startup.
        """
        print("[SYNC] Starting full sync...")
        for peer in PEERS:
            data = self.request_full_sync(peer)
            if data:
                self.apply_full_sync(data)
                return
        print("[SYNC] No peer responded")

