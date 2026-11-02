# Velkommen til Lørenskog

En tjeneste som lager en personlig velkomst til nye innbyggere når de flytter til kommunen.

Tjenesten kjører i Azure, og er bygget med Python, Azure Functions og Azure SQL.

## Problemet

Kommunen har en god side for nye innbyggere, men den er lik for alle, og man må selv finne den og lete fram det som gjelder en.

Denne tjenesten gjør velkomsten automatisk og personlig. Når noen flytter inn, får de bare informasjonen som er relevant for dem. Har de barn, får de også skolen for adressen sin og informasjon om barnehage. Lenkene går til kommunens egne sider og andre offisielle tjenester.

## Slik fungerer det

![Arkitektur](docs/architecture.png)

1. Et annet system sender en flyttehendelse til API-et (webhook). I demoen simulerer jeg den.
2. Tjenesten sjekker at avsenderen kjenner den delte hemmeligheten.
3. Dataene valideres.
4. Hvis hendelsen er behandlet før, returneres den samme velkomsten. Det blir aldri to velkomster for samme hendelse.
5. Adressen slås opp i databasen for å finne skolen.
6. Tjenestene hentes fra databasen: skole og barnehage for familier med barn, og avfall, fastlege og aktiviteter for alle.
7. Velkomsten lages og lagres i Azure SQL.

## Teknologi

- Python 3.11
- Azure Functions (Flex Consumption, Norway East)
- Azure SQL Database (gratisnivå, Sweden Central)
- Managed Identity for innlogging i databasen, uten passord
- SQLite lokalt og i tester
- pytest

## Struktur

```
function_app.py     Inngangen til tjenesten
welcome/            Koden, delt i lag
  routes.py           Tar imot HTTP-kall og sjekker hemmeligheten
  models.py           Validerer flyttehendelsen
  service.py          Logikken: duplikatsjekk og velkomstmelding
  repository.py       Alle SQL-spørringer
  db.py               Kobler til Azure SQL eller lokal SQLite
database/
  sqlite/             Tabeller og testdata for lokal SQLite
  azuresql/           Tabeller og testdata for Azure SQL
scripts/init_db.py  Lager den lokale databasen
tests/              Tester
samples/            Eksempel på en flyttehendelse og demo-fil
docs/               Arkitekturdiagram
```

Koden er delt i lag, slik at hver fil har én jobb. Det gjør den lettere å teste og å endre.

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
| 200 | Hendelsen var behandlet før (samme velkomst returneres) |
| 400 | Ugyldig JSON eller manglende felt |
| 401 | Feil eller manglende hemmelighet |
| 422 | Adressen finnes ikke |

## Demo

`samples/demo.http` inneholder alle kallene. Med VS Code-utvidelsen REST Client kan de kjøres ett og ett med «Send Request».

Hemmeligheten leses fra `samples/.env`, som aldri ligger i Git:

```
WEBHOOK_SECRET=<hemmeligheten>
```

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

Sett en verdi for `WEBHOOK_SECRET` i `local.settings.json` før du starter. Lokalt brukes SQLite.

## Tester

```
python -m pytest -v
```

Testene sjekker blant annet at samme hendelse ikke gir to velkomster, og at skole bare tas med for familier med barn.

## Sikkerhet og personvern

- Tjenesten logger inn i Azure SQL med en Managed Identity, så det finnes ikke noe databasepassord.
- Tjenesten har bare lov til å lese og skrive data, ikke å endre tabeller.
- Databaseserveren tillater bare innlogging med Microsoft Entra ID.
- Alle SQL-spørringer bruker parametere, for å hindre SQL-injeksjon.
- Hemmeligheter ligger i innstillinger, ikke i koden eller i Git.
- Tjenesten lagrer bare det som trengs: navn, e-post, adresse og om man har barn.
- Logger inneholder bare hendelses-id, ikke navn eller e-post.

## Data

- Skolenavn og lenker er hentet fra lorenskog.kommune.no.
- Adressene er fiktive, og koblingen mellom adresse og skole er eksempeldata, ikke kommunens inntaksområder.

## Hva jeg lærte

Lokalt fungerte duplikatsjekken, men i Azure laget samme hendelse to velkomster. Grunnen var at tjenesten kjørte på flere instanser, og hver hadde sin egen SQLite-fil. Løsningen var å flytte til Azure SQL, slik at alle instansene deler én database.

## Videre arbeid

- Logic App som sender velkomsten på e-post, og en påminnelse etter 14 dager
- API Management foran API-et
- Flytte hemmeligheten til Azure Key Vault
- Automatisk retry når databasen våkner fra pause
- Slette gamle data automatisk
- Bruke kommunens data om inntaksområder i stedet for eksempeldata
- Strammere nettverkstilgang til databasen, for eksempel med private endpoint