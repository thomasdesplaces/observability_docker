--
-- PostgreSQL Table creation
--

BEGIN;

SET client_encoding = 'UTF8';

CREATE TABLE clients (
    id text NOT NULL PRIMARY KEY,
    firstname text NOT NULL,
    lastname text NOT NULL
);

COMMIT;

ANALYZE clients;
