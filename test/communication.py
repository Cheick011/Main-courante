#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import threading
import time
from communication import CommunicationModule

def test_communication_module():
    print("=== Test Communication Module ===")

    # Créer l'instance
    comm = CommunicationModule()

    # Démarrer le receiver dans un thread pour ne pas bloquer
    receiver_thread = threading.Thread(target=comm.start, daemon=True)
    receiver_thread.start()
    print("CommunicationModule démarré, receiver en écoute ")

    # Laisser le receiver démarrer correctement
    time.sleep(1)

    # Envoyer un update de test
    update_payload = {
        "id": 4000,
        "heure": "12:00",
        "de": "TestFrom",
        "a": "TestTo",
        "descriptif": "Test update communication module",
        "date": "2026-01-08",
        "id_utilisateur": 1
    }

    comm.send_update("INSERT", "donnees", update_payload)
    print("Update envoyé via CommunicationModule ")

    # Envoyer une demande de full sync
    comm.request_full_sync()
    print("Full sync demandé via CommunicationModule \n")

    # Laisser quelques secondes pour réception et traitement
    time.sleep(2)
    print("=== Test CommunicationModule terminé ===")


if __name__ == "__main__":
    test_communication_module()
