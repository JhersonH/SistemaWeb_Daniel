from django.db import models
from django.core.validators import RegexValidator
from class_assignment.models import ClassAssignment

class Schedule(models.Model):
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE)

    DAY_CHOICES = [
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miércoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ]

    day_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÿ]+$',
        message='Day of the week must contain only letters.'
    )

    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, validators=[day_validator])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_assignment} - {self.day_of_week.capitalize()} {self.start_time} to {self.end_time}"
