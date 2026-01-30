# VorsorgeCoach Dokumentation

## Inhaltsverzeichnis

1. [Übersicht](#übersicht)
2. [Installation](installation.md)
3. [Verwendung](usage.md)
4. [Architektur](architecture.md)
5. [API-Referenz](api-reference.md)
6. [Implementierungsplan](implementation-plan.md)

## Übersicht

VorsorgeCoach ist ein KI-gestützter Assistent für die Schweizer Altersvorsorge, der als GitHub Copilot Agent implementiert ist.

### Abgedeckte Bereiche

- **AHV** (1. Säule)
- **BVG** (2. Säule)
- **Säule 3a** (3. Säule)
- **Steueroptimierung**

### Funktionsweise

Der VorsorgeCoach verwendet:
- **MCP-Server** für komplexe Berechnungen (BVG, Steuern)
- **Skills** für spezifische Beratungsaufgaben
- **GitHub Copilot** für natürliche Sprachinteraktion

## Schnellstart

```bash
# Installation
npm install
pip install -r requirements.txt

# Verwendung
gh copilot
> "Berechne meine AHV-Rente bei einem durchschnittlichen Jahreseinkommen von CHF 80'000"
```

## Dokumentationsstruktur

- `installation.md` - Installationsanleitung
- `usage.md` - Verwendungsbeispiele
- `architecture.md` - Technische Architektur
- `api-reference.md` - API-Dokumentation
- `implementation-plan.md` - Entwicklungsplan

## Weiterführende Links

- [AHV-Gesetz](https://www.admin.ch)
- [BVG-Gesetz](https://www.admin.ch)
- [GitHub Copilot Dokumentation](https://docs.github.com/en/copilot)
