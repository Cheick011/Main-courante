# test_synchro.py
from synchronisation import synchro

data = {
    "utilisateurs": [
        {"id": 1, "nom_utilisateur": "user1", "mot_de_passe": "123", "role": "admin", "date_creation": "2026-01-10"}
    ],
    "donnees": [
        {"id": 1, "date": "2026-01-10", "heure": "12:00", "de": "PC", "a": "Cheick", "descriptif": "test", "id_utilisateur": 1}
    ]
}

s = synchro()
s.synchro_Complete(data)
print("Test synchro complet terminé")
