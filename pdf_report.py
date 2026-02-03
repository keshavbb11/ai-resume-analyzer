from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(result):
    path = f"{result['Resume']}_report.pdf"
    doc = SimpleDocTemplate(path)
    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Resume Analysis Report", styles["Title"]),
        Paragraph(f"Final Score: {result['Score']}", styles["Normal"]),
        Paragraph("Missing Skills:", styles["Heading2"]),
        Paragraph(", ".join(result["Analysis"]["missing_skills"]), styles["Normal"]),
        Paragraph("Recommendations:", styles["Heading2"]),
        Paragraph(result["Recommendations"], styles["Normal"])
    ]

    doc.build(content)
    return path
