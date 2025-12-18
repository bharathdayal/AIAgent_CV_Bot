from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from docx import Document

def export_pdf(text: str) -> bytes:
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1 * inch,
        leftMargin=1 * inch,
        topMargin=1 * inch,
        bottomMargin=1 * inch
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "NameStyle",
        parent=styles["Normal"],
        fontSize=12,
        spaceAfter=14,
        leading=14
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=15,
        spaceAfter=12
    )

    story = []

    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    # Candidate Name (first line)
    story.append(Paragraph(paragraphs[0], name_style))
    story.append(Spacer(1, 12))

    # Remaining paragraphs
    for para in paragraphs[1:]:
        story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()


def export_word(text: str) -> bytes:
    buffer = BytesIO()
    doc = Document()

    for para in text.split("\n\n"):
        p = doc.add_paragraph(para)
        p.paragraph_format.space_after = 12

    doc.save(buffer)
    buffer.seek(0)
    return buffer.read()