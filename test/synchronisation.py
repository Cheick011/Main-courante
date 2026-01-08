#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fichier de test pour le module Synchronisation.
Permet de tester :
- apply_update (INSERT, UPDATE, DELETE)
- apply_full_sync (remplacer complètement les données locales)
"""

from synchronisation import SyncManager
import datetime

def test_apply_update():
    print("=== Test apply_update ===")

    sync = SyncManager()

    # 1️ Test INSERT
    msg_insert = {
        "action": "add",
        "table": "donnees",
        "payload": {
            "id": 9000,
            "heure": "14:00",
            "de": "TestInsertFrom",
            "a": "TestInsertTo",
            "descriptif": "Test INSERT",
            "date": str(datetime.date.today()),
            "id_utilisateur": 1
        }
    }
    sync.apply_update(msg_insert)
    print("INSERT appliqué ")

    # 2️ Test UPDATE
    msg_update = {
        "action": "update",
        "table": "donnees",
        "payload": {
            "id": 9000,
            "heure": "15:00",
            "de": "TestUpdateFrom",
            "a": "TestUpdateTo",
            "descriptif": "Test UPDATE",
            "date": str(datetime.date.today()),
            "id_utilisateur": 1
        }
    }
    sync.apply_update(msg_update)
    print("UPDATE appliqué ")

    # 3️ Test DELETE
    msg_delete = {
        "action": "delete",
        "table": "donnees",
        "payload": {"id": 9000}
    }
    sync.apply_update(msg_delete)
    print("DELETE appliqué \n")


def test_apply_full_sync():
    print("=== Test apply_full_sync ===")

    sync = SyncManager()

    # Données fictives pour full sync
    data = {
        "utilisateurs": [
            {"id": 1, "nom_utilisateur": "admin", "mot_de_passe": "admin", "role": "admin", "date_creation": str(datetime.date.today())},
            {"id": 2, "nom_utilisateur": "user1", "mot_de_passe": "user1", "role": "client", "date_creation": str(datetime.date.today())}
        ],
        "donnees": [
            {"id": 8000, "heure": "10:00", "de": "A", "a": "B", "descriptif": "Full sync test", "date": str(datetime.date.today()), "id_utilisateur": 1}
        ]
    }

    sync.apply_full_sync(data)
    print("FULL SYNC appliqué \n")


if __name__ == "__main__":
    print("=== Début des tests du module Synchronisation ===\n")

    test_apply_update()
    test_apply_full_sync()

    print("=== Tous les tests du module Synchronisation exécutés  ===")
