# VorsorgeCoach - Implementierungsplan

## Übersicht
Ein KI-gestützter Vorsorge-Coach für das Schweizer Vorsorgesystem, der als GitHub Copilot Agent läuft und später als eigenständige Applikation ausgebaut wird.

## Zielsystem
- **Primär**: GitHub Copilot CLI Integration
- **Sekundär**: Eigenständige Applikation (mit GitHub Copilot SDK)
- **Tech Stack**: C# (MCP-Server), Python/TypeScript (Skills)
- **Funktionsumfang**: Beratung und Berechnungen (read-only)

## Abgedeckte Vorsorgethemen
1. **AHV** (Alters- und Hinterlassenenversicherung)
2. **BVG** (Berufliche Vorsorge)
3. **FZL** (Frühzeitige Leistungen)
4. **3a Säule** (Private Vorsorge)

## Kernfunktionen
- ✅ Berechnung von Leistungen und Vorsorgewerten aus Vorsorgeplänen/-ausweisen
- ✅ Beratung zu:
  - Einkäufen in die Pensionskasse
  - Lohnänderungen und deren Auswirkungen
  - WEF-Bezügen (Wohneigentumsförderung)
  - Scheidungsbezügen
- ✅ Zugriff auf relevante Schweizer Webseiten (.ch Domain)
- ✅ MCP-Integration für:
  - BVG-Rechner
  - Steuerrechner (Einkommens-, Vermögens-, Kapitalbezugssteuer)
- ✅ Komplexe Finanzberechnungen und -planung

---

## Workplan

### Phase 1: Projekt-Setup und Grundstruktur
- [ ] Repository-Struktur erstellen
  - [ ] `/skills` - Verzeichnis für Copilot Skills
  - [ ] `/mcp-servers` - Referenzen zu bestehenden MCP-Servern
  - [ ] `/docs` - Dokumentation
  - [ ] `/tests` - Test-Dateien
  - [ ] `/examples` - Beispiel-Vorsorgepläne und -ausweise
- [ ] Grundlegende Konfigurationsdateien erstellen
  - [ ] `package.json` / `pyproject.toml` (je nach Hauptsprache)
  - [ ] `.copilot/` Konfiguration für GitHub Copilot Integration
  - [ ] `README.md` mit Projektbeschreibung
  - [ ] `.gitignore`

### Phase 2: MCP-Server Integration
- [ ] MCP-Server Konfiguration
  - [ ] Bestehende MCP-Server identifizieren und dokumentieren
  - [ ] Verbindung zu BVG-Rechner MCP-Server einrichten
  - [ ] Verbindung zu Steuer-MCP-Server einrichten
  - [ ] MCP-Client Implementation (C#)
- [ ] API-Wrapper für MCP-Server erstellen
  - [ ] BVG-Rechner Interface
  - [ ] Steuerrechner Interface
  - [ ] Fehlerbehandlung und Fallback-Logik

### Phase 3: Core Skills - AHV Berechnung
- [ ] AHV-Skill entwickeln
  - [ ] Beitragsjahre berechnen
  - [ ] AHV-Rente berechnen (einfache Altersrente)
  - [ ] Plafonierung und Skalierungen berücksichtigen
  - [ ] Witwen-/Witwerrenten berechnen
  - [ ] Waisenrenten berechnen
- [ ] Validierung und Tests für AHV-Berechnungen

### Phase 4: Core Skills - BVG Berechnung
- [ ] BVG-Skill entwickeln
  - [ ] Vorsorgeausweis-Parser (PDF/Text-Input)
  - [ ] Altersguthaben berechnen
  - [ ] Umwandlungssatz anwenden
  - [ ] Invaliditätsleistungen berechnen
  - [ ] Todesfallleistungen berechnen
- [ ] Integration mit BVG-Rechner MCP-Server
- [ ] Validierung mit realen Vorsorgeausweisen

### Phase 5: Core Skills - Einkäufe & Optimierung
- [ ] Einkaufs-Beratungs-Skill
  - [ ] Einkaufspotenzial berechnen
  - [ ] Steueroptimierung bei Einkäufen (via Steuer-MCP)
  - [ ] 3-Jahres-Sperrfrist berücksichtigen
  - [ ] Empfehlungen für optimale Einkaufsstrategie
- [ ] Lohnänderungs-Analyse-Skill
  - [ ] Auswirkungen auf BVG-Beiträge
  - [ ] Auswirkungen auf Altersguthaben
  - [ ] Langfristige Prognosen

### Phase 6: Core Skills - WEF & Scheidung
- [ ] WEF-Bezugs-Skill
  - [ ] Maximale WEF-Bezugshöhe berechnen
  - [ ] Rückzahlungsszenarien analysieren
  - [ ] Steuerliche Auswirkungen (via Steuer-MCP)
  - [ ] Vergleich: Bezug vs. Hypothek
- [ ] Scheidungs-Skill
  - [ ] Vorsorgeausgleich berechnen
  - [ ] Aufteilung von Altersguthaben
  - [ ] Auswirkungen auf zukünftige Renten

### Phase 7: 3a Säule & Steueroptimierung
- [ ] 3a-Säule-Skill
  - [ ] Maximale Einzahlungen berechnen
  - [ ] Steuerersparnis durch 3a (via Steuer-MCP)
  - [ ] Gestaffelte Bezugsstrategien
  - [ ] Vergleich: 3a Bank vs. 3a Versicherung
- [ ] Steuer-Optimierungs-Skill
  - [ ] Einkommenssteuer-Berechnung (via Steuer-MCP)
  - [ ] Vermögenssteuer-Berechnung (via Steuer-MCP)
  - [ ] Kapitalbezugssteuer optimieren
  - [ ] Vergleich: Rente vs. Kapital

### Phase 8: Web-Zugriff & Knowledge Base
- [ ] Web-Scraping-Skill (beschränkt auf .ch Domain)
  - [ ] Zugriff auf offizielle Schweizer Behördenseiten
  - [ ] Aktuelle AHV-Tabellen und -Sätze abrufen
  - [ ] BVG-Mindestzinssätze und Umwandlungssätze
  - [ ] Kantonsabhängige Steuertabellen
- [ ] Knowledge Base erstellen
  - [ ] Gesetzliche Grundlagen (AHV, BVG, FZL)
  - [ ] Häufige Beratungsszenarien
  - [ ] Best Practices für Vorsorgeplanung

### Phase 9: Finanzplanung & Berichte
- [ ] Finanzplanungs-Skill
  - [ ] Lebenslange Einkommensprojektion
  - [ ] Rentenkapitallücke berechnen
  - [ ] Inflationsbereinigung
  - [ ] Szenario-Analysen (Best/Worst/Likely Case)
- [ ] Beratungs-Engine
  - [ ] Konversationaler Dialog
  - [ ] Kontextverständnis für Folgefragen
  - [ ] Personalisierte Empfehlungen

### Phase 10: GitHub Copilot Integration
- [ ] Copilot Agent konfigurieren
  - [ ] Agent-Manifest erstellen
  - [ ] Skills registrieren
  - [ ] Prompt-Engineering für natürliche Interaktion
- [ ] CLI-Interface
  - [ ] Kommandos definieren
  - [ ] Input-Validierung
  - [ ] Output-Formatierung
- [ ] Testing im Copilot CLI
  - [ ] End-to-End Tests mit Beispielszenarien
  - [ ] Performance-Optimierung

### Phase 11: Dokumentation & Beispiele
- [ ] Benutzerdokumentation
  - [ ] Installationsanleitung
  - [ ] Verwendungsbeispiele
  - [ ] FAQ
- [ ] Entwicklerdokumentation
  - [ ] API-Dokumentation
  - [ ] Architektur-Übersicht
  - [ ] Erweiterungsanleitungen
- [ ] Beispiel-Dateien
  - [ ] Muster-Vorsorgeausweise (anonymisiert)
  - [ ] Typische Beratungsszenarien
  - [ ] Benchmark-Berechnungen

### Phase 12: Testing & Quality Assurance
- [ ] Unit-Tests für alle Skills
- [ ] Integration-Tests mit MCP-Servern
- [ ] Validierung gegen offizielle Rechner (z.B. AHV, verschiedene PK-Rechner)
- [ ] User Acceptance Testing
- [ ] Performance-Tests

### Phase 13: Vorbereitung für eigenständige Applikation (Zukunft)
- [ ] SDK-Integration vorbereiten
- [ ] Architektur-Refactoring für Standalone-Betrieb
- [ ] UI/UX-Konzept (optional)
- [ ] Deployment-Strategie

---

## Technische Überlegungen

### MCP-Server (C#)
- Bestehende MCP-Server werden genutzt
- C#-Wrapper für nahtlose Integration
- Asynchrone Kommunikation

### Skills (Python/TypeScript)
- **Python**: Komplexe Berechnungen, Datenanalyse
- **TypeScript**: Copilot-Integration, Web-Zugriff
- Modulare Architektur für einfache Erweiterbarkeit

### Datenschutz & Sicherheit
- Keine Speicherung von persönlichen Daten
- Read-only Operationen
- Alle Berechnungen lokal/temporär
- Schweizer Datenschutzstandards (DSG)

### Gesetzliche Grundlagen (Stand 2026)
- AHV-Gesetz (AHVG)
- BVG-Gesetz (BVG)
- Verordnungen: AHVV, BVV 1, BVV 2, BVV 3
- Aktuelle Umwandlungssätze, Grenzen, Sätze aus offiziellen Quellen

---

## Risiken & Abhängigkeiten

### Risiken
1. **Rechtliche Komplexität**: Schweizer Vorsorgesystem ist hochkomplex
2. **Aktualität**: Gesetzliche Änderungen müssen zeitnah eingepflegt werden
3. **MCP-Server Verfügbarkeit**: Abhängigkeit von externen Services
4. **Berechnungsgenauigkeit**: Hohe Anforderungen an Korrektheit

### Abhängigkeiten
- Bestehende MCP-Server für BVG und Steuern
- GitHub Copilot CLI / SDK
- Zugriff auf Schweizer Websites (.ch)
- Offizielle Tabellen und Formeln von Behörden

### Mitigationen
- Regelmäßige Updates der Berechnungslogik
- Fallback-Mechanismen bei MCP-Server-Ausfall
- Extensive Tests gegen offizielle Referenzrechner
- Klare Disclaimer zu Beratungsgrenzen

---

## Nächste Schritte
1. Repository-Struktur aufsetzen (Phase 1)
2. MCP-Server-Verbindungen testen (Phase 2)
3. Mit AHV-Skill beginnen als Proof-of-Concept (Phase 3)
