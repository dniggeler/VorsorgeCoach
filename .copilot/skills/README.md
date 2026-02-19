# VorsorgeCoach Skills Registry

This directory contains Copilot CLI skills for the VorsorgeCoach project.

## Available Skills

### 1. Einkauf (PK-Einkauf Steuerrechner)
**Path:** `Einkauf/skill.md`  
**Version:** 1.2  
**Description:** Berechnet die Steuerersparnis bei freiwilligen Einkäufen in die Pensionskasse (2. Säule) in der Schweiz und die spätere Kapitalbezugssteuer. Ermittelt den Netto-Vorteil unter Berücksichtigung der gesamten Steuerfolgen.

**Capabilities:**
- Steuerersparnis bei PK-Einkäufen (Bund + Kanton + Gemeinde)
- Kapitalbezugssteuer-Berechnung
- Netto-Vorteil: Steuerersparnis minus Kapitalbezugssteuer
- Verteilung des Einkaufs auf mehrere Jahre (1-5 Jahre)
- Automatische Prüfung der 3-Jahres-Regel
- Strukturierte JSON-Ausgabe

**MCP Tools:**
- swisstax-rechner: `search_municipalities`, `calculate_wealth_and_income_tax`, `calculate_capital_benefit_tax`

**Example Triggers:**
- "Was spare ich netto wenn ich CHF 50'000 einkaufe und 2029 als Kapital beziehe?"
- "Lohnt sich ein Einkauf von CHF 80'000 verteilt auf 3 Jahre vs. alles auf einmal?"

---

## How Skills Work

Each skill is defined by a `skill.md` file that describes:
- Capabilities and scope
- Available backend tools (MCP servers)
- Input parameters and expected outputs
- Example use cases
- Important rules and disclaimers

When you invoke a skill, Copilot CLI loads the skill definition and uses it to guide the conversation and orchestrate the appropriate tools.

## Skill Development

To add a new skill:

1. Create a new directory under `skills/` in the project root
2. Create a `skill.md` file with the skill definition
3. Copy or link the skill to `.copilot/skills/` (this directory)
4. Update this README with the new skill information

## Maintenance

Skills in this directory are linked from `../../skills/`. To update a skill, edit the source file in `../../skills/<skill-name>/skill.md`.
