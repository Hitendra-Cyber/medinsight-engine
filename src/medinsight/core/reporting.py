from fpdf import FPDF
from typing import Dict, Any
import datetime

class MedInsightReport(FPDF):
    def header(self):
        # Premium Geometric Banner Accent
        self.set_fill_color(15, 23, 42) # Navy Slate Background Dark #0f172a
        self.rect(0, 0, 210, 24, 'F')
        
        self.set_fill_color(43, 127, 255) # Electric Blue Accent Strip #2b7fff
        self.rect(0, 24, 210, 2, 'F')
        
        self.set_y(6)
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(255, 255, 255)
        self.cell(0, 6, 'MEDINSIGHT | DATA INTELLIGENCE REPORT', ln=True, align='L')
        
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cell(0, 4, f'Pipeline Execution Run: {timestamp} UTC', ln=True, align='L')
        self.set_y(32)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(148, 163, 184)
        self.cell(0, 10, f'Page {self.page_no()} | MedInsight Analytical Engines Group', align='C')

def clean_txt(text: str) -> str:
    if not isinstance(text, str): 
        text = str(text)
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf_report(profile: Dict[str, Any], insights: Dict[str, Any], output_path: str):
    pdf = MedInsightReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- CAPTURE 1: ARCHITECTURAL FOOTPRINT ---
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, '1. Structural Core System Topology', ln=True)
    pdf.set_draw_color(43, 127, 255)
    pdf.set_line_width(0.5) # <-- FIXED: Added the underscore here!
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Modern grid layout configuration
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(51, 65, 85)
    
    matrix_data = [
        ("Total Records Checked", f"{profile['rows']:,} Rows"),
        ("Feature Vector Columns", f"{profile['cols']} Elements"),
        ("Structural Null Fields", f"{profile['missing_cells']} Fault Flags"),
        ("Identified Duplicates", f"{profile['duplicate_rows']} Record Clones"),
        ("Runtime Volumetric Weight", f"{profile['memory_mb']} MB")
    ]
    
    for label, val in matrix_data:
        pdf.set_fill_color(248, 250, 252)
        pdf.cell(85, 8, f"  {label}", border='B', fill=True)
        pdf.set_font('Helvetica', 'B', 10)
        pdf.cell(105, 8, f"  {val}", border='B', ln=True)
        pdf.set_font('Helvetica', '', 10)
        
    pdf.ln(8)
    
    # --- CAPTURE 2: DOMAIN INSIGHTS PIPELINE ---
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, '2. Computed Analytical Rules & Heuristics', ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)
    
    # Statistical Values
    if insights.get("metrics"):
        pdf.set_font('Helvetica', 'B', 10)
        pdf.set_text_color(43, 127, 255)
        pdf.cell(0, 6, 'Derived Domain Coefficients:', ln=True)
        pdf.ln(2)
        
        pdf.set_font('Helvetica', '', 9)
        pdf.set_text_color(51, 65, 85)
        for k, v in insights["metrics"].items():
            pdf.set_fill_color(255, 255, 255)
            pdf.multi_cell(0, 5, clean_txt(f"  > {k}: {v}"), border='L', fill=True)
            pdf.ln(1)
        pdf.ln(4)

    # Observations and Alerts
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 6, 'Automated Strategic Observations:', ln=True)
    pdf.ln(2)
    
    pdf.set_font('Helvetica', '', 9)
    if insights.get("alerts"):
        for alert in insights["alerts"]:
            pdf.set_fill_color(254, 242, 242) # Light soft red background
            pdf.set_text_color(153, 27, 27)   # Dark red text
            pdf.multi_cell(0, 6, clean_txt(f" [ALERT] {alert}"), border=1, fill=True)
            pdf.ln(2)
    else:
        pdf.set_text_color(22, 101, 52) # Safe Green text
        pdf.cell(0, 6, '  - Database baseline completely normal. No anomalies triggered by rules engines.', ln=True)
        
    pdf.output(output_path)