# MCP-Servers

Dieses Verzeichnis enthält Referenzen und Wrapper für die MCP-Server, die vom VorsorgeCoach verwendet werden.

## Verwendete MCP-Server

### BVG-Rechner MCP-Server
- **Funktion**: Berechnungen für die berufliche Vorsorge
- **Technologie**: C#
- **Status**: Wird in Phase 2 integriert

### Steuer-MCP-Server
- **Funktion**: Steuerberechnungen (Einkommens-, Vermögens-, Kapitalbezugssteuer)
- **Technologie**: C#
- **Status**: Wird in Phase 2 integriert

## Struktur

```
mcp-servers/
├── bvg-calculator/   # BVG-Rechner Integration
├── tax-calculator/   # Steuerrechner Integration
└── common/           # Gemeinsame MCP-Client-Logik
```

## MCP-Integration

Die MCP-Server werden über standardisierte Schnittstellen angebunden. C#-Wrapper ermöglichen die nahtlose Integration in die Skill-Infrastruktur.

## Nächste Schritte

MCP-Server-Integration erfolgt in Phase 2 des Implementierungsplans.
