-- Sample SQL initialisation script
--
-- Replace content with your intended schema and values, and
-- rename file to `default.sql`

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE people (name varchar(255) not null, surname varchar(255) not null);
INSERT INTO people VALUES('Heli','Barrocas');
INSERT INTO people VALUES('Etienne','Delacroix');
COMMIT;
