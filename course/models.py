from django.db import models
from django.core.validators import RegexValidator

class Course(models.Model):
    name_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÿ\s]{1,30}$',
        message='Course name must contain only letters and be up to 30 characters.'
    )
    name = models.CharField(max_length=30, validators=[name_validator])

    LEVEL_CHOICES = [
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.level})"
