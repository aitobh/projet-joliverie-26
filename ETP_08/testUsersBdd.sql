-- Script de tests généré le 2026-01-07 13:17:28
-- Exécution : pour chaque utilisateur, connectez-vous séparément :
--   mysql -u <login> -p
-- Puis exécutez le bloc correspondant.

-- ==================== Utilisateur : Charlotte RUIZ (login: cruiz) ====================
-- Connectez-vous : mysql -u cruiz -p
USE st_cruiz;

-- 1) Créer une table
CREATE TABLE IF NOT EXISTS t_test (
    id INT PRIMARY KEY AUTO_INCREMENT,
    col1 VARCHAR(100) NOT NULL,
    col2 INT NOT NULL
);

-- 2) Insérer 2 enregistrements
INSERT INTO t_test (col1, col2) VALUES ('premier', 1), ('second', 2);

-- 3) Lire les données
SELECT * FROM t_test;

-- 4) Mettre à jour un enregistrement
UPDATE t_test SET col1 = 'modifie' WHERE col2 = 2;
SELECT * FROM t_test;

-- 5) Créer un index
CREATE INDEX idx_test_col1 ON t_test(col1);
SHOW INDEX FROM t_test;

-- 6) Supprimer un enregistrement
DELETE FROM t_test WHERE col2 = 1;
SELECT * FROM t_test;

-- 7) Supprimer la table
DROP TABLE IF EXISTS t_test;

-- ==================== Utilisateur : Noemie SAMSON (login: nsamson) ====================
-- Connectez-vous : mysql -u nsamson -p
USE st_nsamson;

-- 1) Créer une table
CREATE TABLE IF NOT EXISTS t_test (
    id INT PRIMARY KEY AUTO_INCREMENT,
    col1 VARCHAR(100) NOT NULL,
    col2 INT NOT NULL
);

-- 2) Insérer 2 enregistrements
INSERT INTO t_test (col1, col2) VALUES ('premier', 1), ('second', 2);

-- 3) Lire les données
SELECT * FROM t_test;

-- 4) Mettre à jour un enregistrement
UPDATE t_test SET col1 = 'modifie' WHERE col2 = 2;
SELECT * FROM t_test;

-- 5) Créer un index
CREATE INDEX idx_test_col1 ON t_test(col1);
SHOW INDEX FROM t_test;

-- 6) Supprimer un enregistrement
DELETE FROM t_test WHERE col2 = 1;
SELECT * FROM t_test;

-- 7) Supprimer la table
DROP TABLE IF EXISTS t_test;
