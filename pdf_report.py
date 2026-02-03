from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor


def generate_pdf(result):
    filename = f"{result['Resume']}_analysis_report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=HexColor("#1e293b")
    )

    heading_style = ParagraphStyle(
        "HeadingStyle",
        fontSize=14,
        spaceBefore=14,
        spaceAfter=8,
        textColor=HexColor("#2563eb")
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        fontSize=11,
        spaceAfter=6,
        textColor=HexColor("#0f172a")
    )

    score_style = ParagraphStyle(
        "ScoreStyle",
        fontSize=13,
        spaceAfter=12,
        textColor=HexColor("#16a34a")
    )

    elements = []

    # ---------------- Title ----------------
    elements.append(Paragraph("AI Resume Analysis Report", title_style))
    elements.append(Spacer(1, 10))

    
    elements.append(Paragraph(
        f"<b>Final Score:</b> {result['Score']} / 10",
        score_style
    ))

  
    elements.append(Paragraph("Missing Skills", heading_style))

    missing_skills = result["Analysis"].get("missing_skills", [])
    if missing_skills:
        elements.append(
            ListFlowable(
                [ListItem(Paragraph(skill, body_style)) for skill in missing_skills],
                bulletType="bullet"
            )
        )
    else:
        elements.append(Paragraph("No major missing skills identified.", body_style))

  
    elements.append(Paragraph("Skill Evaluation", heading_style))

    scores = result["Analysis"]
    elements.append(Paragraph(f"Skills Score: {scores['skills_score']} / 100", body_style))
    elements.append(Paragraph(f"Experience Score: {scores['experience_score']} / 100", body_style))
    elements.append(Paragraph(f"Projects Score: {scores['projects_score']} / 100", body_style))
    elements.append(Paragraph(f"Clarity Score: {scores['clarity_score']} / 100", body_style))

   
    elements.append(Paragraph("Recommendations", heading_style))

    recommendations_text = result["Recommendations"].split("*")
    recommendations_clean = [r.strip() for r in recommendations_text if r.strip()]

    elements.append(
        ListFlowable(
            [ListItem(Paragraph(rec, body_style)) for rec in recommendations_clean],
            bulletType="bullet"
        )
    )

    
    elements.append(Spacer(1, 20))
    elements.append(
        Paragraph(
            "This report is generated using AI-assisted analysis and should be used as guidance, not a final hiring decision.",
            ParagraphStyle(
                "FooterStyle",
                fontSize=9,
                textColor=HexColor("#64748b")
            )
        )
    )

    doc.build(elements)
    return filename
