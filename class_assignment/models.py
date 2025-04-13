from django.db import models
from teacher.models import Teacher
from course.models import Course

class ClassAssignment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    LEVEL_CHOICES = [
        ('initial', 'Initial'),
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
    ]
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    grade = models.PositiveSmallIntegerField()

    section = models.CharField(max_length=1)

    academic_year = models.CharField(max_length=4)

    def save(self, *args, **kwargs):
        if self.section:
            self.section = self.section.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.course.name} - {self.level.capitalize()} {self.grade}{self.section} ({self.academic_year})"
