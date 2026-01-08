#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from notification import notify_system
import time

def test_notification_basic():
    print("=== Test notification basique ===")
    notify_system("Test Notification", "Ceci est un test simple")
    print("Notification basique envoyée \n")
    time.sleep(2)  # Laisser le temps à la notification de s'afficher

def test_notification_multiple():
    print("=== Test notifications multiples ===")
    messages = [
        "Message 1 - Test",
        "Message 2 - Test",
        "Message 3 - Test"
    ]
    for i, msg in enumerate(messages, start=1):
        notify_system(f"Notification {i}", msg)
        print(f"Notification {i} envoyée ")
        time.sleep(1)  # Pause pour que chaque notification soit visible
    print("\n=== Test notifications multiples terminé ===\n")

def test_notification_long_message():
    print("=== Test notification message long ===")
    long_message = "Ceci est un message très long pour tester la notification système. " * 3
    notify_system("Notification Longue", long_message)
    print("Notification longue envoyée \n")
    time.sleep(2)

if __name__ == "__main__":
    print("=== Début des tests du module Notification ===\n")
    
    test_notification_basic()
    test_notification_multiple()
    test_notification_long_message()
    
    print("=== Tous les tests du module Notification exécutés  ===")
