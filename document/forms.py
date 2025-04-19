from django import forms
from .models import Document

class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file']
        labels = {
            'title': 'Título del documento',
            'document_type': 'Tipo de documento',
            'file': 'Archivo',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Ingrese el título del archivo',
            }),
            'document_type': forms.Select(attrs={
                'class': 'form-select mb-3',
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
            }),
        }
