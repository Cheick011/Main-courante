# test_reception.py
from reception import Reception

r = Reception()

# Test d'insertion utilisateur
msg_user = {
    "type": "utilisateur",
    "action": "INSERT",
    "payload": {"nom": "testuser", "mdp": "123", "role": "admin"}
}
r.appliquer(msg_user)
print("Test Reception utilisateur INSERT terminé")

# Test de modification de donnée
msg_donnee = {
    "type": "donnee",
    "action": "UPDATE",
    "payload": {
        "id": 1,
        "date": "2026-01-10",
        "heure": "14:00",
        "de": "PC",
        "a": "Cheick",
        "descriptif": "modif"
    }
}
r.appliquer(msg_donnee)
print("Test Reception donnee UPDATE terminé")
