# VorsorgeCoach

Ein KI-gestützter Vorsorge-Coach für das Schweizer Vorsorgesystem, der als GitHub Copilot Agent läuft.

## Übersicht

VorsorgeCoach ist ein intelligenter Assistent für die Schweizer Altersvorsorge, der komplexe Berechnungen durchführt und fundierte Beratung zu folgenden Themen bietet:

- **AHV** (Alters- und Hinterlassenenversicherung)
- **BVG** (Berufliche Vorsorge / Pensionskasse)
- **Säule 3a** (Private Vorsorge)
- **Steueroptimierung** bei Vorsorgeentscheidungen

## Funktionen

### Berechnungen
- AHV- und BVG-Rentenberechnungen
- Einkaufspotenzial in die Pensionskasse
- **PK-Einkauf Steueroptimierung** (inkl. Kapitalbezugssteuer-Berechnung)
- WEF-Bezüge (Wohneigentumsförderung)
- Vorsorgeausgleich bei Scheidung
- Steueroptimierung (Einkommens-, Vermögens-, Kapitalbezugssteuer)

### Beratung
- Auswirkungen von Lohnänderungen auf die Vorsorge
- Optimale Einkaufsstrategien (inkl. Verteilung auf mehrere Jahre)
- Vergleich Kapitalbezug vs. Rente
- Gestaffelte 3a-Bezugsstrategien
- Langfristige Finanzplanung

## Skills

VorsorgeCoach nutzt spezialisierte **Copilot Skills** für verschiedene Vorsorge-Szenarien:

### Verfügbare Skills

#### 🎯 Einkauf (PK-Einkauf Steuerrechner)
Berechnet Steuerersparnis und Netto-Vorteil bei freiwilligen PK-Einkäufen.

**Capabilities:**
- Steuerersparnis bei Einkäufen (Bund, Kanton, Gemeinde)
- Kapitalbezugssteuer-Berechnung beim späteren Bezug
- Netto-Vorteil: Steuerersparnis minus Kapitalbezugssteuer
- Verteilung auf mehrere Jahre (1-5 Jahre)
- Automatische 3-Jahres-Regel-Prüfung

**Beispiele:**
```
"Was spare ich netto wenn ich CHF 50'000 einkaufe und 2029 als Kapital beziehe?"
"Lohnt sich CHF 80'000 verteilt auf 3 Jahre vs. alles auf einmal?"
```

Siehe [skills/Einkauf/skill.md](skills/Einkauf/skill.md) für Details.

---

Weitere Skills in Planung: AHV-Berechnungen, 3a-Optimierung, WEF-Bezüge

## Technologie

- **MCP-Server**: C# (Anbindung an BVG- und Steuerrechner)
- **Skills**: Python/TypeScript (Berechnungslogik und Copilot-Integration)
- **Integration**: GitHub Copilot CLI
- **Datenschutz**: Read-only, keine Speicherung persönlicher Daten

## Projektstruktur

```
VorsorgeCoach/
├── .copilot/          # GitHub Copilot Agent Konfiguration
│   ├── skills/        # Aktivierte Copilot Skills
│   ├── mcp.json       # MCP-Server Konfiguration
│   └── skills.json    # Skills Registry
├── skills/            # Skill-Definitionen
│   ├── Einkauf/       # PK-Einkauf Steuerrechner
│   └── README.md      # Skills Übersicht
├── mcp-servers/       # MCP-Server Referenzen und Wrapper (C#)
├── docs/              # Dokumentation
├── tests/             # Tests
└── examples/          # Beispiel-Vorsorgeausweise und Szenarien
```

## Installation

```bash
# Repository klonen
git clone <repository-url>
cd VorsorgeCoach

# Dependencies installieren
npm install
pip install -r requirements.txt
```

## Verwendung

```bash
# GitHub Copilot CLI starten
gh copilot

# Beispielanfragen:
# "Berechne meine voraussichtliche AHV-Rente"
# "Wie viel kann ich in die Pensionskasse einkaufen?"
# "Was sind die steuerlichen Auswirkungen eines WEF-Bezugs?"
```

## Rechtliche Hinweise

VorsorgeCoach dient als Informations- und Planungsinstrument. Die bereitgestellten Berechnungen und Empfehlungen ersetzen keine professionelle Finanzberatung. Alle Angaben ohne Gewähr.

Die Berechnungen basieren auf den aktuellen gesetzlichen Grundlagen der Schweiz (AHV-Gesetz, BVG-Gesetz) und werden regelmäßig aktualisiert.

## Entwicklung

Dieses Projekt befindet sich in aktiver Entwicklung. Siehe [Implementierungsplan](docs/implementation-plan.md) für Details.

## Lizenz

[Lizenz hier einfügen]

## Kontakt

[Kontaktinformationen hier einfügen]
