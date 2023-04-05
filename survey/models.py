from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, EmailValidator


class Lead(models.Model):
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    score = models.IntegerField(
        default=0,
        blank=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(0),
        ],
    )

    def __str__(self):
        return f"{self.email}: {self.score} points"


class Survey(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE, null=True)

    def get_lead(self):
        return self.lead.email

    def get_questions(self):
        return self.questions.all()

    def __str__(self):
        return self.lead.email


class Question(models.Model):
    TYPES = [
        ("D", "Descriptive"),
        ("S", "Single Choice"),
        ("M", "Multiple Choice"),
    ]
    type = models.CharField(max_length=1, choices=TYPES)
    number = models.PositiveIntegerField(unique=True, null=True)
    text = models.CharField(max_length=255)

    def get_answer_options(self):
        if self.type != "D":
            options = Answer.objects.filter(question=self.pk).all()
            return options
        else:
            return None

    def __str__(self):
        return self.text


class Response(models.Model):
    survey = models.ForeignKey(
        Survey, on_delete=models.CASCADE, related_name="survey_responses"
    )
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="question_responses"
    )
    text = models.CharField(max_length=510)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=510, default="", blank=True)

    def __str__(self):
        return self.text
