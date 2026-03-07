from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

OUTPUT = r'C:\workspace\dev\VorsorgeCoach\outputs\reports\3a_vorausberechnung_niggeler_2026.pdf'

doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title2', parent=styles['Title'],
    fontSize=18, spaceAfter=4, textColor=colors.HexColor('#1a3a5c'))
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=11, spaceAfter=2, textColor=colors.HexColor('#4a6a8c'))
h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=13, spaceAfter=4, spaceBefore=12, textColor=colors.HexColor('#1a3a5c'))
h3_style = ParagraphStyle('H3', parent=styles['Heading3'],
    fontSize=10, spaceAfter=3, spaceBefore=8, textColor=colors.HexColor('#2a5a8c'))
body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, spaceAfter=3)
small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8,
    textColor=colors.HexColor('#666666'), spaceAfter=2)
note_style = ParagraphStyle('Note', parent=styles['Normal'], fontSize=8,
    textColor=colors.HexColor('#444444'), leftIndent=6, rightIndent=6, spaceAfter=4, spaceBefore=4)

def chf(v):
    return "CHF {:,.0f}".format(v).replace(',', "'")

def pct(v):
    return "{:.1f}%".format(v * 100)

# ── DATA ──────────────────────────────────────────────────────────────────────
MAX_3A = 7258

baloise = 38000.0
ubs_3a = 67000.0
swisslife = 10000.0
frankly = 25000.0
TAX_SAVINGS = 2499

proj_rows = []
b, u, s, f = baloise, ubs_3a, swisslife, frankly
for year in range(2026, 2035):
    is_ret = (year == 2034)
    if is_ret:
        bn = b
        un = u * (1 + 0.01 * 3 / 12)
        sn = s
        fn = (f + MAX_3A) * (1 + 0.025 * 3 / 12)
    else:
        bn = b
        un = u * 1.01
        sn = s
        fn = (f + MAX_3A) * 1.025
    total = bn + un + sn + fn
    proj_rows.append((year, round(bn), round(un), round(sn), round(fn), round(total)))
    b, u, s, f = bn, un, sn, fn

FINAL_TOTAL = proj_rows[-1][5]
TOTAL_CONTRIB = MAX_3A * 9
TOTAL_TAX_SAVINGS = TAX_SAVINGS * 9

cap_tax_total = 12722
cap_tax_baloise = 1666
cap_tax_ubs = 3302
cap_tax_swisslife = 434
cap_tax_frankly = 4880
cap_tax_staggered = cap_tax_baloise + cap_tax_ubs + cap_tax_swisslife + cap_tax_frankly
cap_tax_saving = cap_tax_total - cap_tax_staggered
net_staggered = FINAL_TOTAL - cap_tax_staggered
net_total = FINAL_TOTAL - cap_tax_total

# ── COLORS ────────────────────────────────────────────────────────────────────
BLUE_DARK = colors.HexColor('#1a3a5c')
BLUE_MID = colors.HexColor('#2a5a8c')
BLUE_LIGHT = colors.HexColor('#d9e8f4')
BLUE_ROW = colors.HexColor('#edf4fb')
GREEN = colors.HexColor('#1a6e3c')
GREEN_LIGHT = colors.HexColor('#d5eddf')
ORANGE = colors.HexColor('#c45000')

story = []

# ── HEADER ────────────────────────────────────────────────────────────────────
story.append(Paragraph('Saeule 3a - Vorausberechnung bis Pensionierung', title_style))
story.append(Paragraph('Niggeler Dieter | Wohnort: Zuerich ZH | Erstellt: 05.03.2026', subtitle_style))
story.append(HRFlowable(width='100%', thickness=2, color=BLUE_DARK, spaceAfter=10))

# ── RAHMEN & ANNAHMEN ─────────────────────────────────────────────────────────
story.append(Paragraph('Rahmendaten und Annahmen', h2_style))

info_data = [
    ['Parameter', 'Wert', 'Parameter', 'Wert'],
    ['Versicherte Person', 'Dieter Niggeler', 'Geburtsdatum', '17.03.1969'],
    ['Zivilstand', 'Verheiratet', 'Geschlecht', 'Maennlich'],
    ['Wohnort', 'Zuerich ZH', 'Konfession', 'Keine'],
    ['Pensionierungsdatum', '01.04.2034', 'Pensionierungsalter', '65 Jahre'],
    ['Max. 3a-Beitrag 2026', chf(MAX_3A), 'Steuerbares Eink. (Kanton)', chf(193967)],
    ['Steuerbares Eink. (Bund)', chf(196967), 'Jahressteuer ohne 3a', chf(40081)],
]
info_table = Table(info_data, colWidths=[4*cm, 4.5*cm, 4*cm, 4.5*cm])
info_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BLUE_ROW]),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0c8e0')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(info_table)
story.append(Spacer(1, 8))

# ── KONTENÜBERSICHT ───────────────────────────────────────────────────────────
story.append(Paragraph('Saule 3a Konten - Stand 31.12.2025', h2_style))

konto_data = [
    ['Konto', 'Startguthaben', 'Rendite p.a.', 'Jaehl. Einzahlung', 'Einzahlungsende'],
    ['Baloise', chf(38000), pct(0), '-', '-'],
    ['UBS 3a', chf(67000), pct(0.01), '-', '-'],
    ['Swisslife', chf(10000), pct(0), '-', '-'],
    ['Frankly', chf(25000), pct(0.025), chf(MAX_3A) + ' (Max.)', 'Pensionierung 2034'],
    ['Total', chf(140000), '-', chf(MAX_3A), '-'],
]
konto_table = Table(konto_data, colWidths=[2.8*cm, 3.2*cm, 2.5*cm, 4*cm, 4.5*cm])
konto_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('BACKGROUND', (0, -1), (-1, -1), BLUE_LIGHT),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, BLUE_ROW]),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0c8e0')),
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(konto_table)
story.append(Spacer(1, 4))
story.append(Paragraph(
    'Hinweis: Baloise und Swisslife erzielen 0% Rendite - Optimierungspotenzial durch Umschichtung '
    'in renditestarke 3a-Loesungen (z.B. Frankly/VIAC) vorhanden.',
    note_style))

# ── JAHRESTABELLE ─────────────────────────────────────────────────────────────
story.append(Paragraph('Vorausberechnung 2026-2034 (pro Jahr)', h2_style))

header = ['Jahr', 'Baloise\n(0%)', 'UBS 3a\n(1%)', 'Swisslife\n(0%)', 'Frankly\n(2.5%)',
          'Einzahlung\nFrankly', 'Gesamt-\nguthaben', 'Steuer-\nersparnis']
table_data = [header]
for r in proj_rows:
    yr = str(r[0]) + (' *' if r[0] == 2034 else '')
    table_data.append([yr, chf(r[1]), chf(r[2]), chf(r[3]), chf(r[4]),
                       chf(MAX_3A), chf(r[5]), chf(TAX_SAVINGS)])
table_data.append(['Total / Summe', '-', '-', '-', '-',
                   chf(TOTAL_CONTRIB), chf(FINAL_TOTAL), chf(TOTAL_TAX_SAVINGS)])

col_w = [1.6*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.4*cm, 2.6*cm, 2.8*cm, 2.4*cm]
year_table = Table(table_data, colWidths=col_w, repeatRows=1)
year_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, BLUE_ROW]),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('BACKGROUND', (0, -1), (-1, -1), BLUE_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0c8e0')),
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('BACKGROUND', (0, 9), (-1, 9), colors.HexColor('#e8f4e8')),
    ('TEXTCOLOR', (6, 9), (6, 9), GREEN),
    ('FONTNAME', (6, 9), (6, 9), 'Helvetica-Bold'),
]))
story.append(year_table)
story.append(Spacer(1, 4))
story.append(Paragraph(
    '* 2034: Pensionierungsjahr (01.04.2034). Zins und Frankly-Einzahlung pro rata 3/12. '
    'Steuerersparnis 2034 geschaetzt analog Vorjahre.',
    small_style))

# ── KAPITALBEZUGSSTEUER ───────────────────────────────────────────────────────
story.append(Paragraph('Kapitalbezugssteuer bei Pensionierung (Zuerich, 2034)', h2_style))
story.append(Paragraph(
    'Die Saeule 3a wird bei Pensionierung als Kapital versteuert (getrennt vom uebrigen Einkommen). '
    'Durch zeitlich gestaffelte Bezuege (jedes Konto in einem separaten Steuerjahr) laesst sich '
    'die Steuerlast signifikant senken.',
    body_style))

tax_data = [
    ['Szenario', 'Kapital', 'Steuer', 'Satz', 'Netto'],
    ['Alle Konten gleichzeitig', chf(FINAL_TOTAL), chf(cap_tax_total),
     '{:.1f}%'.format(cap_tax_total / FINAL_TOTAL * 100), chf(net_total)],
    ['Gestaffelt - Baloise (2031)', chf(38000), chf(cap_tax_baloise),
     '{:.1f}%'.format(cap_tax_baloise / 38000 * 100), chf(38000 - cap_tax_baloise)],
    ['Gestaffelt - UBS 3a (2032)', chf(72733), chf(cap_tax_ubs),
     '{:.1f}%'.format(cap_tax_ubs / 72733 * 100), chf(72733 - cap_tax_ubs)],
    ['Gestaffelt - Swisslife (2033)', chf(10000), chf(cap_tax_swisslife),
     '{:.1f}%'.format(cap_tax_swisslife / 10000 * 100), chf(10000 - cap_tax_swisslife)],
    ['Gestaffelt - Frankly (2034)', chf(103352), chf(cap_tax_frankly),
     '{:.1f}%'.format(cap_tax_frankly / 103352 * 100), chf(103352 - cap_tax_frankly)],
    ['Gestaffelt Total', chf(FINAL_TOTAL), chf(cap_tax_staggered),
     '{:.1f}%'.format(cap_tax_staggered / FINAL_TOTAL * 100), chf(net_staggered)],
    ['Steuervorteil durch Staffelung', '', chf(cap_tax_saving), '', chf(cap_tax_saving)],
]
tax_table = Table(tax_data, colWidths=[5.5*cm, 3.2*cm, 2.8*cm, 2*cm, 3.5*cm])
tax_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8.5),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#fce8e0')),
    ('ROWBACKGROUNDS', (0, 2), (-1, -3), [BLUE_ROW, colors.white]),
    ('FONTNAME', (0, -2), (-1, -2), 'Helvetica-Bold'),
    ('BACKGROUND', (0, -2), (-1, -2), GREEN_LIGHT),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, -1), (-1, -1), GREEN),
    ('BACKGROUND', (0, -1), (-1, -1), GREEN_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0c8e0')),
    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
]))
story.append(tax_table)
story.append(Spacer(1, 4))
story.append(Paragraph(
    'Hinweis: Gestaffelte Bezuege nutzen indexierte Werte aus der Projektion. '
    'Effektive Steuerbetraege 2031-2034 werden gemaess aktuellem Steuergesetz berechnet.',
    small_style))

# ── ZUSAMMENFASSUNG ───────────────────────────────────────────────────────────
story.append(Paragraph('Gesamtzusammenfassung', h2_style))

summary_data = [
    ['Kennzahl', 'Wert'],
    ['Startguthaben Saule 3a (31.12.2025)', chf(140000)],
    ['Gesamteinzahlungen Frankly 2026-2034 (9 Jahre)', chf(TOTAL_CONTRIB)],
    ['Projiziertes Gesamtkapital bei Pensionierung (01.04.2034)', chf(FINAL_TOTAL)],
    ['Kapitalwachstum (absolut)', chf(FINAL_TOTAL - 140000)],
    ['Gesamte Steuerersparnis durch 3a-Beitraege (2026-2034)', chf(TOTAL_TAX_SAVINGS)],
    ['Kapitalbezugssteuer (Gesamtbezug)', chf(cap_tax_total)],
    ['Kapitalbezugssteuer (gestaffelt)', chf(cap_tax_staggered)],
    ['Steuervorteil durch Staffelung', chf(cap_tax_saving)],
    ['Netto nach Kapitalbezugssteuer (gestaffelt)', chf(net_staggered)],
]
sum_table = Table(summary_data, colWidths=[10*cm, 5*cm])
sum_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), BLUE_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, BLUE_ROW]),
    ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1, 3), (1, 3), BLUE_MID),
    ('FONTNAME', (0, 5), (-1, 5), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1, 5), (1, 5), GREEN),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (1, -1), (1, -1), GREEN),
    ('BACKGROUND', (0, -1), (-1, -1), GREEN_LIGHT),
    ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#b0c8e0')),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
]))
story.append(sum_table)

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 10))
story.append(HRFlowable(width='100%', thickness=1, color=BLUE_LIGHT, spaceAfter=6))
story.append(Paragraph('Annahmen, Grenzen und Handlungsempfehlungen', h3_style))
story.append(Paragraph(
    '<b>Annahmen:</b> Max. 3a-Beitrag CHF 7\'258/Jahr (Stand 2025; wird jaehrlich indexiert). '
    'Renditen konstant gemaess Kontospezifikation. Kombiniertes steuerbares Einkommen (Niggeler + Santos) '
    'CHF 193\'967 (Kanton) / CHF 196\'967 (Bund). Steuerberechnung Zuerich Stadt 2026, verheiratet, konfessionslos. '
    '2034: Zins und Einzahlung pro rata 3/12.',
    small_style))
story.append(Paragraph(
    '<b>Grenzen:</b> Keine Garantie auf zukuenftige Renditen oder Steuersaetze. '
    'Inflation nicht eingerechnet. 3a-Maximalbeitrag kann sich jaehrlich aendern.',
    small_style))
saving_str = "{:,.0f}".format(cap_tax_saving).replace(",", "'")
story.append(Paragraph(
    '<b>Empfehlungen:</b> (1) Baloise (CHF 38\'000, 0%%) und Swisslife (CHF 10\'000, 0%%) '
    'in renditestarke 3a-Loesungen (z.B. Frankly, VIAC) umschichten. '
    '(2) Staffelung der Bezuege spart CHF ' + saving_str + ' Kapitalbezugssteuer. '
    '(3) Bezugsplanung mindestens 5 Jahre vor Pensionierung starten (PK-Einkaeufe beachten: '
    '3-Jahres-Sperrfrist bei Kapitalbezug).',
    small_style))
story.append(Spacer(1, 6))
story.append(Paragraph(
    'Automatisch erstellt mit VorsorgeCoach (05.03.2026). Ersetzt keine individuelle Rechts- oder Steuerberatung. '
    'Alle Angaben ohne Gewaehr. Beraetergenehmigung erforderlich vor Weiterleitung.',
    ParagraphStyle('Disc', parent=styles['Normal'], fontSize=7,
                   textColor=colors.HexColor('#888888'))))

doc.build(story)
print('PDF erstellt:', OUTPUT)
