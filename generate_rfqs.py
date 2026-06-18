from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

def create_rfq_pdf(filename, title, company, date, context, positions, conditions):
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(name='CustomTitle', parent=styles['Heading1'], fontSize=20, spaceAfter=20, textColor=colors.darkblue)
    h2_style = ParagraphStyle(name='Heading2', parent=styles['Heading2'], fontSize=14, spaceBefore=15, spaceAfter=10, textColor=colors.steelblue)
    normal_style = styles['Normal']
    normal_style.fontSize = 10
    normal_style.leading = 14
    
    elements = []
    
    # Header
    elements.append(Paragraph(company, ParagraphStyle(name='Right', parent=styles['Normal'], alignment=2)))
    elements.append(Paragraph(f"Datum: {date}", ParagraphStyle(name='Right', parent=styles['Normal'], alignment=2)))
    elements.append(Spacer(1, 40))
    
    # Title
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # Context
    elements.append(Paragraph("1. Projektbeschreibung & Ausgangslage", h2_style))
    for para in context.split('\n\n'):
        elements.append(Paragraph(para.replace('\n', ' '), normal_style))
        elements.append(Spacer(1, 10))
    
    elements.append(PageBreak())
    
    # Positions
    elements.append(Paragraph("2. Leistungsverzeichnis (Positionen)", h2_style))
    
    data = [['Pos.', 'Beschreibung', 'Menge', 'Spezifikation']]
    for i, pos in enumerate(positions, 1):
        data.append([str(i), Paragraph(pos['name'], normal_style), pos['qty'], Paragraph(pos['spec'], normal_style)])
        
    t = Table(data, colWidths=[30, 150, 60, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.steelblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 20))
    
    # Conditions
    elements.append(Paragraph("3. Rahmenbedingungen", h2_style))
    for key, value in conditions.items():
        elements.append(Paragraph(f"<b>{key}:</b> {value}", normal_style))
        elements.append(Spacer(1, 8))
        
    elements.append(PageBreak())
    
    # Legal / Compliance
    elements.append(Paragraph("4. Rechtliches & Compliance", h2_style))
    legal_text = """
    Mit der Abgabe eines Angebots akzeptiert der Bieter unsere Allgemeinen Einkaufsbedingungen (AEB).
    Die Vertraulichkeit ist strengstens zu wahren; ein separates NDA ist vor Vertragsabschluss zu unterzeichnen.
    Der Bieter versichert, die Vorgaben der DSGVO sowie geltende Arbeitsschutz- und Mindestlohngesetze einzuhalten.
    Wir behalten uns das Recht vor, vor Auftragsvergabe ein Lieferantenaudit (gem. ISO 9001) durchzuführen.
    Gerichtsstand ist der Sitz unseres Unternehmens. Es gilt ausschließlich das Recht der Bundesrepublik Deutschland.
    """
    elements.append(Paragraph(legal_text.replace('\n', ' '), normal_style))

    doc.build(elements)

if not os.path.exists('rfqs'):
    os.makedirs('rfqs')

# 1. Maschinenbau
create_rfq_pdf(
    'rfqs/01_maschinenbau_fertigungslinie.pdf',
    'Ausschreibung: Modernisierung Fertigungslinie 4 (RFQ-2026-0042)',
    'TechCore Industrial GmbH\nEinkauf Investitionsgüter\nMax-Planck-Str. 1\n80331 München',
    '16. Juni 2026',
    "Sehr geehrte Damen und Herren,\n\nwir planen die umfassende Modernisierung unserer Fertigungslinie 4 am Hauptstandort München. Ziel ist die Erhöhung der Taktzeit um 15% sowie die vollständige Integration in unser neues MES-System (Manufacturing Execution System).\n\nWir laden Sie hiermit ein, auf Basis des beigefügten Leistungsverzeichnisses ein verbindliches Angebot abzugeben. Bitte beachten Sie zwingend die technischen Vorgaben hinsichtlich der Schnittstellen und des Platzbedarfs.",
    [
        {'name': 'Industriemotor Hochleistung', 'qty': '12 Stk', 'spec': '500kW, IP65 Schutzklasse, IE4 Effizienz. Inklusive Montageflansch und Sensoren für Condition Monitoring.'},
        {'name': 'SPS Steuerungseinheit', 'qty': '4 Set', 'spec': 'Kompatibel mit Industrie 4.0 Standard. PROFINET und OPC UA Schnittstellen zwingend erforderlich.'},
        {'name': 'Förderbandmodule', 'qty': '120 Meter', 'spec': 'Schwerlastausführung (bis 500kg/m). Geschwindigkeit stufenlos regelbar 0.5 - 2.5 m/s.'},
        {'name': 'Installation & Inbetriebnahme', 'qty': '1 Pauschal', 'spec': 'Komplette mechanische und elektrische Einbindung in bestehende Anlage. Turn-key.'}
    ],
    {
        'Lieferbedingungen': 'DDP München (Incoterms 2020), frei Verwendungsstelle.',
        'Liefertermin': 'Spätestens 15. September 2026. Eine Verzögerung führt zu Pönalen gem. AEB.',
        'Zahlungsbedingungen': '30 Tage netto nach erfolgreicher Abnahme (FAT) und Rechnungseingang.',
        'Gewährleistung': '48 Monate ab finaler Abnahme (SAT) ohne Kilometerbegrenzung.',
        'Besondere Anforderungen': 'Die Dokumentation muss in Deutsch und Englisch in digitaler Form übergeben werden (EPLAN, Step).'
    }
)

# 2. IT / SaaS
create_rfq_pdf(
    'rfqs/02_saas_crm_migration.pdf',
    'Request for Quotation: Enterprise CRM Migration & Lizenzen',
    'Global Trade Solutions SE\nIT Procurement\nFriedrichstr. 45\n10117 Berlin',
    '22. August 2026',
    "Sehr geehrte Damen und Herren,\n\nunsere aktuelle CRM-Lösung erreicht ihr End-of-Life. Wir suchen einen strategischen Partner für die Bereitstellung von Lizenzen sowie die vollständige Migration unserer Bestandsdaten (ca. 4 Terabyte, 1.2 Mio Datensätze) auf eine moderne, cloud-basierte SaaS-Plattform.\n\nDas System muss mandantenfähig sein und von unseren Niederlassungen in 14 Ländern genutzt werden können. Höchste Anforderungen an Datenschutz und Ausfallsicherheit sind unerlässlich.",
    [
        {'name': 'Enterprise SaaS Lizenzen', 'qty': '850 User', 'spec': 'Voller Lese- und Schreibzugriff. Inkl. API-Nutzungskontingent (10 Mio Calls/Monat).'},
        {'name': 'Datenmigration', 'qty': '1 Pauschal', 'spec': 'ETL-Prozess für 4TB Bestandsdaten aus Altsystem (Oracle). Inkl. Datenbereinigung und Mapping.'},
        {'name': 'Schnittstellen-Entwicklung', 'qty': '3 Stk', 'spec': 'Anbindung an SAP ERP, Microsoft 365 (Exchange) und unser hauseigenes BI-Tool via REST-API.'},
        {'name': 'Managed Service 24/7', 'qty': '36 Monate', 'spec': 'SLA: 99.9% Verfügbarkeit. Max. Response-Time bei P1-Incidents: 1 Stunde.'}
    ],
    {
        'Vertragslaufzeit': 'Initiale Bindung 36 Monate, automatische Verlängerung um 12 Monate.',
        'Preisobergrenze': 'Das Budget für das Gesamtprojekt (Implementierung + Jahr 1) ist auf 450.000 EUR gedeckelt.',
        'Zahlungsziel': 'Lizenzen jährlich im Voraus. Dienstleistungen nach Meilensteinen, 14 Tage netto.',
        'Vertraulichkeit': 'Auftragnehmer muss vor Projektstart ein erweitertes NDA sowie einen AVV (Auftragsverarbeitungsvertrag) gem. DSGVO unterzeichnen.',
        'Audit-Vorbehalt': 'Wir fordern das Recht ein, die Rechenzentren (oder TISAX Zertifikate) jährlich zu auditieren.',
        'Gerichtsstand': 'Berlin, Deutschland.'
    }
)

print("PDFs generated successfully.")
