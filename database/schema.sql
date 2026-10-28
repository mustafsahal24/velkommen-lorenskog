-- Skjema for Velkommen til Lørenskog (SQLite).
-- Kjøres av scripts/init_db.py og lager tabellene på nytt.

DROP TABLE IF EXISTS welcome_messages;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS school_districts;
DROP TABLE IF EXISTS services;

-- Skolekretser: hvilken skole en adresse hører til
CREATE TABLE school_districts (
    id          INTEGER PRIMARY KEY,
    school_name TEXT    NOT NULL,
    url         TEXT
);

-- Adresser i kommunen, koblet til en skolekrets
CREATE TABLE addresses (
    id                 INTEGER PRIMARY KEY,
    street             TEXT    NOT NULL,
    postal_code        TEXT    NOT NULL,
    school_district_id INTEGER NOT NULL REFERENCES school_districts(id),
    UNIQUE (street, postal_code)
);

-- Tjenestene som kan tas med i en velkomst
-- audience: 'all' = alle, 'families' = bare de med barn
CREATE TABLE services (
    id          INTEGER PRIMARY KEY,
    category    TEXT    NOT NULL UNIQUE,
    title       TEXT    NOT NULL,
    description TEXT    NOT NULL,
    url         TEXT    NOT NULL,
    audience    TEXT    NOT NULL DEFAULT 'all'
                CHECK (audience IN ('all', 'families')),
    sort_order  INTEGER NOT NULL DEFAULT 0
);

-- Hver velkomst som er laget
-- event_id er UNIQUE: samme flyttehendelse kan aldri lagres to ganger (idempotens)
CREATE TABLE welcome_messages (
    id           TEXT    PRIMARY KEY,
    event_id     TEXT    NOT NULL UNIQUE,
    full_name    TEXT    NOT NULL,
    email        TEXT    NOT NULL,
    address_id   INTEGER NOT NULL REFERENCES addresses(id),
    has_children INTEGER NOT NULL DEFAULT 0 CHECK (has_children IN (0, 1)),
    message      TEXT    NOT NULL,
    created_at   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);


