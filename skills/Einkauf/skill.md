# Pensionskassen-Einkauf & Steueroptimierung CH
{: .skill-header}

**Skill Name:** PK-Einkauf Steuerrechner  
**Version:** 1.1  
**Beschreibung:** Berechnet die Steuerersparnis bei freiwilligen Einkäufen in die Pensionskasse (2. Säule) in der Schweiz. Vergleicht Steuerbelastung mit und ohne Einkauf und liefert strukturierte JSON-Outputs für weitere Verarbeitung.

## Fähigkeiten (Capabilities)

- Berechnung der **Steuerersparnis** bei Einkäufen in die Pensionskasse (Bund + Kanton + Gemeinde)
- Vergleichsrechnung: Steuerlast **mit Einkauf** vs. **ohne Einkauf**
- Unterstützung für **mehrere Einkaufsszenarien** (verschiedene Beträge parallel vergleichen)
- Berechnung über **mehrere Vorsorgejahre** (Einkäufe verteilt über 3–5 Jahre)
- Strukturierte **JSON-Ausgabe** für Weiterverarbeitung und Reporting
- Berücksichtigung von Zivilstand, Kindern, Kirchensteuer und Gemeindesteuer

## Verfügbare Tools / Backends

- **swisstax-rechner** (MCP-Server)
  - `search_municipalities`: Suche nach Gemeinden für korrekte taxLocationId
  - `calculate_wealth_and_income_tax`: Berechnung der Einkommens- und Vermögenssteuer
  - Zugriff auf aktuelle Steuertabellen (Bund + alle Kantone + viele Gemeinden)
  - Unterstützt Zivilstand, Kinder, Kirchensteuer, religiöse Zugehörigkeit

## Beispieleingaben (Trigger / Intents)

- „Was spare ich an Steuern wenn ich CHF 50'000 einkaufe? Kanton Zürich, verheiratet, 2 Kinder"
- „Vergleich: CHF 40'000 Einkauf in 2026 vs. 2027 – was ist steuerlich günstiger?"
- „Ich kann CHF 80'000 einkaufen – lohnt sich das steuerlich oder soll ich es verteilen?"
- „Steuerersparnis bei CHF 60'000 Einkauf, Single, Zürich, keine Kinder"
- „Soll ich 2026 + 2027 je CHF 40'000 einkaufen oder 2026 CHF 80'000 auf einmal?"

## Antwortstil-Vorgaben

- **JSON-Ausgabe** als primäres Format (strukturiert, maschinenlesbar)
- Immer mit **kantonaler und kommunaler Steuerbelastung** rechnen (wenn Gemeinde nicht angegeben → nachfragen oder Kantonshauptort verwenden)
- Steuerersparnis aufschlüsseln nach:
  - Bundessteuer
  - Kantonssteuer
  - Gemeindesteuer
  - Kirchensteuer (falls zutreffend)
  - **Gesamt-Ersparnis**
- Wichtige Annahmen dokumentieren:
  - Steuerjahr (z.B. 2026, 2027)
  - Verwendete taxLocationId
  - Zivilstand und Kinderanzahl
- Bei großen Beträgen (>CHF 80'000–100'000) auf **3-Jahres-Regel** und **5-Jahres-Regel** hinweisen
- Alle Geldbeträge in **CHF** mit Tausendertrennung durch Apostroph (z.B. CHF 50'000)

## Benötigte Parameter (Slots)

| Slot                     | Beispielwert              | Pflicht? | Bemerkung                              |
|--------------------------|----------------------------|----------|----------------------------------------|
| calculationYear          | 2026, 2027                | ja       | Steuerjahr für die Berechnung          |
| taxLocationId            | (von search_municipalities)| ja       | ESTV ID der Gemeinde                   |
| kanton                   | Zürich, Genf, Bern, ...   | ja       | für Gemeindesuche                      |
| gemeinde                 | Zürich, Winterthur, ...   | empf.    | falls nicht angegeben → Kantonshauptort|
| zivilstand               | Single, Married           | ja       | beeinflusst Steuerprogression stark    |
| numberOfChildren         | 0, 1, 2, 3                | ja       | Kinderabzüge (Default: 0)              |
| taxableIncome            | 196'000                   | ja       | Einkommen **ohne Einkauf**             |
| taxableFederalIncome     | 196'000                   | ja       | Bundessteuerpflichtiges Einkommen      |
| taxableWealth            | 0                         | ja       | Vermögen (Default: 0)                  |
| einkaufsbetrag           | 40'000, 80'000            | ja       | **gewünschter PK-Einkauf**             |
| religiousGroupType       | Other, Protestant, Catholic| nein     | für Kirchensteuer (Default: Other)     |

## Wichtige Formeln / Regeln (Referenz)

- **Steuerersparnis** = Steuerlast(ohne Einkauf) − Steuerlast(mit Einkauf)
- Einkauf reduziert das **steuerpflichtige Einkommen** direkt (Abzug vom Bruttoeinkommen)
- Typische Steuerersparnis: **30–45%** des Einkaufsbetrags (abhängig von Grenzsteuersatz)
- **3-Jahres-Regel**: mind. 3 volle Jahre zwischen Einkauf und Kapitalbezug (sonst Rückforderung)
- **5-Jahres-Regel**: bei mehreren großen Einkäufen in kurzer Zeit (Progressionsbremse)
- Berechnung erfolgt zweimal:
  1. `taxableIncome` = Einkommen ohne Einkauf
  2. `taxableIncome - einkaufsbetrag` = Einkommen mit Einkauf

## JSON Output-Format

```json
{
  "calculationYear": 2026,
  "location": "Zürich (ZH)",
  "taxLocationId": 261,
  "person": {
    "civilStatus": "Married",
    "numberOfChildren": 0
  },
  "scenario_ohne_einkauf": {
    "taxableIncome": 196000,
    "totalTax": 45230,
    "breakdown": {
      "federalTax": 12500,
      "cantonalTax": 21800,
      "municipalTax": 10930
    }
  },
  "scenario_mit_einkauf": {
    "einkaufsbetrag": 50000,
    "taxableIncome": 146000,
    "totalTax": 28760,
    "breakdown": {
      "federalTax": 8200,
      "cantonalTax": 13800,
      "municipalTax": 6760
    }
  },
  "steuerersparnis": {
    "total": 16470,
    "effectiveRate": "32.94%",
    "federal": 4300,
    "cantonal": 8000,
    "municipal": 4170
  },
  "hinweise": [
    "3-Jahres-Regel beachten: Einkauf mind. 3 Jahre vor Kapitalbezug",
    "Einkaufsbetrag > CHF 50'000: Prüfen ob Verteilung über mehrere Jahre steuerlich günstiger"
  ]
}
```

## Workflow (Orchestrierung)

1. **Gemeinde-ID ermitteln**: `search_municipalities` mit Kanton und Gemeindename
2. **Steuerlast ohne Einkauf**: `calculate_wealth_and_income_tax` mit vollem Einkommen
3. **Steuerlast mit Einkauf**: `calculate_wealth_and_income_tax` mit reduziertem Einkommen (−Einkaufsbetrag)
4. **Differenz berechnen**: Steuerersparnis = Steuerlast(ohne) − Steuerlast(mit)
5. **JSON-Output generieren**: Strukturierte Ausgabe mit allen Details
6. **Human-in-Loop**: Bei Beträgen >CHF 80'000 → Empfehlung zur Beratung durch Steuerexperten

## Einschränkungen / Disclaimer

- Keine individuelle Steuerberatung – nur indikative Berechnungen
- Steuersätze und Freibeträge können sich ändern (Stand Februar 2026)
- **Der maximal mögliche Einkaufsbetrag** wird NICHT berechnet (muss als Input bekannt sein)
- Komplexe Fälle (Selbständige, mehrere PK, Vorbezüge, Scheidung) erfordern Fachberatung
- Keine Berücksichtigung von AHV-Beiträgen auf Einkauf
