
# Velkommen til Lørenskog

En liten tjeneste som sender en personlig velkomst til nye innbyggere når de flytter til kommunen.

Jeg laget prosjektet for å lære og vise hvordan man kan bygge en integrasjon med Azure Functions, Python og SQL.

## Problemet

Kommunen har en god velkomstside for nye innbyggere, men den er lik for alle, og man må selv finne den og lete fram det som gjelder en.

Tjenesten gjør velkomsten automatisk og personlig: når noen flytter inn, får de bare informasjonen som er relevant for dem. Har de barn, får de også skolen for adressen sin og informasjon om barnehage.

## Hvordan det fungerer

1. Et annet system sender en flyttehendelse til API-et (webhook). I denne demoen simulerer jeg den.
2. API-et sjekker at avsenderen er godkjent og at dataene er gyldige.
3. Hvis hendelsen er behandlet før, returneres den samme velkomsten (ingen duplikater).
4. Adressen slås opp i databasen for å finne skolen.
5. Det lages en velkomstmelding med lenker til kommunens egne sider, og den lagres.

## Teknologi

- Python 3.11
- Azure Functions (HTTP-triggere)
- SQLite lokalt (planen er Azure SQL)
- pytest

## Struktur

```
welcome/       Applikasjonen
  routes.py      HTTP-endepunktene
  models.py      Validering av flyttehendelsen
  service.py     Logikken som lager velkomsten
  repository.py  Alle databasespørringer
  db.py          Databasetilkobling
database/      Tabeller (schema.sql) og testdata (seed.sql)
scripts/       init_db.py lager databasen lokalt
tests/         Tester
samples/       Eksempel på en flyttehendelse
```

Jeg har delt koden i lag, slik at hver fil har én jobb. Da er den lettere å teste og å endre, for eksempel ved bytte fra SQLite til Azure SQL.

## API

| Metode | Adresse | Beskrivelse |
|---|---|---|
| GET | `/api/health` | Viser at tjenesten kjører |
| POST | `/api/events/move-in` | Tar imot en flyttehendelse og lager en velkomst |
| GET | `/api/welcome/{id}` | Henter en velkomst |

`POST /api/events/move-in` krever headeren `X-Webhook-Secret`.

| Statuskode | Når |
|---|---|
| 201 | Ny velkomst laget |
| 200 | Hendelsen var behandlet før |
| 400 | Ugyldig JSON eller manglende felt |
| 401 | Feil eller manglende hemmelighet |
| 422 | Adressen finnes ikke |

## Kjøre lokalt

Krav: Python 3.11 og Azure Functions Core Tools.

```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy local.settings.example.json local.settings.json
python scripts/init_db.py
func start
```

Sett en verdi for `WEBHOOK_SECRET` i `local.settings.json` før du starter.

Send en flyttehendelse:

```
curl.exe -i -X POST http://localhost:7071/api/events/move-in -H "Content-Type: application/json" -H "X-Webhook-Secret: <din hemmelighet>" --data "@samples/move-in.json"
```

## Tester

```
python -m pytest -v
```

Testene sjekker blant annet at samme hendelse ikke gir to velkomster, og at skole bare tas med for familier med barn.

## Data og personvern

- Skolenavn og lenker er hentet fra lorenskog.kommune.no.
- Adressene er fiktive, og koblingen mellom adresse og skole er eksempeldata, ikke kommunens inntaksområder.
- Tjenesten lagrer bare det som trengs for å sende velkomsten: navn, e-post, adresse og om man har barn.
- Logger inneholder bare hendelses-id, ikke navn eller e-post.
- Hemmeligheter ligger i innstillinger utenfor koden, ikke i Git.

## Videre arbeid

- Publisere til Azure og bytte til Azure SQL
- Flytte hemmeligheten til Azure Key Vault
- Logic App som sender velkomsten på e-post og en påminnelse etter 14 dager
- API Management foran API-et
- Slette gamle data automatisk