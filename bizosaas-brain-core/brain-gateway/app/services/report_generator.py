"""
Report generation service.

Handles the creation of CSV and PDF reports for analytics data.
"""

import io
import csv
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)


class ReportGenerator:
    """Generates analytics reports in various formats."""
    
    @staticmethod
    def generate_csv(data: List[Dict[str, Any]], filename: str = "report.csv") -> io.BytesIO:
        """
        Generate a CSV file from a list of dictionaries.
        
        Args:
            data: List of data rows (dicts)
            filename: Suggested filename (metadata)
            
        Returns:
            BytesIO object containing CSV data
        """
        if not data:
            return io.BytesIO(b"")
            
        output = io.StringIO()
        fieldnames = data[0].keys()
        
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
        
        # Convert to bytes
        output.seek(0)
        return io.BytesIO(output.getvalue().encode('utf-8'))

    @staticmethod
    def generate_pdf_report(
        title: str,
        summary_data: Dict[str, Any],
        tables: List[Dict[str, Any]]
    ) -> io.BytesIO:
        """
        Generate a PDF report with summary and data tables.
        
        Args:
            title: Report title
            summary_data: Key-value pairs for the summary section
            tables: List of dicts, each containing 'title', 'headers', and 'rows'
            
        Returns:
            BytesIO object containing PDF data
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title_style = styles['Title']
        elements.append(Paragraph(title, title_style))
        elements.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Summary Section
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        summary_text = []
        for key, value in summary_data.items():
            summary_text.append(f"<b>{key}:</b> {value}")
        elements.append(Paragraph("<br/>".join(summary_text), styles['Normal']))
        elements.append(Spacer(1, 0.25 * inch))
        
        # Tables
        for table_data in tables:
            elements.append(Paragraph(table_data.get('title', 'Data Table'), styles['Heading3']))
            
            headers = table_data.get('headers', [])
            rows = table_data.get('rows', [])
            
            if not headers:
                elements.append(Paragraph("No data available", styles['Normal']))
                continue
                
            # Prepare table data
            data = [headers] + rows
            
            # Create Table
            t = Table(data)
            
            # Style
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            
            elements.append(t)
            elements.append(Spacer(1, 0.25 * inch))
            
        try:
            doc.build(elements)
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            # Return empty if failed or handle gracefully
            return io.BytesIO(b"Error generating PDF")
            
        buffer.seek(0)
        return buffer
