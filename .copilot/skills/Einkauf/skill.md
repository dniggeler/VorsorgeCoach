# Pensionskassen-Einkauf & Steueroptimierung CH
{: .skill-header}

**Skill Name:** PK-Einkauf  
**Version:** 1.0  
**Beschreibung:** Berechnet die Steuerersparnis bei freiwilligen Einkäufen in die Pensionskasse (2. Säule) in der Schweiz und die spätere Kapitalbezugssteuer. Ermittelt den Netto-Vorteil unter Berücksichtigung der gesamten Steuerfolgen und liefert strukturierte JSON-Outputs für weitere Verarbeitung.

## Fähigkeiten (Capabilities)

- Berechnung der **Steuerersparnis** bei Einkäufen in die Pensionskasse (Bund + Kanton + Gemeinde)
- Berechnung der **Kapitalbezugssteuer** beim späteren Bezug des angesparten Kapitals
- **Netto-Vorteil**: Steuerersparnis minus Kapitalbezugssteuer = effektiver Gewinn durch Einkauf
- Vergleichsrechnung: Steuerlast **mit Einkauf** vs. **ohne Einkauf**
- Unterstützung für **mehrere Einkaufsszenarien** (verschiedene Beträge parallel vergleichen)
- **Verteilung des Einkaufs** auf mehrere Jahre (1–5 Jahre) mit automatischer Berechnung der Steuerersparnis pro Jahr
- Automatische Prüfung der **3-Jahres-Regel** zwischen letztem Einkauf und Kapitalbezug
- Strukturierte **JSON-Ausgabe** für Weiterverarbeitung und Reporting
- Berücksichtigung von Zivilstand, Kindern, Kirchensteuer und Gemeindesteuer

## Verfügbare Tools / Backends

- **swisstax-rechner** (MCP-Server)
  - `search_municipalities`: Suche nach Gemeinden für korrekte taxLocationId
  - `calculate_wealth_and_income_tax`: Berechnung der Einkommens- und Vermögenssteuer
  - `calculate_capital_benefit_tax`: Berechnung der Kapitalbezugssteuer (Kapitalleistung aus Vorsorge)
  - Zugriff auf aktuelle Steuertabellen (Bund + alle Kantone + viele Gemeinden)
  - Unterstützt Zivilstand, Kinder, Kirchensteuer, religiöse Zugehörigkeit

## Beispieleingaben (Trigger / Intents)

- „Was spare ich netto wenn ich CHF 50'000 einkaufe und 2029 als Kapital beziehe? Zürich, verheiratet"
- „Lohnt sich ein Einkauf von CHF 80'000 verteilt auf 3 Jahre vs. alles auf einmal? Bezug 2030"
- „Ich kaufe CHF 60'000 ein und beziehe 2028 – was bleibt nach Kapitalbezugssteuer übrig?"
- „Vergleich: CHF 40'000 Einkauf in 2026 mit Bezug 2029 vs. kein Einkauf"
- „Steuerersparnis bei CHF 100'000 verteilt auf 5 Jahre, Bezug 2032, Single, Zürich"

## Antwortstil-Vorgaben

- **JSON-Ausgabe** als primäres Format (strukturiert, maschinenlesbar)
- Immer mit **kantonaler und kommunaler Steuerbelastung** rechnen (wenn Gemeinde nicht angegeben → nachfragen oder Kantonshauptort verwenden)
- **Netto-Vorteil prominent darstellen**: Steuerersparnis − Kapitalbezugssteuer = effektiver Gewinn
- Steuerersparnis aufschlüsseln nach:
  - Bundessteuer
  - Kantonssteuer
  - Gemeindesteuer
  - Kirchensteuer (falls zutreffend)
  - **Gesamt-Ersparnis** (über alle Einkaufsjahre summiert)
- Kapitalbezugssteuer aufschlüsseln nach:
  - Bundessteuer
  - Kantonssteuer
  - Gemeindesteuer
  - **Gesamt-Kapitalbezugssteuer**
- Wichtige Annahmen dokumentieren:
  - Einkaufsjahre (z.B. 2026, 2027, 2028)
  - Bezugsjahr (z.B. 2030)
  - Verwendete taxLocationId
  - Zivilstand und Kinderanzahl
- **3-Jahres-Regel automatisch prüfen**: Warnung wenn Bezugsjahr < (letztes Einkaufsjahr + 3)
- Bei Verteilung auf mehrere Jahre: optimale Aufteilung vorschlagen (gleiche Raten oder progressionsoptimiert)
- Alle Geldbeträge in **CHF** mit Tausendertrennung durch Apostroph (z.B. CHF 50'000)

## Benötigte Parameter (Slots)

| Slot                     | Beispielwert              | Pflicht? | Bemerkung                              |
|--------------------------|----------------------------|----------|----------------------------------------|
| calculationYear          | 2026                      | ja       | Erstes Einkaufsjahr (Default: aktuelles Jahr) |
| verteilungsJahre         | 1, 3, 5                   | nein     | Einkauf auf n Jahre verteilen (Default: 1 = alles sofort) |
| bezugsjahr               | 2030, 2035                | nein     | Jahr des Kapitalbezugs (falls angegeben → Kapitalbezugssteuer wird berechnet) |
| taxLocationId            | (von search_municipalities)| ja       | ESTV ID der Gemeinde                   |
| kanton                   | Zürich, Genf, Bern, ...   | ja       | für Gemeindesuche                      |
| gemeinde                 | Zürich, Winterthur, ...   | empf.    | falls nicht angegeben → Kantonshauptort|
| zivilstand               | Single, Married           | ja       | beeinflusst Steuerprogression stark    |
| numberOfChildren         | 0, 1, 2, 3                | ja       | Kinderabzüge (Default: 0)              |
| taxableIncome            | 196'000                   | ja       | Jahreseinkommen **ohne Einkauf**       |
| taxableFederalIncome     | 196'000                   | ja       | Bundessteuerpflichtiges Einkommen      |
| taxableWealth            | 0                         | ja       | Vermögen (Default: 0)                  |
| einkaufsbetrag           | 40'000, 80'000            | ja       | **Gesamt-Einkaufsbetrag** (wird ggf. auf Jahre verteilt) |
| bestehendesKapital       | 191'000                   | nein     | Vorhandenes PK-Kapital vor Einkauf (für Kapitalbezugssteuer) |
| religiousGroupType       | Other, Protestant, Catholic| nein     | für Kirchensteuer (Default: Other)     |

## Wichtige Formeln / Regeln (Referenz)

### Steuerersparnis pro Jahr
- **Steuerersparnis(Jahr i)** = Steuerlast(ohne Einkauf) − Steuerlast(mit Einkauf im Jahr i)
- Einkauf reduziert das **steuerpflichtige Einkommen** direkt (Abzug vom Bruttoeinkommen)
- Typische Steuerersparnis: **30–45%** des Einkaufsbetrags (abhängig von Grenzsteuersatz)
- Bei Verteilung auf n Jahre: Einkauf pro Jahr = Gesamtbetrag ÷ n (Standardfall: gleiche Raten)

### Kapitalbezugssteuer
- **Kapitalbezugssteuer** = Steuer auf (bestehendesKapital + einkaufsbetrag) beim Bezug
- Separater Steuersatz für Kapitalleistungen (meist niedriger als Einkommenssteuersatz)
- Berechnung mit `calculate_capital_benefit_tax` für das Bezugsjahr

### Netto-Vorteil (effektiver Gewinn)
- **Netto-Vorteil** = Σ Steuerersparnis(alle Einkaufsjahre) − Kapitalbezugssteuer
- **Rendite** ≈ Netto-Vorteil ÷ einkaufsbetrag × 100%
- Positiver Netto-Vorteil → Einkauf lohnt sich
- Negativer Netto-Vorteil → Einkauf kostet mehr als er bringt

### Compliance-Regeln
- **3-Jahres-Regel**: mind. 3 volle Jahre zwischen **letztem** Einkauf und Kapitalbezug (sonst Rückforderung der Steuerersparnis)
- **5-Jahres-Regel**: bei mehreren großen Einkäufen in kurzer Zeit kann Progressionsbremse greifen

## JSON Output-Format

```json
{
  "eingabe": {
    "einkaufsbetrag_gesamt": 50000,
    "verteilungsJahre": 1,
    "einkaufsjahre": [2026],
    "bezugsjahr": 2029,
    "location": "Zürich (ZH)",
    "taxLocationId": 261,
    "person": {
      "civilStatus": "Married",
      "numberOfChildren": 0,
      "jahreseinkommen": 196000
    }
  },
  "steuerersparnis_einkauf": {
    "jahre": [
      {
        "jahr": 2026,
        "einkaufsbetrag": 50000,
        "steuerlast_ohne_einkauf": 45230,
        "steuerlast_mit_einkauf": 28760,
        "ersparnis": 16470,
        "breakdown": {
          "federal": 4300,
          "cantonal": 8000,
          "municipal": 4170
        }
      }
    ],
    "gesamt_steuerersparnis": 16470
  },
  "kapitalbezugssteuer": {
    "bezugsjahr": 2029,
    "kapital_ohne_einkauf": 191000,
    "kapital_mit_einkauf": 241000,
    "steuer_ohne_einkauf": 8450,
    "steuer_mit_einkauf": 11280,
    "mehrsteuer_durch_einkauf": 2830,
    "breakdown": {
      "federal": 980,
      "cantonal": 1200,
      "municipal": 650
    }
  },
  "netto_vorteil": {
    "steuerersparnis_gesamt": 16470,
    "kapitalbezugssteuer_mehrkosten": 2830,
    "netto_gewinn": 13640,
    "rendite_prozent": "27.28%",
    "interpretation": "Der Einkauf lohnt sich: CHF 13'640 effektiver Steuervorteil"
  },
  "compliance_check": {
    "letzter_einkauf": 2026,
    "bezugsjahr": 2029,
    "jahre_dazwischen": 3,
    "dreijahresregel_erfuellt": true,
    "warnung": null
  },
  "hinweise": [
    "3-Jahres-Regel erfüllt: 3 Jahre zwischen Einkauf und Bezug",
    "Netto-Vorteil positiv: Einkauf empfohlen",
    "Alternative prüfen: Verteilung auf 2–3 Jahre könnte Progression weiter optimieren"
  ]
}
```

## Workflow (Orchestrierung)

### Phase 1: Vorbereitung
1. **Gemeinde-ID ermitteln**: `search_municipalities` mit Kanton und Gemeindename
2. **Einkauf aufteilen**: Wenn `verteilungsJahre` > 1 → Einkaufsbetrag gleichmäßig auf Jahre verteilen
3. **3-Jahres-Regel prüfen**: Falls `bezugsjahr` angegeben → Check ob (bezugsjahr − letztes_einkaufsjahr) ≥ 3

### Phase 2: Steuerersparnis berechnen (für jedes Einkaufsjahr)
4. **Steuerlast ohne Einkauf**: `calculate_wealth_and_income_tax` mit vollem Einkommen
5. **Steuerlast mit Einkauf**: `calculate_wealth_and_income_tax` mit reduziertem Einkommen (−Jahres-Einkaufsbetrag)
6. **Ersparnis pro Jahr**: Differenz = Steuerlast(ohne) − Steuerlast(mit)
7. **Summe über alle Jahre**: Gesamt-Steuerersparnis aufsummieren

### Phase 3: Kapitalbezugssteuer berechnen (optional, falls Bezugsjahr angegeben)
8. **Kapital ohne Einkauf**: bestehendesKapital beim Bezugsjahr
9. **Kapital mit Einkauf**: bestehendesKapital + einkaufsbetrag_gesamt
10. **Kapitalbezugssteuer ohne Einkauf**: `calculate_capital_benefit_tax` mit Kapital_ohne
11. **Kapitalbezugssteuer mit Einkauf**: `calculate_capital_benefit_tax` mit Kapital_mit
12. **Mehrkosten**: Kapitalbezugssteuer(mit) − Kapitalbezugssteuer(ohne)

### Phase 4: Netto-Vorteil ermitteln
13. **Netto-Gewinn berechnen**: Gesamt-Steuerersparnis − Kapitalbezugssteuer-Mehrkosten
14. **Rendite berechnen**: (Netto-Gewinn ÷ einkaufsbetrag_gesamt) × 100%
15. **Interpretation**: Positiv/Negativ, Empfehlung aussprechen

### Phase 5: Output & Human-in-Loop
16. **JSON-Output generieren**: Strukturierte Ausgabe mit allen Details
17. **Warnungen**: 3-Jahres-Regel verletzt, negative Rendite, große Beträge
18. **Human-in-Loop**: Bei Beträgen >CHF 80'000 oder negativem Netto-Vorteil → Empfehlung zur Fachberatung

## Einschränkungen / Disclaimer

- Keine individuelle Steuerberatung – nur indikative Berechnungen
- Steuersätze und Freibeträge können sich ändern (Stand Februar 2026)
- **Der maximal mögliche Einkaufsbetrag** wird NICHT berechnet (muss als Input bekannt sein)
- **Zukünftige Einkommen/Steuersätze**: Berechnungen für zukünftige Jahre basieren auf heutigen Steuersätzen
- **Kapitalrendite**: Keine Berücksichtigung der Verzinsung des PK-Guthabens zwischen Einkauf und Bezug
- **Umwandlungssatz**: Keine Berechnung von Rentenoptionen (nur Kapitalbezug)
- Komplexe Fälle (Selbständige, mehrere PK, Vorbezüge, Scheidung) erfordern Fachberatung
- Keine Berücksichtigung von AHV-Beiträgen auf Einkauf
