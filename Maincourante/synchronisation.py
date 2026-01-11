#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: synchronisation
   :platform: Unix, windows
   :synopsis: module pour synchroniser la base de donnée d'une machine avec les autres dans le multiast en cas de demarrage ou d'interruption pour avoir un contenu coherent.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""




from Connexion_dataBase import connexion

class synchro:

    """
    Full database synchronization manager for replacing local data with
    peer data.
    """
    def __init__(self):
        """
        Initialization.
        """

    def synchro_Complete(self, data):
        """
        Applies a full synchronization to the local database.

        Deletes all existing records in 'utilisateurs' and 'donnees' tables,
        and inserts the records provided in the 'data' dictionary.

        Args:
            data (dict): Dictionary containing two keys:
                - "utilisateurs": list of user records
                - "donnees": list of data records

        Exceptions:
            Any database error triggers a rollback and is printed.
        """


        conn = connexion()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM utilisateurs;")
            cur.execute("DELETE FROM donnees;")

            for u in data["utilisateurs"]:
                cur.execute("""
                    INSERT INTO utilisateurs
                    (id, nom_utilisateur, mot_de_passe, role, date_creation)
                    VALUES (%s,%s,%s,%s,%s)
                """, (
                    u["id"], u["nom_utilisateur"],
                    u["mot_de_passe"], u["role"],
                    u["date_creation"]
                ))

            for d in data["donnees"]:
                cur.execute("""
                    INSERT INTO donnees
                    (id, date, heure, de, a, descriptif, id_utilisateur)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """, (
                    d["id"], d["date"], d["heure"],
                    d["de"], d["a"], d["descriptif"],
                    d["id_utilisateur"]
                ))

            conn.commit()
            print("Synchronisation complète appliquée")

        except Exception as e:
            conn.rollback()
            print("Erreur sync complète :", e)

        finally:
            cur.close()
            conn.close()
