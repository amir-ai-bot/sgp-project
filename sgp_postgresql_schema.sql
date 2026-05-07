-- SGP PostgreSQL Database Schema

-- Drop tables if they exist to allow for clean re-creation
DROP TABLE IF EXISTS Rapports CASCADE;
DROP TABLE IF EXISTS Documents CASCADE;
DROP TABLE IF EXISTS Taches CASCADE;
DROP TABLE IF EXISTS Projets CASCADE;
DROP TABLE IF EXISTS Utilisateurs CASCADE;
DROP TABLE IF EXISTS Roles CASCADE;

-- Table: Roles
CREATE TABLE Roles (
    id_role SERIAL PRIMARY KEY,
    nom_role VARCHAR(50) UNIQUE NOT NULL
);

-- Table: Utilisateurs
CREATE TABLE Utilisateurs (
    id_utilisateur SERIAL PRIMARY KEY,
    nom_utilisateur VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL, -- Store hashed passwords
    id_role INTEGER NOT NULL,
    FOREIGN KEY (id_role) REFERENCES Roles(id_role)
);

-- Table: Projets
CREATE TABLE Projets (
    id_projet SERIAL PRIMARY KEY,
    nom_projet VARCHAR(255) NOT NULL,
    description TEXT,
    date_debut DATE NOT NULL,
    date_fin_prevue DATE,
    statut VARCHAR(50) DEFAULT 'En Cours',
    chef_projet_id INTEGER NOT NULL,
    FOREIGN KEY (chef_projet_id) REFERENCES Utilisateurs(id_utilisateur)
);

-- Table: Taches
CREATE TABLE Taches (
    id_tache SERIAL PRIMARY KEY,
    nom_tache VARCHAR(255) NOT NULL,
    description TEXT,
    date_debut DATE,
    date_fin_prevue DATE,
    statut VARCHAR(50) DEFAULT 'À Faire',
    priorite VARCHAR(50) DEFAULT 'Moyenne',
    id_projet INTEGER NOT NULL,
    assigne_a_id INTEGER, -- Can be NULL if not yet assigned
    FOREIGN KEY (id_projet) REFERENCES Projets(id_projet),
    FOREIGN KEY (assigne_a_id) REFERENCES Utilisateurs(id_utilisateur)
);

-- Table: Documents
CREATE TABLE Documents (
    id_document SERIAL PRIMARY KEY,
    nom_document VARCHAR(255) NOT NULL,
    chemin_fichier VARCHAR(255) NOT NULL,
    type_document VARCHAR(100),
    date_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_projet INTEGER NOT NULL,
    upload_par_id INTEGER NOT NULL,
    FOREIGN KEY (id_projet) REFERENCES Projets(id_projet),
    FOREIGN KEY (upload_par_id) REFERENCES Utilisateurs(id_utilisateur)
);

-- Table: Rapports
CREATE TABLE Rapports (
    id_rapport SERIAL PRIMARY KEY,
    nom_rapport VARCHAR(255) NOT NULL,
    type_rapport VARCHAR(100),
    date_generation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contenu TEXT,
    genere_par_id INTEGER NOT NULL,
    id_projet INTEGER,
    FOREIGN KEY (genere_par_id) REFERENCES Utilisateurs(id_utilisateur),
    FOREIGN KEY (id_projet) REFERENCES Projets(id_projet) -- Can be NULL for global reports
);

-- Initial Data (Optional, for testing purposes)
INSERT INTO Roles (nom_role) VALUES ('Administrateur'), ('Chef de Projet'), ('Membre Equipe'), ('Client'), ('Direction');

-- Hashed password for 'admin' (password: adminpass)
INSERT INTO Utilisateurs (nom_utilisateur, email, mot_de_passe, id_role) VALUES
('admin', 'admin@sgp.com', '$2b$12$cfoT0.JzxIyN4oh7HqueCO./kxnSvD5tBEHLBxsdLuIjNCHvsT.n.', (SELECT id_role FROM Roles WHERE nom_role = 'Administrateur')),
('chef1', 'chef1@sgp.com', '$2b$12$cfoT0.JzxIyN4oh7HqueCO./kxnSvD5tBEHLBxsdLuIjNCHvsT.n.', (SELECT id_role FROM Roles WHERE nom_role = 'Chef de Projet')),
('membre1', 'membre1@sgp.com', '$2b$12$cfoT0.JzxIyN4oh7HqueCO./kxnSvD5tBEHLBxsdLuIjNCHvsT.n.', (SELECT id_role FROM Roles WHERE nom_role = 'Membre Equipe'));

INSERT INTO Projets (nom_projet, description, date_debut, chef_projet_id) VALUES
('Projet Alpha', 'Développement du module de gestion des utilisateurs.', '2026-04-01', (SELECT id_utilisateur FROM Utilisateurs WHERE email = 'chef1@sgp.com')),
('Projet Beta', 'Implémentation des fonctionnalités de reporting.', '2026-04-15', (SELECT id_utilisateur FROM Utilisateurs WHERE email = 'chef1@sgp.com'));

INSERT INTO Taches (nom_tache, description, id_projet, assigne_a_id) VALUES
('Conception UI Login', 'Concevoir l''interface utilisateur pour la page de connexion.', (SELECT id_projet FROM Projets WHERE nom_projet = 'Projet Alpha'), (SELECT id_utilisateur FROM Utilisateurs WHERE email = 'membre1@sgp.com')),
('Développement API Auth', 'Développer l''API pour l''authentification des utilisateurs.', (SELECT id_projet FROM Projets WHERE nom_projet = 'Projet Alpha'), (SELECT id_utilisateur FROM Utilisateurs WHERE email = 'membre1@sgp.com'));

-- Note: Passwords are hashed using a placeholder 'pbkdf2:sha256:260000$h6w1a2b3c4d5e6f7$8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b' for 'adminpass'.
-- In a real application, you would hash passwords securely during user registration.
