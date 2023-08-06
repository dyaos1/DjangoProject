from django.db import models
from django.contrib.auth.models import AbstractUser, User

# Create your models here.

class Member(models.Model):
    class CompanyChoices(models.TextChoices):
        ELIM = "elim"
        EL = "el"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.CharField(
        max_length=10, choices=CompanyChoices.choices, default=CompanyChoices.ELIM
    )
    department = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.user.username
