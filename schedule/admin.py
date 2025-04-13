from django.contrib import admin
from .models import Schedule
from .forms import ScheduleForm

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    form = ScheduleForm
    list_display = ('class_assignment', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week',)
