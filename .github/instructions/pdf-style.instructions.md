---
applyTo: "outputs/reports/**"
---
# PDF Report Style Guide — VorsorgeCoach

Alle PDF-Berichte, die in diesem Projekt erstellt werden, müssen diesen Gestaltungsrichtlinien folgen, unabhängig davon, welcher Skill sie generiert.

---

## Seitenformat

- **Format:** A4 Hochformat (210 × 297 mm)
- **Ränder:** oben 20 mm, unten 20 mm, links 20 mm, rechts 15 mm
- **Schriftart:** Helvetica (Fallback: Arial, sans-serif)
- **Grundschriftgrösse:** 10 pt, Zeilenabstand 1.4

---

## Farbpalette

| Rolle | Hex-Code | Verwendung |
|---|---|---|
| Primary (Dunkelblau) | `#1a3c5e` | Seitenkopf, H1-Hintergrund, Tabellenköpfe |
| Accent (Grün) | `#2ecc71` | Kennzahlen-Badges, Highlights, Icons |
| Light Background | `#f0f4f8` | Abwechselnde Tabellenzeilen (gerade), Info-Boxen |
| Text Dark | `#1a1a1a` | Fliesstext |
| Text Light | `#ffffff` | Text auf Primary-Hintergrund |
| Border | `#d0d8e4` | Tabellenrahmen, Trennlinien |
| Warning | `#e67e22` | Hinweise, Sperrfristen, Handlungsbedarf |

---

## Typografie

| Element | Schrift | Grösse | Farbe | Stil |
|---|---|---|---|---|
| H1 (Berichtstitel) | Helvetica Bold | 16 pt | `#ffffff` auf `#1a3c5e` | Grossbuchstaben |
| H2 (Abschnitt) | Helvetica Bold | 13 pt | `#1a3c5e` | Normal |
| H3 (Unterabschnitt) | Helvetica Bold | 11 pt | `#1a3c5e` | Normal |
| Fliesstext | Helvetica | 10 pt | `#1a1a1a` | Normal |
| Tabellenkopf | Helvetica Bold | 9 pt | `#ffffff` auf `#1a3c5e` | Normal |
| Tabelleninhalt | Helvetica | 9 pt | `#1a1a1a` | Normal |
| Fussnote / Disclaimer | Helvetica | 7.5 pt | `#666666` | Kursiv |
| Kennzahl (gross) | Helvetica Bold | 18 pt | `#1a3c5e` | Normal |

---

## Seitenkopf (Header) — jede Seite

```
┌──────────────────────────────────────────────────────────┐
│  [Logo Platzhalter — links]    VorsorgeCoach       [Datum]│
│  [Berichtstitel — H1, volle Breite, Primary-Hintergrund] │
└──────────────────────────────────────────────────────────┘
```

- **Zeile 1:** Logo links (falls vorhanden: `outputs/assets/logo.png`, Höhe 20 mm), Firmenname „VorsorgeCoach" zentriert, Datum rechts (Format: DD.MM.YYYY)
- **Zeile 2:** Berichtstitel in H1 (weiss auf `#1a3c5e`), volle Seitenbreite
- Auf Folgeseiten: schlanker Header (nur Logo + Titel, Höhe 10 mm)

---

## Seitenfuss (Footer) — jede Seite

```
┌──────────────────────────────────────────────────────────┐
│  Hinweis: orientierende Auswertung, keine Beratung.      │
│  Erstellt: YYYY-MM-DD  |  Seite N / M          Vertraulich│
└──────────────────────────────────────────────────────────┘
```

- Linkes Drittel: Kurzfassung des Disclaimers (7.5 pt, kursiv, grau)
- Mitte: Erstellungsdatum (ISO: YYYY-MM-DD)
- Rechts: Seitennummer „Seite N / M" + „Vertraulich"
- Trennlinie über dem Footer: `#d0d8e4`, 0.5 pt

---

## Pflichtabschnitte (Reihenfolge)

Jeder Bericht muss die folgenden Abschnitte in dieser Reihenfolge enthalten:

1. **Titelseite** — Klientenname, Berichtsart, Erstellungsdatum, Berichts-ID
2. **Rechtlicher Hinweis** — Volltext-Disclaimer (siehe unten)
3. **Annahmen & Datenstand** — Alle verwendeten Renditen, Steuersätze, Bewertungsdaten
4. **Hauptinhalt** — Je nach Berichtsart (Projektionen, Szenarien, Empfehlungen)
5. **Empfehlungen & nächste Schritte** — Prioritäts-Tabelle mit Frist und Verantwortlichem
6. **Berechnungsgrundlagen** — Kurznotiz zu verwendeten Tools/MCP-Servern

---

## Disclaimer-Pflichttext (Vollversion, Abschnitt 2)

> **Hinweis:** Dies ist eine orientierende Auswertung und stellt keine verbindliche Finanz- oder Rechtsberatung dar. Zur rechtsverbindlichen Beratung ist die Prüfung durch einen zugelassenen Vorsorge-/Steuerberater erforderlich. Alle Projektionen basieren auf den angegebenen Annahmen und können von der tatsächlichen Entwicklung abweichen. Steuern nach aktuell bekanntem Recht; Änderungen vorbehalten.

---

## Tabellen

- **Kopfzeile:** Hintergrund `#1a3c5e`, Text weiss, Helvetica Bold 9 pt
- **Zeilen:** abwechselnd weiss / `#f0f4f8`
- **Rahmenlinie:** `#d0d8e4`, 0.5 pt, nur horizontale Linien (keine vertikalen)
- **Zahlen:** rechtsbündig; Text und Labels: linksbündig
- **Negativwerte / Steuern:** in `#e67e22` (orange/warning)
- **Totalspalte/-zeile:** Helvetica Bold, Hintergrund `#dce8f5`

---

## Zahlen- und Währungsformatierung

- **Währung:** `CHF 1'234'567` (Apostroph als Tausendertrenner, kein Leerzeichen)
- **Prozent:** `3.50%` (zwei Dezimalstellen)
- **Datumsformat intern:** ISO `YYYY-MM-DD`
- **Datumsformat in Ausgaben:** `DD.MM.YYYY`
- **Negative Beträge:** mit Minuszeichen `CHF -5'000`, nicht in Klammern

---

## Kennzahlen-Badges (Summary-Boxen)

Für hervorgehobene Schlüsselzahlen (z.B. Gesamtvermögen, Ersatzquote):

```
┌─────────────────────┐
│  CHF 1'903'606      │  ← 18pt Bold, #1a3c5e
│  Nettovermögen      │  ← 9pt, #666666
│  bei Pensionierung  │
└─────────────────────┘
```

- Hintergrund: `#f0f4f8`, Rahmen links: 4 pt solid `#2ecc71`
- Drei bis vier Badges nebeneinander auf einer Zeile (Spaltenbreite ~45 mm)

---

## Diagramme (falls enthalten)

- **Balkendiagramme:** Primärfarbe `#1a3c5e`, Sekundärfarbe `#2ecc71`
- **Liniendiagramme:** Linie `#1a3c5e` (2 pt), Datenpunkte ausgefüllt
- **Kreisdiagramme:** Palette: `#1a3c5e`, `#2ecc71`, `#3498db`, `#e67e22`, `#95a5a6`
- Achsenbeschriftungen: Helvetica 8 pt; Titel: Helvetica Bold 9 pt
- Keine 3D-Effekte; keine Schatten

---

## Dateiname & Ablageort

```
outputs/reports/<nachname>_<YYYYMMDD>_<berichtstyp>.pdf
```

Beispiele:
- `outputs/reports/niggeler_20260305_vermoegensentwicklung.pdf`
- `outputs/reports/niggeler_20260305_rente-vs-kapital.pdf`
- `outputs/reports/niggeler_20260305_3a-zusammenfassung.pdf`

Zulässige `<berichtstyp>`-Werte: `vermoegensentwicklung`, `rente-vs-kapital`, `3a-zusammenfassung`, `pk-einkauf`, `snapshot`, `aktionsplan`
