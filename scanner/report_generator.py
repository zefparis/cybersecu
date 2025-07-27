"""
Report Generator for OWASP ZAP Scanner

This module provides functionality to generate reports in various formats (PDF, JSON)
from the scan results.
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, Union
from dataclasses import asdict, is_dataclass

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer,
        Table, TableStyle, PageBreak
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    def __init__(self, scan_results: Dict[str, Any], output_dir: str = "reports"):
        self.scan_results = scan_results
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_json_report(self, filename: Optional[str] = None) -> str:
        if not filename:
            filename = f"scan_report_{self.timestamp}.json"
        elif not filename.endswith('.json'):
            filename += ".json"

        filepath = os.path.join(self.output_dir, filename)

        def convert(obj):
            if is_dataclass(obj):
                return {k: convert(v) for k, v in asdict(obj).items()}
            elif isinstance(obj, (list, tuple)):
                return [convert(i) for i in obj]
            elif isinstance(obj, dict):
                return {k: convert(v) for k, v in obj.items()}
            elif hasattr(obj, 'isoformat'):
                return obj.isoformat()
            return obj

        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "scan_id": self.scan_results.get("id", "unknown"),
                "target": self.scan_results.get("target", ""),
                "scan_start": self.scan_results.get("start_time", ""),
                "scan_end": self.scan_results.get("end_time", ""),
                "status": self.scan_results.get("status", "unknown"),
                "vulnerability_count": len(self.scan_results.get("vulnerabilities", []))
            },
            "vulnerabilities": [convert(v) for v in self.scan_results.get("vulnerabilities", [])],
            "summary": self._generate_summary()
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        return filepath

    def generate_pdf_report(self, filename: Optional[str] = None) -> Optional[str]:
        if not REPORTLAB_AVAILABLE:
            return None

        if not filename:
            filename = f"scan_report_{self.timestamp}.pdf"
        elif not filename.endswith('.pdf'):
            filename += ".pdf"

        filepath = os.path.join(self.output_dir, filename)
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Title', fontSize=24, spaceAfter=20,
                                  textColor=colors.HexColor('#00ff9d'), alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='Subtitle', fontSize=12, spaceAfter=30,
                                  textColor=colors.HexColor('#888888'), alignment=TA_CENTER))
        styles.add(ParagraphStyle(name='SectionHeader', fontSize=16, spaceAfter=10,
                                  textColor=colors.HexColor('#00ccff')))
        styles.add(ParagraphStyle(name='VulnerabilityTitle', fontSize=14, spaceAfter=6,
                                  textColor=colors.HexColor('#ff5555')))
        styles.add(ParagraphStyle(name='Italic', fontSize=10, textColor=colors.grey))

        elements.append(Paragraph("Rapport d'Analyse de Sécurité", styles['Title']))
        elements.append(Paragraph("Généré par CyberCrim - IA-Solution", styles['Subtitle']))
        elements.append(Paragraph("Détails du Scan", styles['SectionHeader']))

        meta_data = [
            ["Cible:", self.scan_results.get("target", "N/A")],
            ["ID du Scan:", self.scan_results.get("id", "N/A")],
            ["Date de Début:", self._format_timestamp(self.scan_results.get("start_time"))],
            ["Date de Fin:", self._format_timestamp(self.scan_results.get("end_time"))],
            ["Statut:", self.scan_results.get("status", "inconnu").capitalize()],
            ["Vulnérabilités Trouvées:", str(len(self.scan_results.get("vulnerabilities", [])))]
        ]

        meta_table = Table(meta_data, colWidths=[150, 350])
        meta_table.setStyle(TableStyle([
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#1a1a1f')),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor('#252530')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#333333')),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 20))

        summary = self._generate_summary()
        elements.append(Paragraph("Résumé des Résultats", styles['SectionHeader']))
        summary_table = Table(
            [[k.capitalize(), str(v)] for k, v in summary.items()],
            colWidths=[150, 350]
        )
        summary_table.setStyle(meta_table.style)
        elements.append(summary_table)
        elements.append(Spacer(1, 20))

        vulns = self.scan_results.get("vulnerabilities")
        if vulns:
            elements.append(PageBreak())
            elements.append(Paragraph("Détails des Vulnérabilités", styles['SectionHeader']))
            for i, vuln in enumerate(vulns, 1):
                elements.append(Paragraph(f"{i}. {vuln.get('name', 'Sans Nom')}", styles['VulnerabilityTitle']))
                vuln_data = [["Description:", vuln.get('description', 'N/A')],
                             ["Sévérité:", vuln.get('severity', 'inconnue').capitalize()],
                             ["URL:", vuln.get('url', 'N/A')],
                             ["Solution:", vuln.get('solution', 'Aucune')] ]
                if vuln.get('evidence'):
                    vuln_data.append(["Preuve:", vuln['evidence']])
                if vuln.get('reference'):
                    vuln_data.append(["Référence:", vuln['reference']])

                table = Table(vuln_data, colWidths=[100, 400])
                table.setStyle(meta_table.style)
                elements.append(table)
                elements.append(Spacer(1, 15))

        elements.append(Spacer(1, 20))
        elements.append(Paragraph("Rapport généré par CyberCrim - IA-Solution", styles['Italic']))
        elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Italic']))
        doc.build(elements)
        return filepath

    def _generate_summary(self) -> Dict[str, int]:
        summary = {"high": 0, "medium": 0, "low": 0, "info": 0}
        for vuln in self.scan_results.get("vulnerabilities", []):
            sev = vuln.get("severity", "info").lower()
            if sev in summary:
                summary[sev] += 1
        return summary

    @staticmethod
    def _format_timestamp(timestamp: Union[int, float, str, None]) -> str:
        if not timestamp:
            return "N/A"
        try:
            if isinstance(timestamp, (int, float)):
                dt = datetime.fromtimestamp(timestamp)
            else:
                dt = datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M:%S")
        except Exception:
            return str(timestamp)
