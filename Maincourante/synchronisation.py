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
from Connexion_dataBase import connexion
from config import PEERS, PORT
import threading

class synchro:
    """
    Manager for network synchronization.

    Handles requesting full database synchronization from peers
    and applying received data to the local database.
    """

    def synchrocomplete(self, peer_ip: str) -> dict | None:
        """
        Sends a FULL_SYNC request to a peer and waits for the response.

        :param peer_ip: IP address of the peer to query.
        :type peer_ip: str
        :return: A dictionary containing 'utilisateurs' and 'donnees' if successful, None otherwise.
        :rtype: dict | None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)  # 5-second timeout
            message = {"type": "sync", "action": "FULL_SYNC", "payload": None}
            sock.sendto(json.dumps(message).encode("utf-8"), (peer_ip, PORT))
            
            data, _ = sock.recvfrom(65536)  # Maximum message size
            response = json.loads(data.decode())
            return response.get("payload", None)
        except Exception as e:
            print(f"[SYNC] Peer {peer_ip} unavailable: {e}")
            return None
        finally:
            sock.close()

    def appliquer_synchro(self, data: dict):
        """
        Applies the data received from a peer to the local database.

        :param data: Dictionary containing 'utilisateurs' and 'donnees'.
        :type data: dict
        """
        if not data:
            print("[SYNC] No data to synchronize")
            return

        conn = connexion()
        cur = conn.cursor()
        try:
            # Clear local data
            cur.execute("DELETE FROM utilisateurs;")
            cur.execute("DELETE FROM donnees;")

            # Insert users
            for u in data["utilisateurs"]:
                cur.execute("""
                    INSERT INTO utilisateurs
                    (id, nom_utilisateur, mot_de_passe, role, date_creation)
                    VALUES (%s,%s,%s,%s,%s)
                """, (u["id"], u["nom_utilisateur"], u["mot_de_passe"], u["role"], u["date_creation"]))

            # Insert data entries
            for d in data["donnees"]:
                cur.execute("""
                    INSERT INTO donnees
                    (id, date, heure, de, a, descriptif, id_utilisateur)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (d["id"], d["date"], d["heure"], d["de"], d["a"], d["descriptif"], d["id_utilisateur"]))

            conn.commit()
            print("[SYNC] Full synchronization applied successfully")
        except Exception as e:
            conn.rollback()
            print("[SYNC] Error applying full sync:", e)
        finally:
            cur.close()
            conn.close()

    def start_sync(self):
        """
        Attempts to fetch the full database from peers listed in config.PEERS
        until a response is obtained. If no peer responds, the local database
        is kept.
        """
        print("[SYNC] Starting network synchronization...")
        for peer_ip in PEERS:
            print(f"[SYNC] Querying peer {peer_ip}...")
            data = self.request_full_sync(peer_ip)
            if data:
                print(f"[SYNC] Peer {peer_ip} responded, applying data...")
                self.apply_full_sync(data)
                break
        else:
            print("[SYNC] No peers responded. Local database remains unchanged.")

def sync_thread():
    """
    Starts the synchronization process in a background thread.
    """
    manager = SyncManager()
    threading.Thread(target=manager.start_sync, daemon=True).start()
