from django.contrib import admin, messages
from .models import ClassAssignment
from django.urls import reverse
from django.shortcuts import redirect

@admin.register(ClassAssignment)
class ClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'level', 'grade', 'section', 'academic_year')
    list_filter = ('level', 'grade', 'academic_year', 'teacher')

    def response_add(self, request, obj, post_url_continue=None):
        # Si se evitó el guardado, redirige sin éxito
        if hasattr(obj, '_skip_save') and obj._skip_save:
            msg = "⚠ Ya existe una asignación igual para este docente en ese año académico."
            self.message_user(request, msg, level=messages.ERROR)

            # Redirige al formulario sin el mensaje verde
            opts = self.model._meta
            redirect_url = reverse(f'admin:{opts.app_label}_{opts.model_name}_add')
            return redirect(redirect_url)

        return super().response_add(request, obj, post_url_continue)

    def save_model(self, request, obj, form, change):
        exists = ClassAssignment.objects.exclude(pk=obj.pk).filter(
            teacher=obj.teacher,
            course=obj.course,
            level=obj.level,
            grade=obj.grade,
            section=obj.section.upper(),
            academic_year=obj.academic_year
        ).exists()

        if exists:
            obj._skip_save = True  # Flag para detectar en response_add
            return  # Cancela el guardado sin error ni mensaje verde

        obj.section = obj.section.upper()
        super().save_model(request, obj, form, change)