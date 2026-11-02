-- Skjema for Velkommen til Lørenskog (Azure SQL / T-SQL).
-- Samme tabeller som schema.sql, men med SQL Server-typer.

DROP TABLE IF EXISTS welcome_messages;
DROP TABLE IF EXISTS addresses;
DROP TABLE IF EXISTS school_districts;
DROP TABLE IF EXISTS services;

-- Skolekretser: hvilken skole en adresse hører til
CREATE TABLE school_districts (
    id          INT           PRIMARY KEY,
    school_name NVARCHAR(200) NOT NULL,
    url         NVARCHAR(500)
);

-- Adresser i kommunen, koblet til en skolekrets
CREATE TABLE addresses (
    id                 INT           PRIMARY KEY,
    street             NVARCHAR(200) NOT NULL,
    postal_code        NVARCHAR(10)  NOT NULL,
    school_district_id INT           NOT NULL REFERENCES school_districts(id),
    UNIQUE (street, postal_code)
);

-- Tjenestene som kan tas med i en velkomst
CREATE TABLE services (
    id          INT           IDENTITY(1,1) PRIMARY KEY,
    category    NVARCHAR(50)  NOT NULL UNIQUE,
    title       NVARCHAR(200) NOT NULL,
    description NVARCHAR(500) NOT NULL,
    url         NVARCHAR(500) NOT NULL,
    audience    NVARCHAR(20)  NOT NULL DEFAULT 'all'
                CHECK (audience IN ('all', 'families')),
    sort_order  INT           NOT NULL DEFAULT 0
);

-- Hver velkomst som er laget
-- event_id er UNIQUE: samme flyttehendelse kan aldri lagres to ganger (idempotens)
CREATE TABLE welcome_messages (
    id           NVARCHAR(36)  PRIMARY KEY,
    event_id     NVARCHAR(100) NOT NULL UNIQUE,
    full_name    NVARCHAR(200) NOT NULL,
    email        NVARCHAR(320) NOT NULL,
    address_id   INT           NOT NULL REFERENCES addresses(id),
    has_children BIT           NOT NULL DEFAULT 0,
    message      NVARCHAR(MAX) NOT NULL,
    created_at   DATETIME2     NOT NULL DEFAULT SYSUTCDATETIME()
);