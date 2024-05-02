from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Specialization(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100)  # Иконка для отображения

    def __str__(self):
        return self.title


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


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_added = models.DateTimeField(auto_now_add=True)
    biography = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="candidate_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization.title}"
