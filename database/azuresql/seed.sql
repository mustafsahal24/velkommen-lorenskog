-- Testdata for Velkommen til Lørenskog (Azure SQL / T-SQL).
-- Samme data som seed.sql. N foran teksten gjør at æ, ø og å lagres riktig.
-- Koblingen mellom adresse og skole er EKSEMPELDATA, ikke kommunens inntaksområder.

-- Skolekretser (barneskoler)
INSERT INTO school_districts (id, school_name, url) VALUES
    (1, N'Benterud skole',   N'https://www.lorenskog.kommune.no/benterud-skole'),
    (2, N'Fjellhamar skole', N'https://www.lorenskog.kommune.no/fjellhamar-skole'),
    (3, N'Rasta skole',      N'https://www.lorenskog.kommune.no/rasta-skole');

-- Adresser (fiktive gatenavn, kun for demo)
INSERT INTO addresses (id, street, postal_code, school_district_id) VALUES
    (1, N'Eksempelveien 1', N'1470', 1),
    (2, N'Eksempelveien 2', N'1470', 1),
    (3, N'Testgata 10',     N'1472', 2),
    (4, N'Demostien 5',     N'1473', 3);

-- Tjenester i velkomsten (lenker hentet fra kommunens side "Ny i Lørenskog")
INSERT INTO services (category, title, description, url, audience, sort_order) VALUES
    (N'school',       N'Skoletilhørighet',
     N'Kart over inntaksområder, skolestart og bytte av skole.',
     N'https://www.lorenskog.kommune.no/tjenester/barnehage-og-skole/skole/skoletilhorighet-bytte-skole/',
     N'families', 10),
    (N'kindergarten', N'Barnehage',
     N'Les om barnehagetilbudet i kommunen og hvordan du søker plass.',
     N'https://www.lorenskog.kommune.no/tjenester/barnehage-og-skole/barnehage/',
     N'families', 20),
    (N'waste',        N'Avfall og renovasjon',
     N'ROAF håndterer husholdningsavfallet. Se hva du kan kaste og hvor.',
     N'https://www.roaf.no/',
     N'all', 30),
    (N'gp',           N'Fastlege',
     N'Velg fastlege på Helsenorge.',
     N'https://www.helsenorge.no/fastlegen/',
     N'all', 40),
    (N'activities',   N'Aktiviteter',
     N'Finn aktiviteter og tilbud fra kommunen, lag og foreninger.',
     N'https://lorenskog.friskus.com/',
     N'all', 50);