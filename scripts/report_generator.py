"""
Report Generator — HTML Network Reports

Generates professional HTML reports from health check and compliance data
for management review and audit documentation.
"""

from datetime import datetime
from pathlib import Path


def generate_html_report(title: str, sections: list[dict], output_path: str) -> str:
    """Generate a styled HTML report."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 40px; background: #f5f5f5; color: #333; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a5276; border-bottom: 3px solid #1a5276; padding-bottom: 10px; }}
        h2 {{ color: #2c3e50; margin-top: 30px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #1a5276; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f0f7fc; }}
        .status-healthy {{ color: #27ae60; font-weight: bold; }}
        .status-warning {{ color: #f39c12; font-weight: bold; }}
        .status-critical {{ color: #e74c3c; font-weight: bold; }}
        .footer {{ margin-top: 30px; text-align: center; color: #888; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
"""

    for section in sections:
        html += f"<h2>{section['title']}</h2>\n"
        if "table" in section:
            html += "<table><thead><tr>"
            for header in section["table"]["headers"]:
                html += f"<th>{header}</th>"
            html += "</tr></thead><tbody>"
            for row in section["table"]["rows"]:
                html += "<tr>"
                for cell in row:
                    css_class = ""
                    if cell in ("healthy", "pass"):
                        css_class = ' class="status-healthy"'
                    elif cell in ("warning",):
                        css_class = ' class="status-warning"'
                    elif cell in ("critical", "fail"):
                        css_class = ' class="status-critical"'
                    html += f"<td{css_class}>{cell}</td>"
                html += "</tr>"
            html += "</tbody></table>"

    html += """
        <div class="footer">
            <p>NetOps Toolkit — Automated Network Report</p>
        </div>
    </div>
</body>
</html>"""

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(html)
    return output_path


if __name__ == "__main__":
    sections = [
        {
            "title": "Device Health Summary",
            "table": {
                "headers": ["Device", "CPU", "Memory", "Uptime", "Status"],
                "rows": [
                    ["CORE-SW-01", "23%", "45%", "142 days", "healthy"],
                    ["CORE-SW-02", "31%", "52%", "142 days", "healthy"],
                    ["DIST-SW-BR01", "67%", "78%", "89 days", "warning"],
                    ["ACC-SW-FL3-01", "88%", "82%", "45 days", "critical"],
                ],
            },
        },
    ]
    path = generate_html_report("Network Health Report", sections, "reports/health_report.html")
    print(f"Report generated: {path}")
