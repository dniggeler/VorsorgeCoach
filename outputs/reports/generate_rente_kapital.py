"""
Bericht: Rente oder Kapital – Entscheidungsanalyse
Person: Niggeler Dieter | Pensionierung: 31.03.2034
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
from reportlab.platypus import Flowable
import datetime

# ── Palette ─────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#1B2A4A")
TEAL      = colors.HexColor("#0D7C7C")
TEAL_LIGHT= colors.HexColor("#E6F4F4")
AMBER     = colors.HexColor("#E8A020")
AMBER_LIGHT=colors.HexColor("#FDF3E0")
GREY_BG   = colors.HexColor("#F5F6F8")
GREY_LINE = colors.HexColor("#D1D5DB")
GREY_TEXT = colors.HexColor("#6B7280")
WHITE     = colors.white
RED_WARN  = colors.HexColor("#DC2626")
GREEN_OK  = colors.HexColor("#16A34A")

# ── Styles ───────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22,
                              textColor=NAVY, spaceAfter=4),
        "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=13,
                              textColor=NAVY, spaceBefore=14, spaceAfter=4),
        "h3": ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=10,
                              textColor=TEAL, spaceBefore=8, spaceAfter=3),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9,
                               textColor=colors.HexColor("#374151"), leading=14),
        "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8,
                                textColor=GREY_TEXT, leading=12),
        "warn": ParagraphStyle("warn", fontName="Helvetica-Oblique", fontSize=8,
                               textColor=RED_WARN, leading=12),
        "caption": ParagraphStyle("caption", fontName="Helvetica-Bold", fontSize=8,
                                  textColor=GREY_TEXT),
        "meta": ParagraphStyle("meta", fontName="Helvetica", fontSize=9,
                               textColor=WHITE, leading=13),
        "meta_bold": ParagraphStyle("meta_bold", fontName="Helvetica-Bold", fontSize=9,
                                    textColor=WHITE, leading=13),
        "kpi_val": ParagraphStyle("kpi_val", fontName="Helvetica-Bold", fontSize=18,
                                  textColor=NAVY, leading=22, alignment=TA_CENTER),
        "kpi_lbl": ParagraphStyle("kpi_lbl", fontName="Helvetica", fontSize=8,
                                  textColor=GREY_TEXT, alignment=TA_CENTER),
        "footer": ParagraphStyle("footer", fontName="Helvetica", fontSize=7,
                                 textColor=GREY_TEXT, alignment=TA_CENTER),
        "rec_body": ParagraphStyle("rec_body", fontName="Helvetica", fontSize=9,
                                   textColor=NAVY, leading=14),
    }

# ── Helpers ───────────────────────────────────────────────────────────────────
def chf(n): return f"CHF {n:,.0f}".replace(",", "'")
def pct(n): return f"{n:.1f}%"

def hr(color=GREY_LINE, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color, spaceAfter=6, spaceBefore=6)

def section_header(text, styles):
    return [
        Paragraph(text, styles["h2"]),
        HRFlowable(width="100%", thickness=1.5, color=TEAL, spaceAfter=8),
    ]

def kpi_table(items, styles):
    """items = list of (value, label, color_bar)"""
    cells = []
    for val, lbl, bar_color in items:
        inner = Table(
            [[Paragraph(val, styles["kpi_val"])],
             [Paragraph(lbl, styles["kpi_lbl"])]],
            colWidths=[40*mm]
        )
        inner.setStyle(TableStyle([
            ("ALIGN",      (0,0), (-1,-1), "CENTER"),
            ("TOPPADDING",  (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0),(-1,-1), 6),
            ("LEFTPADDING", (0,0), (-1,-1), 2),
            ("RIGHTPADDING",(0,0), (-1,-1), 2),
            ("LINEABOVE",  (0,0), (-1,0), 3, bar_color),
            ("BACKGROUND", (0,0), (-1,-1), GREY_BG),
            ("ROUNDEDCORNERS", [3]),
        ]))
        cells.append(inner)
    t = Table([cells], colWidths=[42*mm]*len(items))
    t.setStyle(TableStyle([
        ("ALIGN",      (0,0), (-1,-1), "CENTER"),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1), 3),
        ("RIGHTPADDING",(0,0),(-1,-1), 3),
    ]))
    return t

def two_col_table(rows, col_widths, styles, header_row=None, alt_bg=True):
    data = []
    if header_row:
        data.append(header_row)
    data.extend(rows)

    ts = [
        ("FONTNAME",     (0,0), (-1,-1), "Helvetica"),
        ("FONTSIZE",     (0,0), (-1,-1), 9),
        ("TEXTCOLOR",    (0,0), (-1,-1), colors.HexColor("#374151")),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("LINEBELOW",    (0,0), (-1,-2), 0.3, GREY_LINE),
        ("LINEBELOW",    (0,-1),(-1,-1), 0.5, GREY_LINE),
        ("VALIGN",       (0,0), (-1,-1), "MIDDLE"),
    ]
    if header_row:
        ts += [
            ("BACKGROUND", (0,0), (-1,0), NAVY),
            ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
            ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ]
        data_rows = data[1:]
        offset = 1
    else:
        data_rows = data
        offset = 0

    if alt_bg:
        for i, _ in enumerate(data_rows):
            if i % 2 == 0:
                ts.append(("BACKGROUND", (0, i+offset), (-1, i+offset), GREY_BG))

    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle(ts))
    return t

# ── Bar chart ─────────────────────────────────────────────────────────────────
def income_bar_chart():
    """Side-by-side bar: Rente vs Kapital annual net income."""
    d = Drawing(160*mm, 55*mm)
    bc = VerticalBarChart()
    bc.x = 12*mm
    bc.y = 8*mm
    bc.width = 140*mm
    bc.height = 40*mm
    bc.data = [
        [97515, 97491],  # LE 87, r=2%
    ]
    bc.bars[0].fillColor = TEAL
    bc.categoryAxis.categoryNames = ["Volle Rente", "Kapitalbezug (LE 87, 2%)"]
    bc.categoryAxis.labels.fontName = "Helvetica"
    bc.categoryAxis.labels.fontSize = 8
    bc.valueAxis.valueMin = 90000
    bc.valueAxis.valueMax = 102000
    bc.valueAxis.valueStep = 2000
    bc.valueAxis.labels.fontName = "Helvetica"
    bc.valueAxis.labels.fontSize = 7
    bc.groupSpacing = 20
    d.add(bc)
    return d

# ── Page template helpers ─────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN = 18*mm

def on_first_page(canvas, doc):
    _draw_header(canvas, doc, first=True)
    _draw_footer(canvas, doc)

def on_later_pages(canvas, doc):
    _draw_header(canvas, doc, first=False)
    _draw_footer(canvas, doc)

def _draw_header(canvas, doc, first):
    canvas.saveState()
    # Navy top bar
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_H - 22*mm, PAGE_W, 22*mm, fill=1, stroke=0)
    if first:
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 14)
        canvas.drawString(MARGIN, PAGE_H - 13*mm, "Rente oder Kapital – Entscheidungsanalyse")
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawString(MARGIN, PAGE_H - 18.5*mm, "Pensionierung 2. Säule | Niggeler Dieter | 31.03.2034")
        # Right: date
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica", 8)
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 13*mm, "VorsorgeCoach")
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 18.5*mm,
                               datetime.date.today().strftime("%d.%m.%Y"))
    else:
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawString(MARGIN, PAGE_H - 13*mm, "Rente oder Kapital – Entscheidungsanalyse")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 13*mm,
                               f"Seite {doc.page}")
    canvas.restoreState()

def _draw_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(GREY_LINE)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 12*mm, PAGE_W - MARGIN, 12*mm)
    canvas.setFillColor(GREY_TEXT)
    canvas.setFont("Helvetica", 6.5)
    canvas.drawString(MARGIN, 8*mm,
        "Diese Analyse dient ausschliesslich zu Informationszwecken und stellt keine Rechts- oder Steuerberatung dar. "
        "Alle Berechnungen sind indikativ.")
    canvas.restoreState()

# ── Main ──────────────────────────────────────────────────────────────────────
def build():
    out = "C:/workspace/dev/VorsorgeCoach/outputs/reports/niggeler_rente_vs_kapital_2034.pdf"
    doc = SimpleDocTemplate(
        out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=26*mm, bottomMargin=18*mm,
    )
    S = make_styles()
    story = []

    # ── 1. PERSONENDATEN ──────────────────────────────────────────────────────
    meta_data = [
        ["Person", "Niggeler Dieter", "Geburtsdatum", "17.03.1969"],
        ["Wohnort", "Zürich ZH", "Zivilstand", "verheiratet"],
        ["Pensionierung", "31.03.2034 (Alter 65)", "Pensionskasse", "PayrollPlus AG"],
    ]
    meta_table = Table(meta_data, colWidths=[32*mm, 55*mm, 35*mm, 50*mm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), NAVY),
        ("TEXTCOLOR",    (0,0), (-1,-1), WHITE),
        ("FONTNAME",     (0,0), (0,-1),  "Helvetica-Bold"),
        ("FONTNAME",     (2,0), (2,-1),  "Helvetica-Bold"),
        ("FONTNAME",     (1,0), (1,-1),  "Helvetica"),
        ("FONTNAME",     (3,0), (3,-1),  "Helvetica"),
        ("FONTSIZE",     (0,0), (-1,-1), 8.5),
        ("TOPPADDING",   (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0), (-1,-1), 5),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("TEXTCOLOR",    (0,0), (0,-1),  colors.HexColor("#94A3B8")),
        ("TEXTCOLOR",    (2,0), (2,-1),  colors.HexColor("#94A3B8")),
        ("LINEBELOW",    (0,0), (-1,-2), 0.4, colors.HexColor("#334E7A")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5*mm))

    # ── 2. WARNUNG ────────────────────────────────────────────────────────────
    warn_table = Table(
        [[Paragraph("⚠  Hinweis: Der Vorsorgeausweis weist Zivilstand «ledig» aus; das Klientenprofil «verheiratet». "
                    "Steuerberechnungen basieren auf verheiratet. Bitte Diskrepanz vor Entscheid klären.", S["warn"])]],
        colWidths=[PAGE_W - 2*MARGIN]
    )
    warn_table.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), AMBER_LIGHT),
        ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING",   (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0), (-1,-1), 6),
        ("LINEABOVE",    (0,0), (-1,0),  2, AMBER),
    ]))
    story.append(warn_table)
    story.append(Spacer(1, 5*mm))

    # ── 3. KPI ÜBERSICHT ─────────────────────────────────────────────────────
    story += section_header("Auf einen Blick", S)
    story.append(kpi_table([
        ("CHF 97'515",  "Netto-Jahreseink. Rente",   TEAL),
        ("CHF 97'491",  "Netto-Jahreseink. Kapital",  NAVY),
        ("CHF 145'913", "Kapitalbezugssteuer",         AMBER),
        ("83.7 Jahre",  "Break-even-Alter",            colors.HexColor("#7C3AED")),
    ], S))
    story.append(Spacer(1, 6*mm))

    # ── 4. EINGABEN ───────────────────────────────────────────────────────────
    story += section_header("Eingaben und Annahmen", S)
    eingaben = [
        ("PK-Jahresrente (brutto, Vorsorgeausweis)",   "CHF 80'979"),
        ("PK-Alterskapital (brutto, Projektion 1.5%)", "CHF 1'396'193"),
        ("AHV-Rente (erwartet ab 65)",                 "CHF 32'000"),
        ("Steuerbares Vermögen bei Pensionierung",     "CHF 400'000 (Schätzung, exkl. 3a)"),
        ("Gemeinde / Steuerort",                       "Zürich ZH (taxLocationId 800000000)"),
        ("Rendite-Annahme auf Kapital",                "2.0% p.a."),
        ("Lebenserwartung (Basis)",                    "87 Jahre"),
    ]
    story.append(two_col_table(
        [[Paragraph(k, S["body"]), Paragraph(v, S["body"])] for k,v in eingaben],
        col_widths=[110*mm, 62*mm], styles=S
    ))
    story.append(Spacer(1, 6*mm))

    # ── 5. SZENARIO-VERGLEICH ─────────────────────────────────────────────────
    story += section_header("Szenario-Vergleich", S)

    # Side-by-side scenario cards
    rente_rows = [
        ["Brutto-Jahreseinkommen (PK + AHV)", "CHF 112'979"],
        ["Steuer laufend (Kanton + Bund)", "− CHF 15'464"],
        ["", ""],
        ["Netto-Jahreseinkommen", "CHF 97'515"],
        ["", ""],
        ["Partnerrente (bei Tod)", "CHF 48'588/Jahr"],
        ["Kapital für Erbschaft", "—"],
    ]
    kapital_rows = [
        ["Alterskapital brutto",              "CHF 1'396'193"],
        ["Kapitalbezugssteuer (einmalig)",    "− CHF 145'913  (10.5%)"],
        ["Netto-Kapital nach Steuern",        "CHF 1'250'280"],
        ["Jährl. Entnahme (22 J., 2%)",       "CHF 70'805"],
        ["Steuer laufend (AHV + Vermögen)",   "− CHF 5'314"],
        ["Netto-Jahreseinkommen",             "CHF 97'491"],
        ["Kapital für Erbschaft",             "Restkapital vererbbar"],
    ]

    def scenario_table(title, rows, accent):
        header = Table(
            [[Paragraph(title, ParagraphStyle("sh", fontName="Helvetica-Bold",
                        fontSize=10, textColor=WHITE))]],
            colWidths=[85*mm]
        )
        header.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), accent),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
        ]))
        body_rows = []
        for i, (k, v) in enumerate(rows):
            is_total = "Netto-Jahreseinkommen" in k
            fn = "Helvetica-Bold" if is_total else "Helvetica"
            bg = TEAL_LIGHT if (is_total and accent == TEAL) else (
                 colors.HexColor("#EEF2FF") if (is_total and accent == NAVY) else
                 (GREY_BG if i % 2 == 0 else WHITE))
            body_rows.append([
                Paragraph(k, ParagraphStyle("sc", fontName=fn, fontSize=8.5,
                          textColor=NAVY if is_total else colors.HexColor("#374151"))),
                Paragraph(v, ParagraphStyle("sv", fontName="Helvetica-Bold" if is_total else "Helvetica",
                          fontSize=8.5, alignment=TA_RIGHT,
                          textColor=accent if is_total else colors.HexColor("#374151"))),
            ])
        bt = Table(body_rows, colWidths=[52*mm, 33*mm])
        bt.setStyle(TableStyle([
            ("TOPPADDING",   (0,0), (-1,-1), 4),
            ("BOTTOMPADDING",(0,0), (-1,-1), 4),
            ("LEFTPADDING",  (0,0), (-1,-1), 8),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("LINEBELOW",    (0,0), (-1,-2), 0.3, GREY_LINE),
        ]))
        for i, (k, _) in enumerate(rows):
            if i % 2 == 0:
                bt.setStyle(TableStyle([("BACKGROUND", (0,i), (-1,i), GREY_BG)]))
        wrapper = Table([[header], [bt]], colWidths=[85*mm])
        wrapper.setStyle(TableStyle([
            ("BOX",        (0,0), (-1,-1), 0.5, GREY_LINE),
            ("TOPPADDING", (0,0), (-1,-1), 0),
            ("BOTTOMPADDING",(0,0),(-1,-1), 0),
            ("LEFTPADDING",(0,0), (-1,-1), 0),
            ("RIGHTPADDING",(0,0),(-1,-1), 0),
        ]))
        return wrapper

    sc_table = Table(
        [[scenario_table("Szenario 1 — Volle Rente", rente_rows, TEAL),
          Spacer(4*mm, 1),
          scenario_table("Szenario 2 — Voller Kapitalbezug", kapital_rows, NAVY)]],
        colWidths=[85*mm, 4*mm, 85*mm]
    )
    sc_table.setStyle(TableStyle([
        ("VALIGN",     (0,0), (-1,-1), "TOP"),
        ("TOPPADDING", (0,0), (-1,-1), 0),
        ("BOTTOMPADDING",(0,0),(-1,-1), 0),
        ("LEFTPADDING",(0,0),(-1,-1), 0),
        ("RIGHTPADDING",(0,0),(-1,-1), 0),
    ]))
    story.append(sc_table)
    story.append(Spacer(1, 6*mm))

    # ── 6. KAPITALBEZUGSSTEUER BREAKDOWN ──────────────────────────────────────
    story += section_header("Kapitalbezugssteuer – Aufschlüsselung", S)
    tax_rows = [
        ["Bundessteuer",              "CHF 32'110",   "22.0%"],
        ["Kantonssteuer",             "CHF 51'395",   "35.2%"],
        ["Gemeindesteuer",            "CHF 62'408",   "42.8%"],
        ["Kirchensteuer",             "CHF 0",         "0.0%"],
        ["Total Kapitalbezugssteuer", "CHF 145'913",  "10.5% des Kapitals"],
    ]
    story.append(two_col_table(
        [[Paragraph(a, S["body"]),
          Paragraph(b, ParagraphStyle("tr", fontName="Helvetica", fontSize=9, alignment=TA_RIGHT)),
          Paragraph(c, ParagraphStyle("tr2", fontName="Helvetica", fontSize=9,
                    textColor=GREY_TEXT, alignment=TA_RIGHT))]
         for a,b,c in tax_rows],
        col_widths=[95*mm, 40*mm, 37*mm], styles=S,
        header_row=[Paragraph(h, ParagraphStyle("th", fontName="Helvetica-Bold",
                    fontSize=9, textColor=WHITE))
                    for h in ["Steuerart", "Betrag", "Anteil"]],
    ))
    story.append(Spacer(1, 6*mm))

    # ── 7. BREAK-EVEN ─────────────────────────────────────────────────────────
    story += section_header("Break-even-Analyse", S)

    be_box = Table([[
        Paragraph(
            "Die kumulierten Netto-PK-Rentenzahlungen (CHF 66'954/Jahr nach inkrementeller Steuer) "
            "erreichen den Netto-Kapitalbetrag von CHF 1'250'280 nach <b>18.7 Jahren</b> – "
            "entsprechend Alter <b>83 Jahre 8 Monate</b>.",
            ParagraphStyle("be", fontName="Helvetica", fontSize=9,
                           textColor=NAVY, leading=14)),
    ]], colWidths=[PAGE_W - 2*MARGIN])
    be_box.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,-1), TEAL_LIGHT),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("LINEABOVE",    (0,0), (-1,0),  3, TEAL),
    ]))
    story.append(be_box)
    story.append(Spacer(1, 4*mm))
    story.append(Paragraph(
        "Statistische Lebenserwartung eines Schweizer Mannes mit 65 Jahren: ~84–85 Jahre "
        "→ Break-even liegt <b>genau im statistischen Erwartungsbereich</b>. "
        "Dies ist eine echte Pattsituation.",
        S["body"]
    ))
    story.append(Spacer(1, 5*mm))

    # ── 8. SENSITIVITÄT ───────────────────────────────────────────────────────
    story += section_header("Sensitivität: Netto-Jahreseinkommen Kapital-Szenario", S)
    sens_header = [Paragraph(h, ParagraphStyle("sh", fontName="Helvetica-Bold",
                   fontSize=9, textColor=WHITE))
                   for h in ["Rendite p.a.", "Lebenserwartung 82", "Lebenserwartung 87", "Lebenserwartung 92"]]
    sens_data = [
        ["0%",   "CHF 100'232", "CHF 83'517",  "CHF 72'993"],
        ["2%",   "CHF 114'168", "CHF 97'491 ◀", "CHF 87'066"],
        ["4%",   "CHF 129'457", "CHF 113'204", "CHF 103'251"],
        ["Rente (fix)", "CHF 97'515", "CHF 97'515", "CHF 97'515"],
    ]
    sens_rows = []
    for row in sens_data:
        is_rente = row[0] == "Rente (fix)"
        style_key = "Helvetica-Bold" if is_rente else "Helvetica"
        color = TEAL if is_rente else colors.HexColor("#374151")
        sens_rows.append([
            Paragraph(row[0], ParagraphStyle("sr0", fontName=style_key, fontSize=9, textColor=color)),
            Paragraph(row[1], ParagraphStyle("sr1", fontName=style_key, fontSize=9,
                      alignment=TA_RIGHT, textColor=color)),
            Paragraph(row[2], ParagraphStyle("sr2", fontName=style_key, fontSize=9,
                      alignment=TA_RIGHT,
                      textColor=TEAL if "◀" in row[2] else color)),
            Paragraph(row[3], ParagraphStyle("sr3", fontName=style_key, fontSize=9,
                      alignment=TA_RIGHT, textColor=color)),
        ])
    story.append(two_col_table(
        sens_rows,
        col_widths=[30*mm, 45*mm, 45*mm, 52*mm],
        styles=S, header_row=sens_header,
    ))
    story.append(Paragraph("◀ Basisszenario (LE 87, Rendite 2%)", S["small"]))
    story.append(Spacer(1, 6*mm))

    # ── 9. ENTSCHEIDUNGSFAKTOREN ──────────────────────────────────────────────
    story += section_header("Entscheidungsfaktoren (qualitativ)", S)
    factors = [
        ("Gesundheit / Familiengeschichte", "Kurze LE → Kapital", "Lange LE → Rente",         "neutral"),
        ("Ehefrau absichern",               "—",                   "Partnerrente CHF 48'588/J → Rente","rente"),
        ("Erbschaft gewünscht",             "Restkapital vererbbar → Kapital", "—",             "kapital"),
        ("Grosse Ausgaben / Hypothek",      "Flexibilität → Kapital",          "—",             "kapital"),
        ("Umwandlungssatz-Risiko",          "Künftige Senkung möglich → Kapital","—",           "kapital"),
        ("Planungssicherheit",              "—",                   "Lebenslang garantiert → Rente","rente"),
        ("3-Jahres-Regel Einkäufe",         "—",                   "Einkäufe 08/2025 + 12/2025 → Bezug ab 01.12.2028 ✓","neutral"),
    ]
    fac_header = [Paragraph(h, ParagraphStyle("fh", fontName="Helvetica-Bold",
                  fontSize=9, textColor=WHITE))
                  for h in ["Faktor", "Spricht für Kapital", "Spricht für Rente"]]
    fac_rows = []
    for name, kap, ren, _ in factors:
        fac_rows.append([
            Paragraph(name, S["body"]),
            Paragraph(kap,  ParagraphStyle("fk", fontName="Helvetica", fontSize=8.5,
                      textColor=NAVY)),
            Paragraph(ren,  ParagraphStyle("fr", fontName="Helvetica", fontSize=8.5,
                      textColor=TEAL)),
        ])
    story.append(two_col_table(
        fac_rows,
        col_widths=[55*mm, 65*mm, 52*mm],
        styles=S, header_row=fac_header,
    ))
    story.append(Spacer(1, 6*mm))

    # ── 10. EMPFEHLUNG ────────────────────────────────────────────────────────
    story += section_header("Empfehlung", S)

    recs = [
        (TEAL,  "→ Rente bevorzugen",
         "Wenn Dieter und/oder seine Frau voraussichtlich <b>über 84 Jahre</b> alt werden, "
         "oder die langfristige Absicherung der Ehefrau Priorität hat "
         "(Partnerrente CHF 48'588/Jahr, lebenslang)."),
        (NAVY,  "→ Kapital bevorzugen",
         "Wenn Erbschaft gewünscht ist, eigene Investitionskompetenz vorhanden, "
         "eine Rendite <b>&gt; 2% realistisch erzielbar</b> ist, "
         "oder eine Hypothekentilgung / grosse Ausgabe geplant ist."),
        (AMBER, "→ Mischstrategie prüfen",
         "Teilkapitalbezug (z.B. 25–50%) kombiniert finanzielle Flexibilität mit "
         "laufender Absicherung. <b>Maximalen Kapitalbezugsanteil laut PK-Reglement klären.</b>"),
    ]
    for accent, title, text in recs:
        rec_table = Table([[
            Table([[""]], colWidths=[3*mm], rowHeights=[None]),
            Table([
                [Paragraph(title, ParagraphStyle("rt", fontName="Helvetica-Bold",
                           fontSize=9.5, textColor=accent))],
                [Paragraph(text, S["rec_body"])],
            ], colWidths=[PAGE_W - 2*MARGIN - 16*mm]),
        ]], colWidths=[3*mm, PAGE_W - 2*MARGIN - 3*mm])
        rec_table.setStyle(TableStyle([
            ("BACKGROUND",   (0,0), (-1,-1), GREY_BG),
            ("LINEABOVE",    (0,0), (0,0),   0, accent),
            ("LINEBEFORE",   (0,0), (0,-1),  4, accent),
            ("TOPPADDING",   (0,0), (-1,-1), 6),
            ("BOTTOMPADDING",(0,0), (-1,-1), 6),
            ("LEFTPADDING",  (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 8),
            ("VALIGN",       (0,0), (-1,-1), "TOP"),
        ]))
        story.append(rec_table)
        story.append(Spacer(1, 3*mm))

    story.append(Spacer(1, 5*mm))
    story.append(Paragraph(
        "Diese Analyse ist indikativ. Alle Steuerberechnungen basieren auf den Tarifen 2034 (projiziert). "
        "Für eine verbindliche Entscheidung empfiehlt sich eine unabhängige Fach- und Steuerberatung.",
        S["small"]
    ))

    # ── Build ──────────────────────────────────────────────────────────────────
    doc.build(story, onFirstPage=on_first_page, onLaterPages=on_later_pages)
    print(f"PDF erstellt: {out}")

if __name__ == "__main__":
    build()
