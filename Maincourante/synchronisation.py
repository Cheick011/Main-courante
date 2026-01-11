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


class synchro:
    """
    Network synchronization manager.

    Handles full database synchronization requests and applies received
    data to the local database by overwriting existing content.
    """

    def synchrocomplete(self, peer_ip: str) -> Optional[dict]:
        """
        Request a full database synchronization from a peer.

        Args:
            peer_ip (str): IP address of the peer.

        Returns:
            dict or None: Full database payload if successful, None otherwise.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)

            message = {
                "type": "sync",
                "action": "REQUEST",
                "payload": None
            }

            sock.sendto(json.dumps(message).encode("utf-8"), (peer_ip, PORT))

            data, _ = sock.recvfrom(65536)
            response = json.loads(data.decode("utf-8"))

            return response.get("payload")

        except Exception as e:
            print(f"[SYNC] Peer {peer_ip} unreachable: {e}")
            return None

        finally:
            sock.close()

    def appliquer_synchro(self, data: dict):
        """
        Apply a full synchronization payload to the local database.

        This method completely clears existing tables and reinserts
        all received data.

        Args:
            data (dict): Dictionary containing 'utilisateurs' and 'donnees'.
        """
        if not data:
            print("[SYNC] No data to apply")
            return

        conn = connexion()
        cur = conn.cursor()

        try:
            # Clear tables (respect foreign keys order)
            cur.execute("DELETE FROM donnees;")
            cur.execute("DELETE FROM utilisateurs;")

            # Insert users
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

            # Insert data records
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
            print("[SYNC] Full synchronization successfully applied")

        except Exception as e:
            conn.rollback()
            print("[SYNC] Error while applying synchronization:", e)

        finally:
            cur.close()
            conn.close()

    def start_sync(self):
        """
        Attempt to fetch and apply a full database synchronization
        from the first available peer.
        """
        print("[SYNC] Starting synchronization process...")

        for peer_ip in PEERS:
            print(f"[SYNC] Contacting peer {peer_ip}...")
            data = self.synchrocomplete(peer_ip)

            if data:
                print(f"[SYNC] Synchronization received from {peer_ip}")
                self.appliquer_synchro(data)
                break
        else:
            print("[SYNC] No peers responded. Local database unchanged.")
