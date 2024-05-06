from django.db import models
from django.contrib.auth.models import User


class Specialization(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    biography = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="candidate_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization.title if self.specialization else 'No Specialization'}"


class TestAttempt(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def score(self):
        return (self.correct_answers / self.total_questions) * 100

    def passed(self):
        return self.score() >= 80  # Например, считаем, что 80% - проходной порог

    def __str__(self):
        return f"Attempt by {self.candidate} for {self.specialization.title}"


class Question(models.Model):
    text = models.CharField(max_length=255)
    specialization = models.ForeignKey(
        Specialization, related_name="questions", on_delete=models.CASCADE
    )


class Choice(models.Model):
    text = models.CharField(max_length=255)
    question = models.ForeignKey(
        Question, related_name="choices", on_delete=models.CASCADE
    )
    is_correct = models.BooleanField(default=False)


class ContactRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact request from {self.name}"
