#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: Connexion_dataBase
   :platform: Unix, windows
   :synopsis: module pour connecter l'application à la base de donnée postgresql

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""

import psycopg2

def connexion():
   """
    Établit une connexion à la base de données PostgreSQL.

    Cette fonction crée et retourne une connexion à la base de données
    ``spelo_app`` en utilisant la bibliothèque ``psycopg2`` avec les
    paramètres de connexion prédéfinis.

    :return: Objet de connexion à la base de données PostgreSQL.
    :rtype: psycopg2.extensions.connection
    :raises psycopg2.OperationalError: Si la connexion à la base de données échoue.
    """
   
   return psycopg2.connect(
        dbname="spelo_app",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )
