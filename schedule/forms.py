from django import forms
from .models import Schedule
import datetime

def generate_time_choices(start=6, end=21, step=30):
    times = []
    current = datetime.datetime(100, 1, 1, start, 0)
    end_time = datetime.datetime(100, 1, 1, end, 0)
    while current <= end_time:
        value = current.time().strftime('%H:%M')
        label = current.time().strftime('%I:%M %p')
        times.append((value, label))
        current += datetime.timedelta(minutes=step)
    return times

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'start_time': forms.Select(choices=generate_time_choices()),
            'end_time': forms.Select(choices=generate_time_choices()),
        }
