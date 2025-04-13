from django.contrib import admin
from .models import ClassAssignment

@admin.register(ClassAssignment)
class ClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'course', 'level', 'grade', 'section', 'academic_year')
    list_filter = ('level', 'academic_year')
    search_fields = ('teacher__user__first_name', 'teacher__user__last_name', 'course__name')
