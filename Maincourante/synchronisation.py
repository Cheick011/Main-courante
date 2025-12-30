from Connexion_dataBase import connexion

class SyncManager:

    def apply_update(self, msg):
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
