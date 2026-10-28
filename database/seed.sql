-- Testdata for Velkommen til Lørenskog.
-- Skolenavn og lenker er hentet fra kommunens oversikt over barneskoler.
-- Koblingen mellom adresse og skole er EKSEMPELDATA, ikke kommunens inntaksområder.

-- Skolekretser (barneskoler)
INSERT INTO school_districts (id, school_name, url) VALUES
    (1, 'Benterud skole',   'https://www.lorenskog.kommune.no/benterud-skole'),
    (2, 'Fjellhamar skole', 'https://www.lorenskog.kommune.no/fjellhamar-skole'),
    (3, 'Rasta skole',      'https://www.lorenskog.kommune.no/rasta-skole');

-- Adresser (fiktive gatenavn, kun for demo)
INSERT INTO addresses (id, street, postal_code, school_district_id) VALUES
    (1, 'Eksempelveien 1', '1470', 1),
    (2, 'Eksempelveien 2', '1470', 1),
    (3, 'Testgata 10',     '1472', 2),
    (4, 'Demostien 5',     '1473', 3);

-- Tjenester i velkomsten
-- Lenker og beskrivelser er hentet fra kommunens side "Ny i Lørenskog".
-- audience: 'families' vises bare for dem med barn.
INSERT INTO services (category, title, description, url, audience, sort_order) VALUES
    ('school',       'Skole',
     'Se hvilken skole adressen din hører til, og hvordan du bytter skole.',
     'https://www.lorenskog.kommune.no/tjenester/barnehage-og-skole/skole/skoletilhorighet-bytte-skole/',
     'families', 10),
    ('kindergarten', 'Barnehage',
     'Les om barnehagetilbudet i kommunen og hvordan du søker plass.',
     'https://www.lorenskog.kommune.no/tjenester/barnehage-og-skole/barnehage/',
     'families', 20),
    ('waste',        'Avfall og renovasjon',
     'ROAF håndterer husholdningsavfallet. Se hva du kan kaste og hvor.',
     'https://www.roaf.no/',
     'all', 30),
    ('gp',           'Fastlege',
     'Velg fastlege på Helsenorge.',
     'https://www.helsenorge.no/fastlegen/',
     'all', 40),
    ('activities',   'Aktiviteter',
     'Finn aktiviteter og tilbud fra kommunen, lag og foreninger.',
     'https://lorenskog.friskus.com/',
     'all', 50);