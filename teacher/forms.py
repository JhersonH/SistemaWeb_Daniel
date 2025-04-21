from django import forms
from django.contrib.auth.models import User
from .models import Teacher

class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
            'placeholder': 'Ingresa tus nombres'
        }),
        error_messages={'required': 'El nombre es obligatorio.'}
    )

    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
            'placeholder': 'Ingresa tus apellidos'
        }),
        error_messages={'required': 'El apellido es obligatorio.'}
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
            'placeholder': 'Ingresa tu correo electrónico'
        }),
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'invalid': 'Ingresa un correo válido.'
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        exclude = ['user']

        widgets = {
            'dni': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: 12345678'
            }),
            'birth_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: 987654321'
            }),
            'address': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: Av. Los Próceres 123'
            }),
            'teaching_area': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: Matemática'
            }),
            'profession': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: Ingeniero de Sistemas'
            }),
            'academic_degree': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200',
                'placeholder': 'Ej: Licenciado'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200 resize-none'
            }),
            'hiring_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200'
            }),
            'teaching_level': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200'
            }),
            'labor_condition': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-4 py-2 focus:ring focus:ring-blue-200'
            }),
        }

        error_messages = {
            'dni': {'required': 'El DNI es obligatorio.'},
            'birth_date': {'required': 'La fecha de nacimiento es obligatoria.'},
            'phone_number': {'required': 'El número de teléfono es obligatorio.'},
            'address': {'required': 'La dirección es obligatoria.'},
            'teaching_level': {'required': 'El nivel de enseñanza es obligatorio.'},
            'teaching_area': {'required': 'El área de enseñanza es obligatoria.'},
            'labor_condition': {'required': 'La condición laboral es obligatoria.'},
            'hiring_date': {'required': 'La fecha de contratación es obligatoria.'},
            'profession': {'required': 'La profesión es obligatoria.'},
            'academic_degree': {'required': 'El grado académico es obligatorio.'},
        }

    # Validaciones explícitas para asegurar que los campos requeridos funcionen correctamente
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni:
            raise forms.ValidationError("El DNI es obligatorio.")
        return dni

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not phone:
            raise forms.ValidationError("El número de teléfono es obligatorio.")
        return phone

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise forms.ValidationError("La dirección es obligatoria.")
        return address

    def clean_profession(self):
        profession = self.cleaned_data.get('profession')
        if not profession:
            raise forms.ValidationError("La profesión es obligatoria.")
        return profession

    def clean_academic_degree(self):
        degree = self.cleaned_data.get('academic_degree')
        if not degree:
            raise forms.ValidationError("El grado académico es obligatorio.")
        return degree
