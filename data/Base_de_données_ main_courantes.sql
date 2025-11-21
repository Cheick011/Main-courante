CREATE DATABASE spelo_app ;
USE spelo_app;



CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom_utilisateur VARCHAR(50) UNIQUE NOT NULL,
    mot_de_passe TEXT NOT NULL,
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    role TEXT DEFAULT 'lecteur' CHECK (statut IN ('lecteur', 'admin', 'gestionnaire')) 
);


insert INTO TABLE utilisateurs (nom_utilisateur, mot_de_passe, role)  values
('admin', 'admin','admin'),
('gestionnaire', 'gestionnaire', 'gestionnaire'),
('lecteur', 'lecteur', 'lecteur');


CREATE TABLE donnees (
    id SERIAL PRIMARY KEY,
    heure TIME DEFAULT CURRENT_TIME,
    de TEXT;
    a TEX
    descriptif TEXT NOT NULL,
    date DATE DEFAULT CURRENT_DATE,
    id_utilisateur INTEGER REFERENCES utilisateurs(id) ON DELETE SET NULL
);





-- rôle de base : ne peut que lire
CREATE ROLE lecteur;

-- rôle gestionnaire : peut manipuler les données
CREATE ROLE gestionnaire;

-- rôle admin : peut tout faire
CREATE ROLE admin;


-- Données accessibles à tous (lecture)
GRANT SELECT ON donnees TO lecteur;

-- Gestionnaire : lecture + modification
GRANT SELECT, INSERT, UPDATE, DELETE ON donnees TO gestionnaire;

-- Admin : tout, y compris gérer utilisateurs
GRANT SELECT, INSERT, UPDATE, DELETE ON donnees TO admin;
GRANT SELECT, INSERT, UPDATE, DELETE ON utilisateurs TO admin;





