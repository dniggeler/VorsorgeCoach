# Skills Setup - VorsorgeCoach

## Status: ✅ Complete

All skills from the `skills/` directory are now available in the `.copilot/skills/` directory and ready to use with GitHub Copilot CLI.

## Available Skills

### 1. Einkauf (PK-Einkauf Steuerrechner) v1.2
**Status:** ✓ Active  
**Location:** `.copilot/skills/Einkauf/skill.md`

Berechnet Steuerersparnis und Netto-Vorteil bei freiwilligen PK-Einkäufen unter Berücksichtigung der Kapitalbezugssteuer.

**Key Features:**
- Steuerersparnis bei PK-Einkäufen (Bund + Kanton + Gemeinde)
- Kapitalbezugssteuer-Berechnung beim späteren Bezug
- Netto-Vorteil: Steuerersparnis minus Kapitalbezugssteuer
- Verteilung auf mehrere Jahre (1-5 Jahre)
- Automatische 3-Jahres-Regel-Prüfung
- JSON-strukturierte Ausgabe

**MCP Integration:**
- `swisstax-rechner`: search_municipalities, calculate_wealth_and_income_tax, calculate_capital_benefit_tax

## Directory Structure

```
.copilot/
├── skills/              # Active skills available to Copilot
│   ├── Einkauf/
│   │   └── skill.md
│   └── README.md        # Skills documentation
├── skills.json          # Skills registry
└── mcp.json            # MCP server configuration
```

## How to Use Skills

### In Copilot CLI

Skills are automatically available when you use the GitHub Copilot CLI in this repository. Simply ask questions related to the skill's domain:

```
"Was spare ich netto wenn ich CHF 50'000 in die PK einkaufe und 2029 als Kapital beziehe?"
"Lohnt sich ein Einkauf von CHF 80'000 verteilt auf 3 Jahre?"
```

Copilot will automatically:
1. Recognize the context (PK-Einkauf)
2. Load the Einkauf skill definition
3. Use the appropriate MCP tools (swisstax-rechner)
4. Orchestrate the calculation workflow
5. Return structured JSON output

### Managing Skills

Use the provided management script:

```powershell
# List all skills
.\manage-skills.ps1 list

# Show skill details
.\manage-skills.ps1 info Einkauf

# Sync skills from source
.\manage-skills.ps1 sync
```

## Adding New Skills

1. **Create skill directory:**
   ```
   skills/
   └── NewSkillName/
       └── skill.md
   ```

2. **Define skill in skill.md:**
   - Capabilities
   - MCP tools needed
   - Input parameters
   - Output format
   - Example triggers

3. **Activate skill:**
   ```powershell
   .\manage-skills.ps1 enable NewSkillName
   ```
   Or manually copy to `.copilot/skills/NewSkillName/`

4. **Update registry:**
   Add entry to `.copilot/skills.json`

5. **Test:**
   Ask Copilot CLI a question in the skill's domain

## Maintenance

### Updating Skills

When you modify a skill definition in `skills/*/skill.md`:

1. Either run `.\manage-skills.ps1 sync` to sync all skills
2. Or manually copy the updated `skill.md` to `.copilot/skills/*/`

### MCP Server Configuration

MCP servers are configured in `.copilot/mcp.json`. Currently configured:
- **bvg-rechner**: BVG calculations (not used by Einkauf skill)
- **swisstax-rechner**: Required for Einkauf skill (needs to be added to mcp.json)

## Next Steps

To make the Einkauf skill fully functional, you need to:

1. ✅ Skill definition created
2. ✅ Skill activated in .copilot/skills/
3. ⚠️  Add swisstax-rechner MCP server to `.copilot/mcp.json`
4. ⚠️  Install/configure swisstax-rechner MCP server
5. ⚠️  Test the complete workflow

## References

- [Main README](../README.md)
- [Skills Documentation](../skills/README.md)
- [Einkauf Skill Definition](../skills/Einkauf/skill.md)
- [Skills Registry](.copilot/skills.json)
