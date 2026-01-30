# VorsorgeCoach Skills

Dieses Verzeichnis enthält die Copilot Skills für den VorsorgeCoach.

## Struktur

```
skills/
├── ahv/              # AHV-Berechnungen und Beratung
├── bvg/              # BVG-Berechnungen und Beratung
├── pillar3a/         # 3a-Säule Berechnungen
├── tax/              # Steueroptimierung
├── planning/         # Finanzplanung
└── common/           # Gemeinsame Utilities
```

## Skill-Entwicklung

Jeder Skill sollte folgende Struktur haben:

```
skill-name/
├── __init__.py       # Skill-Export
├── skill.py          # Hauptlogik
├── models.py         # Datenmodelle
├── tests/            # Unit-Tests
└── README.md         # Skill-Dokumentation
```

## Nächste Schritte

Skills werden in den Phasen 3-9 des Implementierungsplans entwickelt.
