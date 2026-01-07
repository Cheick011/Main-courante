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
      Establishes a connection to the PostgreSQL database.

      This function creates and returns a connection to the ``spelo_app``
      database using the ``psycopg2`` library with predefined connection
      parameters.

      :return: PostgreSQL database connection object.
      :rtype: psycopg2.extensions.connection
      :raises psycopg2.OperationalError: If the connection to the database fails.

    """
   
   return psycopg2.connect(
        dbname="spelo_app",
        user="admin",
        password="admin",
        host="localhost",
        port=5432
    )
