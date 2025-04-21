from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from roles.models import Role


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    dni_validator = RegexValidator(
        regex=r'^\d{8,20}$',
        message='DNI must contain between 8 and 20 digits.'
    )
    dni = models.CharField(max_length=20, unique=True, validators=[dni_validator])

    birth_date = models.DateField()

    phone_validator = RegexValidator(
        regex=r'^\+?\d{9,11}$',
        message='Phone number must have 9 to 11 digits, optionally starting with "+".'
    )
    phone_number = models.CharField(max_length=12, validators=[phone_validator])

    address = models.CharField(max_length=255)

    LEVEL_CHOICES = [
        ('primaria', 'Primaria'),
        ('secundaria', 'Secundaria'),
    ]
    teaching_level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    area_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÿ\s]{1,30}$',
        message='Teaching area must contain only letters (max 30 characters).'
    )
    teaching_area = models.CharField(max_length=30, validators=[area_validator])

    CONDITION_CHOICES = [
        ('nombrado', 'Nombrado'),
        ('contratado', 'Contratado'),
        ('jubilado', 'Jubilado'),
    ]
    labor_condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)

    hiring_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    profession = models.CharField(max_length=50, blank=True)
    academic_degree = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
