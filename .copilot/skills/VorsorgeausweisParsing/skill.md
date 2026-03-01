---
name: vorsorgeausweis-parsing
description: Extrahiert strukturierte Pensionskassen-Daten aus Vorsorgeausweis-PDFs. Verwende diesen Skill wenn ein Vorsorgeausweis, ein PK-Dokument oder eine PDF-Datei geparst oder analysiert werden soll.
---

# Vorsorgeausweis Parsing & Datenextraktion

## Fähigkeiten (Capabilities)

- **PDF direkt analysieren** ohne manuelle Textextraktion (Anthropic Document API)
- Extraktion aller relevanten Felder aus dem Vorsorgeausweis:
  - Personalien (Name, Geburtsdatum, AHV-Nummer, Zivilstand, Eintrittsdatum)
  - Versicherter Lohn (Lohn 1 & 2)
  - Altersleistungen (Rente, Kapital, projizierte Werte bei vorzeitiger Pensionierung)
  - Leistungen bei Invalidität und Todesfall
  - Finanzierung (Sparbeiträge, Risikoprämien, Altersguthaben per Datum)
  - Einkaufspotenzial (maximale Einlage, Wohneigentumsförderung)
- Ausgabe als **strukturierte Markdown-Datei** im kanonischen Format
- Automatische Erkennung fehlender oder unplausibler Felder mit Rückfragen
- Unterstützung mehrerer Vorsorgeausweise (verschiedene Pensionskassen) pro Klient

## Anthropic Document Skills – Integration

Dieses Skill verwendet die **Anthropic Document API** (`document`-Content-Type), um PDF-Dokumente direkt an Claude zu übergeben – ohne Vorverarbeitung durch externe Bibliotheken.

### API-Verwendung

```json
{
  "role": "user",
  "content": [
    {
      "type": "document",
      "source": {
        "type": "base64",
        "media_type": "application/pdf",
        "data": "<BASE64_ENCODED_PDF>"
      },
      "title": "Vorsorgeausweis 2025",
      "context": "Schweizer Pensionskassen-Vorsorgeausweis. Extrahiere alle Felder gemäss dem kanonischen Datenmodell.",
      "citations": { "enabled": true }
    },
    {
      "type": "text",
      "text": "Extrahiere alle Vorsorgedaten aus diesem Vorsorgeausweis als strukturierte Markdown-Datei gemäss dem definierten Ausgabeformat."
    }
  ]
}
```

### Unterstützte Quellformate

| Format       | source.type | Bemerkung                                      |
|--------------|-------------|------------------------------------------------|
| PDF (lokal)  | `base64`    | Datei einlesen, Base64-kodieren, hochladen     |
| PDF (URL)    | `url`       | Direkter Link zu öffentlich zugänglichem PDF   |
| Files API    | `file`      | Vorab hochgeladene Datei via Anthropic Files API (`file_id`) |

### Python-Snippet (base64)

```python
import anthropic, base64, pathlib

client = anthropic.Anthropic()

pdf_data = base64.standard_b64encode(
    pathlib.Path("docs/va-2025.pdf").read_bytes()
).decode("utf-8")

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data},
                    "title": "Vorsorgeausweis 2025",
                    "citations": {"enabled": True},
                },
                {"type": "text", "text": "Extrahiere alle Vorsorgedaten als Markdown."},
            ],
        }
    ],
)
print(message.content[0].text)
```

## Beispieleingaben (Trigger / Intents)

- „Lade diesen Vorsorgeausweis hoch und extrahiere alle Daten strukturiert"
- „Parse den VA von [Klient] und gib die Markdown-Zusammenfassung zurück"
- „Welches Altersguthaben weist der Vorsorgeausweis aus?"
- „Extrahiere Einkaufspotenzial aus dem angehängten Vorsorgeausweis-PDF"
- „Wie hoch ist die projizierte Altersrente laut Vorsorgeausweis?"

## Benötigte Parameter (Slots)

| Slot              | Beispielwert              | Pflicht? | Bemerkung                                         |
|-------------------|--------------------------|----------|---------------------------------------------------|
| dokumentQuelle    | Pfad, URL oder file_id   | ja       | Lokale PDF-Datei, URL oder Anthropic Files API ID |
| gueltigkeitsDatum | 2025-12-31               | nein     | Stichtag des Ausweises (Default: aus Dokument)    |
| klientId          | niggeler_dieter          | nein     | Für Dateinamen und Protokollierung                |

## Ausgabeformat (kanonisches Markdown)

```markdown
# Vorsorgeausweis — [Nachname Vorname]

**Quelle:** va-2025.pdf  
**Extrahiert am:** 2026-03-01  
**Gültig ab:** 2025-12-31  
**Arbeitgeber:** PayrollPlus AG — Vertrags-Nr.: 105808 — Plan-Nr.: 10408184

---

## Personalien

| Feld             | Wert                  |
|------------------|-----------------------|
| Nachname         | Niggeler              |
| Vorname          | Dieter                |
| Geburtsdatum     | 1969-03-17            |
| AHV-Nummer       | 756.5179.2300.83      |
| Eintritt         | 2019-02-01            |
| Zivilstand       | ledig                 |
| Geschlecht       | Mann                  |

## Versicherter Lohn

| Lohn 1 (CHF) | Lohn 2 (CHF) |
|--------------|--------------|
| 211'888      | 211'888      |

## Leistungen im Alter

- **Pensionierungsdatum:** 2034-03-31 (Alter 65)
- **Jährliche Altersrente:** CHF 80'979
- **Projiziertes Kapital (1.50%):** CHF 1'396'193
- **Kinder-Rente:** CHF 16'196

### Vorzeitige Pensionierung

| Alter | Rente (CHF) | Kapital (CHF) |
|-------|-------------|---------------|
| 64    | 74'927      | 1'337'984     |
| 63    | 69'154      | 1'280'635     |
| 62    | 63'655      | 1'224'133     |
| 61    | 58'423      | 1'168'466     |
| 60    | 53'454      | 1'113'622     |

## Leistungen bei Invalidität

| Feld                    | Wert (CHF) |
|-------------------------|------------|
| Jährliche Rente         | 105'944    |
| Kinder-Rente            | 21'189     |
| Wartezeit               | 12 Monate  |

## Leistungen im Todesfall

| Feld                                    | Wert (CHF) |
|-----------------------------------------|------------|
| Partner-Rente vor Pensionierung         | 63'566     |
| Partner-Rente nach Pensionierung        | 48'588     |
| Waisen-Rente                            | 21'189     |
| Todesfallkapital                        | 940'842    |
| Zusätzliches Todesfallkapital           | 383'078    |

## Finanzierung

| Feld                             | Wert (CHF)   |
|----------------------------------|--------------|
| Sparbeitrag 2025                 | 34'961.35    |
| Risikoprämie 2025                | 7'380.75     |
| Verwaltungskosten                | 368.50       |
| Gesamtaufwand                    | 42'710.60    |
| Altersguthaben BVG               | 182'996.85   |
| Altersguthaben Total             | 823'219.75   |
| Freizügigkeitsleistung BVG       | 196'344.70   |
| Freizügigkeitsleistung Total     | 940'839.00   |

### Einkäufe

| Datum      | Betrag (CHF) |
|------------|--------------|
| 2025-08-13 | 50'000       |
| 2025-12-01 | 20'000       |

## Einkaufspotenzial

| Feld                      | Wert (CHF) |
|---------------------------|------------|
| Maximaler Vorbezug        | 385'250    |
| Maximale mögliche Einlage | 0          |
| Mindesteinlage            | 0          |

---

## Hinweise / Fehlende Felder

_(keine)_
```

## Workflow (Orchestrierung)

### Phase 1: Dokument laden
1. **Quellformat bestimmen**: Lokale Datei → Base64; URL → `url`-Typ; Files API → `file_id`
2. **Bei lokalem PDF**: `pathlib.Path(...).read_bytes()` → `base64.standard_b64encode(...).decode()`
3. **Datei validieren**: Nur PDFs (application/pdf) werden als Vorsorgeausweise akzeptiert

### Phase 2: Extraktion via Anthropic Document API
4. **API-Aufruf** mit `document`-Content-Block und Extraktions-Prompt
5. **Citations aktivieren** (`citations: {enabled: true}`) für Quellenreferenz pro Feld
6. **Modell**: `claude-opus-4-5` (bevorzugt für komplexe Dokumente), Fallback `claude-sonnet-4-5`

### Phase 3: Validierung & Bereinigung
7. **Markdown parsen** aus Claude-Antwort
8. **Pflichtfelder prüfen**: Name, Geburtsdatum, Versicherter Lohn, Altersguthaben
9. **Plausibilitätsprüfung**: Kapital > 0, Rente > 0, Datum ≤ heute
10. **Fehlende Felder**: Im Abschnitt „Hinweise / Fehlende Felder" auflisten → Rückfrage an Berater

### Phase 4: Output & Weitergabe
11. **Markdown speichern**: `outputs/data/<klientId>_va_<datum>.md`
12. **An andere Skills übergeben**: Einkauf-Skill, Projektion-Skill, Snapshot-Skill
13. **Human-in-Loop**: Berater bestätigt extrahierte Daten vor irreversiblen Aktionen

## Einschränkungen / Disclaimer

- Anthropic Document API unterstützt PDFs bis **32 MB** und bis zu **100 Seiten**
- Qualität der Extraktion abhängig von PDF-Format (gedruckt/digitalisiert, Qualität)
- Handschriftliche oder stark tabellarisierte Dokumente können unvollständig extrahiert werden
- **Keine Speicherung von PII** ohne explizite Beraterzustimmung
- Extrahierte Daten sind **nicht rechtsverbindlich** – immer Originalausweis als Quelle behalten
- Ältere Vorsorgeausweise (vor 2015) können abweichende Felder enthalten

## Hinweis (Sicherheit & Datenschutz)

> **Wichtig:** Vorsorgeausweise enthalten sensitive Personendaten (AHV-Nummer, Lohn, Kapital).  
> PDF-Dateien werden direkt an die Anthropic API gesendet. Stelle sicher, dass die Anthropic-Datenschutzrichtlinien (Data Privacy) für produktive Klientendaten akzeptiert wurden und die entsprechende API-Vereinbarung (Privacy Addendum) vorliegt.  
> Für Tests immer anonymisierte/fiktive Dokumente verwenden.
