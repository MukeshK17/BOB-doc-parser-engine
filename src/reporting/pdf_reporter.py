# src/reporting/pdf_reporter.py
import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_final_pdf_report(json_dir, output_pdf_path):
    """
    Generates a beautifully styled, dynamic audit report matching your 
    ReportLab template specifications perfectly.
    """
    doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    cell_text_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
    )
    
    header_text_style = ParagraphStyle(
        'HeaderValueText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.whitesmoke,
        fontName="Helvetica-Bold"
    )

    elements.append(Paragraph("FRAUD RISK INTERACTIVE AUDIT REPORT", styles['Title']))
    elements.append(Spacer(1, 12))

    # Ingest runtime analytical records
    all_reports = []
    if os.path.exists(json_dir):
        for filename in sorted(os.listdir(json_dir)):
            if filename.endswith(".json"):
                with open(os.path.join(json_dir, filename), 'r') as f:
                    try:
                        all_reports.append(json.load(f))
                    except Exception:
                        continue

    if not all_reports:
        elements.append(Paragraph("No processing records found.", cell_text_style))
        doc.build(elements)
        return

    # Metrics Calculations
    total_docs = len(all_reports)
    flagged = [r for r in all_reports if r.get('primary_keywords') or r.get('query_answer') == "YES"]
    clean_count = total_docs - len(flagged)

    stats_data = [
        ["Metric", "Value"],
        ["Total Documents Scanned", total_docs],
        ["Total Flagged Documents", len(flagged)],
        ["Total Clean Documents", clean_count]
    ]
    
    stats_table = Table(stats_data, colWidths=[200, 100])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(stats_table)
    elements.append(Spacer(1, 24))

    elements.append(Paragraph("Detailed Document Audit Results", styles['Heading2']))
    elements.append(Spacer(1, 12))

    # Pull the exact prompt the user entered dynamically from the first record
    user_query_header = all_reports[0].get("interactive_query", "Query Result")
    
    headers = [
        Paragraph("File Name", header_text_style), 
        Paragraph("Status", header_text_style), 
        Paragraph(f"Query: \"{user_query_header}\"", header_text_style), 
        Paragraph("Primary Hits", header_text_style)
    ]
    table_data = [headers]

    red_highlight_row_indices = []

    for idx, r in enumerate(all_reports, start=1):
        query_ans = r.get('query_answer', 'NA')
        status = "FLAGGED" if (r.get('primary_keywords') or query_ans == "YES") else "CLEAN"
        
        # Format metrics lists using your crisp `<br/>` newline layout
        hits_dict = r.get('primary_keywords', {})
        hits = "<br/>".join([f"{k}({v})" for k, v in hits_dict.items()]) if hits_dict else "None"
            
        table_data.append([
            Paragraph(r.get('document_name', 'Unknown'), cell_text_style),
            Paragraph(status, cell_text_style),
            Paragraph(query_ans, cell_text_style), 
            Paragraph(hits, cell_text_style)
        ])
        
        if query_ans == "YES":
            red_highlight_row_indices.append(idx)

    # Set cell spacing constraints to guarantee it doesn't break wide table layouts
    results_table = Table(table_data, colWidths=[120, 65, 155, 160])
    
    table_styles = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]
    
    # Apply soft red background tinting rule (#FFCCCC)
    for row_idx in red_highlight_row_indices:
        table_styles.append(('BACKGROUND', (0, row_idx), (-1, row_idx), colors.HexColor('#FFCCCC')))
        
    results_table.setStyle(TableStyle(table_styles))
    elements.append(results_table)
    doc.build(elements)
    print(f"[SUCCESS] Executive PDF Report generated at: {output_pdf_path}")
    