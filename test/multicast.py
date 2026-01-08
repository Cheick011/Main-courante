#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier de test pour le module Multicast.
Permet de tester :
- MulticastSender (send_message, send_update, request_full_sync)
- MulticastReceiver (réception et traitement des messages)
"""

import threading
import time
from multicast import MulticastSender, MulticastReceiver
from synchronisation import SyncManager

def test_multicast_sender():
    print("=== Test MulticastSender ===")
    
    # Envoyer un message simple
    MulticastSender.send_message({"type": "test", "msg": "Hello multicast sender"})
    print("Message simple envoyé ")

    # Envoyer un update test
    payload = {
        "id": 5000,
        "heure": "12:30",
        "de": "X",
        "a": "Y",
        "descriptif": "Test send_update",
        "date": "2026-01-08",
        "id_utilisateur": 1
    }
    MulticastSender.send_update("INSERT", "donnees", payload)
    print("Update envoyé via send_update ")

    # Envoyer une requête de full sync
    MulticastSender.request_full_sync()
    print("Request full sync envoyé \n")


def test_multicast_receiver():
    print("=== Test MulticastReceiver ===")
    
    sync = SyncManager()
    receiver = MulticastReceiver(sync)

    # Lancer le receiver dans un thread daemon
    receiver_thread = threading.Thread(target=receiver.run, daemon=True)
    receiver_thread.start()
    print("MulticastReceiver en écoute ")

    # Laisser quelques secondes pour la réception
    time.sleep(2)

    # Envoyer un message test pour voir si le receiver le traite
    MulticastSender.send_message({"type": "test", "msg": "Message pour receiver"})
    print("Message envoyé pour test receiver ")

    # Laisser le temps au receiver de traiter
    time.sleep(2)
    print("=== Test MulticastReceiver terminé \n")


if __name__ == "__main__":
    print("=== Début des tests du module Multicast ===\n")

    test_multicast_sender()
    test_multicast_receiver()

    print("=== Tous les tests du module Multicast exécutés  ===")
