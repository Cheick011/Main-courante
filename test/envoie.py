# test_envoie.py
from envoie import Envoie
from config import PEERS

# Simuler un peer local
PEERS[:] = ["127.0.0.1"]

print("Envoi d'un message test...")
Envoie.send("donnee", "INSERT", {"id": 1, "date": "2026-01-10", "heure": "12:00", "de": "PC", "a": "Cheick", "descriptif": "Test"})
print("Test Envoie terminé")
