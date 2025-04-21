from django.db import models

class Role(models.Model):
    ROLE_CHOICES = [
        ('teacher', 'Docente'),
        ('student', 'Alumno'),
        ('director', 'Director'),
        ('subdirector', 'Subdirector'),
        ('coordinator', 'Coordinador'),
        ('secretary', 'Secretaria'),
        ('admin', 'Administrador'),
        ('authorized', 'Apoderado'),
    ]

    role_type = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name='Rol'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_role_type_display()
