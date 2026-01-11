#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: synchro
   :platform: Unix, Windows
   :synopsis: Network synchronization of Spelo application data.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitiers.fr>

"""

import socket
import json
from typing import Optional

from Connexion_dataBase import connexion
from config import PEERS, PORT


class Synchro:
    """
    Full synchronization manager.

    This class handles the process of requesting full database synchronization from a peer machine,
    applying the received data to the local database, and performing full synchronization at startup.


    """

    def request_full_sync(self, peer_ip: str) -> Optional[dict]:
        """
        Request full database sync from a peer.

        This method sends a synchronization request to a peer machine, waits for a response, and 
        returns the payload of the received synchronization data.

        Args:
            peer_ip (str): The IP address of the peer machine to request synchronization from.

        Returns:
            dict or None:
                - Returns the 'payload' from the peer's response if synchronization data is received.
                - Returns None if there is an error or the peer is unreachable.
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)

            message = {
                "type": "sync",         # Message type: sync
                "action": "REQUEST",    # Action: request full sync
                "payload": None         # No payload is needed for the request
            }

            sock.sendto(json.dumps(message).encode(), (peer_ip, PORT))
            data, _ = sock.recvfrom(65536)

            response = json.loads(data.decode())
            return response.get("payload")  # Returns the payload if present

        except Exception as e:
            print(f"[SYNC] Peer {peer_ip} unreachable: {e}")
            return None

        finally:
            sock.close()

    def apply_full_sync(self, data: dict):
        """
        Completely overwrite the local database with received data.

        This method is used to replace the local database's content with the full synchronization 
        data received from a peer. It deletes existing records in the 'utilisateurs' and 'donnees' 
        tables and inserts the new data.

        Args:
            data (dict): The data received from the peer containing the 'utilisateurs' and 'donnees' 
                         tables to be applied to the local database.

        Returns:
            None
        """
        if not data:
            print("[SYNC] No data received")
            return

        conn = connexion()
        cur = conn.cursor()

        try:
            # Delete all existing records in the local tables
            cur.execute("DELETE FROM donnees;")
            cur.execute("DELETE FROM utilisateurs;")

            # Insert new records into the 'utilisateurs' table
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

            # Insert new records into the 'donnees' table
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

        This method attempts to synchronize with each peer listed in the `PEERS` list by calling
        `request_full_sync` and applying the data received using `apply_full_sync`.

        It stops after the first successful synchronization.

        Returns:
            None
        """
        print("[SYNC] Starting full sync...")
        for peer in PEERS:
            data = self.request_full_sync(peer)  # Request sync from each peer
            if data:
                self.apply_full_sync(data)  # Apply received data
                return
        print("[SYNC] No peer responded")
