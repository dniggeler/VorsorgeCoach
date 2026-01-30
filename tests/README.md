# VorsorgeCoach Tests

Dieses Verzeichnis enthält Tests für alle Komponenten des VorsorgeCoach.

## Teststruktur

```
tests/
├── unit/             # Unit-Tests für einzelne Skills
├── integration/      # Integration-Tests mit MCP-Servern
├── e2e/              # End-to-End Tests
└── fixtures/         # Test-Daten und Fixtures
```

## Test-Ausführung

### Python-Tests
```bash
pytest
pytest --cov=skills tests/  # Mit Coverage
```

### TypeScript/JavaScript-Tests
```bash
npm test
npm run test:coverage
```

## Test-Anforderungen

- Alle Skills müssen Unit-Tests haben
- Integration-Tests für MCP-Server-Anbindungen
- Validierung gegen offizielle Rechner (AHV, BVG)
- Performance-Tests für komplexe Berechnungen

## Nächste Schritte

Test-Infrastruktur wird aufgebaut, sobald erste Skills implementiert sind (ab Phase 3).
