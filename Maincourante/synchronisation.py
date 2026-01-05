#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
.. module:: synchronisation
   :platform: Unix, windows
   :synopsis: module pour synchroniser la base de donnée d'une machine avec les autres dans le multiast en cas de demarrage ou d'interruption pour avoir un contenu coherent.

.. moduleauthor:: N'DIAYE Cheick Bounama Boubacar <cheick.n.diaye@etu.univ-poitier.fr>


"""

from Connexion_dataBase import connexion

class SyncManager:
    """
    Gestionnaire de synchronisation des données entre les nœuds.

    Cette classe permet d'appliquer des mises à jour partielles (ajout, mise à jour, suppression)
    des données locales ainsi que d'effectuer une synchronisation complète avec les autres machines.
    """

    def apply_update(self, msg):
        """
        Applique une mise à jour locale en fonction de l'action reçue (ajout, mise à jour, suppression).

        Cette méthode traite les messages multicast et applique les modifications à la base de données locale
        dans la table ``donnees``.

        :param msg: Message reçu contenant les détails de l'action à appliquer.
        :type msg: dict
        :raises Exception: Si une erreur se produit lors de l'application de la mise à jour.
        """
        action = msg["action"]
        table = msg["table"]
        payload = msg["payload"]

        conn = connexion()
        cur = conn.cursor()

        try:
            if table == "donnees":

                if action == "add":
                    cur.execute("""
                        INSERT INTO donnees (id, heure, de, a, descriptif, date, id_utilisateur)
                        VALUES (%(id)s, %(heure)s, %(de)s, %(a)s, %(descriptif)s, %(date)s, %(id_utilisateur)s)
                        ON CONFLICT (id) DO NOTHING;
                    """, payload)

                elif action == "update":
                    cur.execute("""
                        UPDATE donnees SET
                            heure=%(heure)s,
                            de=%(de)s,
                            a=%(a)s,
                            descriptif=%(descriptif)s,
                            date=%(date)s,
                            id_utilisateur=%(id_utilisateur)s
                        WHERE id=%(id)s;
                    """, payload)

                elif action == "delete":
                    cur.execute("DELETE FROM donnees WHERE id=%(id)s;", payload)

            conn.commit()
            print(" Mise à jour locale appliquée")

        except Exception as e:
            print(" Erreur apply_update :", e)

        cur.close()
        conn.close()

    def apply_full_sync(self, data):
        """
        Applique une synchronisation complète des données locales avec celles des autres nœuds.

        Cette méthode efface toutes les données locales dans les tables ``utilisateurs`` et ``donnees``
        et les remplace par celles reçues d'un autre nœud, assurant ainsi une cohérence complète entre les machines.

        :param data: Données à synchroniser, comprenant les tables ``utilisateurs`` et ``donnees``.
        :type data: dict
        :raises Exception: Si une erreur se produit lors de l'application de la synchronisation.
        """
        conn = connexion()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM utilisateurs;")
            cur.execute("DELETE FROM donnees;")

            for u in data["utilisateurs"]:
                cur.execute("""
                    INSERT INTO utilisateurs (id, nom_utilisateur, mot_de_passe, role, date_creation)
                    VALUES (%s, %s, %s, %s, %s)
                """, (u["id"], u["nom_utilisateur"], u["mot_de_passe"], u["role"], u["date_creation"]))

            for d in data["donnees"]:
                cur.execute("""
                    INSERT INTO donnees (id, heure, de, a, descriptif, date, id_utilisateur)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (d["id"], d["heure"], d["de"], d["a"], d["descriptif"], d["date"], d["id_utilisateur"]))

            conn.commit()
            print(" FULL SYNC appliqué")

        except Exception as e:
            print(" Erreur full sync :", e)

        cur.close()
        conn.close()
