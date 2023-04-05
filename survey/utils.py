from io import BytesIO
from threading import Lock
from django.core.mail import EmailMessage
from django.conf import settings
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


# Creating a global lock object for thread-safety
lock = Lock()


def calculate_score(responses):
    # Total number of questions that are non-descriptive and can be scored
    total = 0
    points = 0

    for response in responses:
        if response.question.type == "M":
            answer_list = response.text.split(", ")
            option_list = response.question.answers.all()
            option_list_length = len(option_list)
            total += option_list_length
            points += option_list_length
            for option in option_list:
                if option.text in answer_list:
                    points -= 1
    score = round((points / total) * 100)
    return score


def generate_report(questions, responses, email, score):
    buffer = BytesIO()

    # Locking the thread because reportlab is not thread-safe
    lock.acquire()

    try:
        # Initialize a canned PDF using PLATYPUS DocTemplate
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        elements = []

        # Define styles
        stylesheet = getSampleStyleSheet()
        title_style = stylesheet["Title"]
        question_style = stylesheet["Heading1"]
        answer_style = stylesheet["Normal"]

        # Add title
        elements.append(Paragraph(f"Good Life Report for {email}", title_style))

        # Define table styles
        table_style = TableStyle(
            [
                # Question column
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                # Answer column
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.black),
                ("ALIGN", (0, 1), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                # Table grid
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )

        # Define table data
        table_data = []
        for i in range(len(questions)):
            table_data.append(
                [
                    Paragraph(questions[i].text, question_style),
                    Paragraph(responses[i].text, answer_style),
                ]
            )

        table = Table(table_data)
        table.setStyle(table_style)

        # Add table
        elements.append(table)

        # Add score
        elements.append(Paragraph(f"Score: {score}", title_style))

        # Add custom message based on score
        custom_msg = ""
        if score <= 50:
            custom_msg = "You require much improvement, though. But I can help you out. Join my site goodlife.com to improve all aspects of your life!"
        elif score > 50:
            custom_msg = "You're already doing well. Join goodlife.com to reach even greater heights!"
        message = f"Thanks for taking the survey. {custom_msg}"
        elements.append(Paragraph(message, answer_style))
        doc.build(elements)

        report = buffer.getvalue()
        buffer.seek(0)

    finally:
        lock.release()

    return report


def mail_report(report, to):
    subject = "Good Life Report"
    body = "Here is your FREE Good Life Report, attached with this mail. Check it out and take the recommended action to live a great life!"
    from_email = settings.EMAIL_HOST_USER
    email = EmailMessage(subject, body, from_email, [to])
    email.attach("good_life_report.pdf", report, "application/pdf")
    email.send()
