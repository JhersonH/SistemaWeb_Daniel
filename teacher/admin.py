from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'teaching_level', 'teaching_area', 'labor_condition')
    search_fields = ('user__first_name', 'user__last_name', 'dni')
    list_filter = ('teaching_level', 'labor_condition')
