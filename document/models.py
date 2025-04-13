from django.db import models
from class_assignment.models import ClassAssignment
from django.core.validators import FileExtensionValidator, RegexValidator

class Document(models.Model):
    class_assignment = models.ForeignKey(ClassAssignment, on_delete=models.CASCADE)

    title_validator = RegexValidator(
        regex=r'^[A-Za-zÀ-ÿ0-9\s\-_.]{3,50}$',
        message='Title must be 3–50 characters long and contain only letters, numbers, spaces, hyphens, underscores, or dots.'
    )
    title = models.CharField(max_length=50, validators=[title_validator])

    description = models.TextField(blank=True, null=True)

    DOCUMENT_TYPE_CHOICES = [
        ('evaluation', 'Evaluation'),
        ('material', 'Material'),
        ('report', 'Report'),
    ]
    document_type = models.CharField(max_length=15, choices=DOCUMENT_TYPE_CHOICES)

    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'ppt', 'pptx'])]
    )

    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.class_assignment})"
