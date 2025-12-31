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
    return psycopg2.connect(
        dbname="spelo_app",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )
