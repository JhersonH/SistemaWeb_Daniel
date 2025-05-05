# views.py (en tu app principal o una app general)
from datetime import datetime
from collections import defaultdict
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from class_assignment.models import ClassAssignment
from schedule.models import Schedule
from document.forms import DocumentUploadForm
from document.models import Document
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from teacher.decorators import role_required
from teacher.forms import UserForm, TeacherForm
from teacher.models import Teacher
from django.utils.timezone import localtime
from collections import Counter
from datetime import timedelta
import json
import unicodedata

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        messages.error(self.request, "Usuario o contraseña incorrecta.")
        return super().form_invalid(form)

@login_required
def teacher_dashboard(request):
    user = request.user

    # Clases asignadas
    assignments = ClassAssignment.objects.filter(teacher__user=user)

    # Cursos por nivel
    level_counts = {'primaria': 0, 'secundaria': 0}
    for assignment in assignments:
        level_counts[assignment.level] += 1

    courses_levels_labels = json.dumps(['Primaria', 'Secundaria'])
    courses_levels_data = [level_counts['primaria'], level_counts['secundaria']]

    # Documentos por tipo
    documents = Document.objects.filter(class_assignment__in=assignments)
    doc_types = {'evaluacion': 0, 'material': 0, 'reporte': 0}
    for doc in documents:
        doc_types[doc.document_type] += 1

    documents_types_labels = json.dumps(['Evaluación', 'Material', 'Reporte'])
    documents_types_data = [doc_types['evaluacion'], doc_types['material'], doc_types['reporte']]

    # Clases por día
    schedules = Schedule.objects.filter(class_assignment__in=assignments)
    day_counts = Counter(schedule.day_of_week.lower() for schedule in schedules)
    days_order = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']

    schedules_labels = json.dumps([day.capitalize() for day in days_order])
    schedules_data = [day_counts.get(day, 0) for day in days_order]

    # Duración total por día
    durations_by_day = {day: timedelta() for day in days_order}

    for sched in schedules:
        day = sched.day_of_week.lower()
        start = sched.start_time
        end = sched.end_time

        # Calcular duración de la clase
        start_delta = timedelta(hours=start.hour, minutes=start.minute)
        end_delta = timedelta(hours=end.hour, minutes=end.minute)
        durations_by_day[day] += (end_delta - start_delta)

    # Convertir a horas reales con decimales exactos
    minutes_per_day_data = [int(durations_by_day[day].total_seconds() // 60) for day in days_order]

    context = {
        'courses_levels_labels': courses_levels_labels,
        'courses_levels_data': courses_levels_data,
        'documents_types_labels': documents_types_labels,
        'documents_types_data': documents_types_data,
        'schedules_labels': schedules_labels,
        'schedules_data': schedules_data,
        'hours_per_day_data': minutes_per_day_data
    }

    return render(request, 'dashboard/home_dashboard.html', context)

@login_required
def teacher_courses(request):
    current_year = str(datetime.now().year)
    assignments = ClassAssignment.objects.filter(teacher__user=request.user)

    # Separamos por año actual y anteriores
    current_year_courses = [a for a in assignments if a.academic_year == current_year]
    past_courses_grouped = defaultdict(list)

    for assignment in assignments:
        if assignment.academic_year != current_year:
            past_courses_grouped[assignment.academic_year].append(assignment)

    # Ordenamos cursos actuales por nombre
    current_year_courses.sort(key=lambda a: a.course.name.lower())

    # Ordenamos cursos anteriores por año DESC y por nombre ASC
    past_years_courses = {
        year: sorted(course_list, key=lambda a: a.course.name.lower())
        for year, course_list in sorted(past_courses_grouped.items(), reverse=True)
    }

    # Paginamos cursos del año actual (5 por página, por ejemplo)
    current_page_number = request.GET.get("page")
    current_paginator = Paginator(current_year_courses, 4)
    current_year_page_obj = current_paginator.get_page(current_page_number)

    return render(request, 'dashboard/teacher_courses.html', {
        'current_year': current_year,
        'current_year_page_obj': current_year_page_obj,
        'current_year_courses': current_year_page_obj,  # alias para el template
        'past_years_courses': past_years_courses
    })

@login_required
def course_detail(request, assignment_id):
    user = request.user
    assignment = get_object_or_404(ClassAssignment, id=assignment_id, teacher__user=user)
    documents = Document.objects.filter(class_assignment=assignment)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.class_assignment = assignment  # Forzamos la asignación segura
            doc.save()
            return redirect('course_detail', assignment_id=assignment.id)
    else:
        form = DocumentUploadForm()

    return render(request, 'dashboard/course_detail.html', {
        'assignment': assignment,
        'documents': documents,
        'form': form
    })


@login_required
def teacher_documents(request):
    user = request.user
    documents = Document.objects.filter(class_assignment__teacher__user=user).select_related('class_assignment__course')

    # Filtros
    course_filter = request.GET.get('course')
    year_filter = request.GET.get('year')

    if course_filter:
        documents = documents.filter(class_assignment__course__name__icontains=course_filter)
    if year_filter:
        documents = documents.filter(class_assignment__academic_year=year_filter)

    # Cursos y años únicos para los filtros
    all_courses = Document.objects.filter(class_assignment__teacher__user=user).values_list('class_assignment__course__name', flat=True).distinct().order_by('class_assignment__course__name')
    all_years = Document.objects.filter(class_assignment__teacher__user=user).values_list('class_assignment__academic_year', flat=True).distinct().order_by('-class_assignment__academic_year')

    # Paginación
    paginator = Paginator(documents, 20)  # 10 documentos por página
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/teacher_documents.html', {
        'documents': page_obj,
        'all_courses': all_courses,
        'all_years': all_years,
        'course_filter': course_filter,
        'year_filter': year_filter
    })

@login_required
def delete_document(request, document_id):
    document = get_object_or_404(Document, id=document_id, class_assignment__teacher__user=request.user)

    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Documento eliminado correctamente.')
    else:
        messages.error(request, 'Acción no permitida.')

    # Redirecciona conservando filtros si los hubiera
    referer = request.META.get('HTTP_REFERER', reverse('teacher_documents'))
    return redirect(referer)

@login_required
def teacher_schedule(request):
    user = request.user
    current_year = str(datetime.now().year)

    teacher = get_object_or_404(Teacher, user=user)

    # Cursos asignados
    assignments = ClassAssignment.objects.filter(teacher=teacher, academic_year=current_year)

    # Todos los horarios
    schedules = Schedule.objects.filter(class_assignment__in=assignments)

    # Día actual (ej: 'Lunes')
    current_day = localtime(now()).strftime('%A')

    day_translation = {
        'Monday': 'Lunes',
        'Tuesday': 'Martes',
        'Wednesday': 'Miércoles',
        'Thursday': 'Jueves',
        'Friday': 'Viernes',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo',
    }

    today_name = day_translation[current_day]  # Ej: "Miércoles"

    # 🔥 Normaliza nombres y compara sin tildes y en minúscula
    normalized_today = normalize_string(today_name)

    weekly_schedules = [
        sched for sched in schedules
        if normalize_string(sched.day_of_week) == normalized_today
    ]

    # Ordenamos por hora
    weekly_schedules.sort(key=lambda x: x.start_time)

    # Construir eventos para el calendario
    events = []
    dow = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    for sched in schedules:
        day_index = dow.index(sched.day_of_week.capitalize())
        events.append({
            'title': f"{sched.class_assignment.course.name} ({sched.start_time.strftime('%H:%M')} - {sched.end_time.strftime('%H:%M')})",
            'daysOfWeek': [str((day_index + 1) % 7)],  # Lunes=1, ..., Domingo=0
            'startTime': sched.start_time.strftime('%H:%M'),
            'endTime': sched.end_time.strftime('%H:%M'),
            'display': 'block',
            'id': sched.id
        })

    return render(request, 'dashboard/teacher_schedule.html', {
        'events_json': json.dumps(events),
        'assignments': assignments,
        'weekly_schedules': weekly_schedules
    })

def normalize_string(value):
    return ''.join(
        c for c in unicodedata.normalize('NFD', value)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Función auxiliar para convertir día a índice FullCalendar (0=domingo, ..., 6=sábado)
def get_day_index(day):
    days = {
        'domingo': 0,
        'lunes': 1,
        'martes': 2,
        'miércoles': 3,
        'miercoles': 3,
        'jueves': 4,
        'viernes': 5,
        'sábado': 6,
        'sabado': 6
    }
    return days.get(day.lower(), 0)

@role_required('teacher')
@login_required
def add_schedule(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        assignment_id = request.POST.get('class_assignment')

        # Verificamos que la clase pertenezca al docente logueado
        try:
            assignment = ClassAssignment.objects.get(id=assignment_id, teacher__user=request.user)
            Schedule.objects.create(
                class_assignment=assignment,
                day_of_week=day,
                start_time=start_time,
                end_time=end_time
            )
            messages.success(request, 'Horario registrado correctamente.')
        except ClassAssignment.DoesNotExist:
            messages.error(request, 'No tienes permiso para registrar ese horario.')

    return redirect('teacher_schedule')

@role_required('teacher')
@login_required
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id, class_assignment__teacher__user=request.user)

    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Horario eliminado correctamente.')

    return redirect('teacher_schedule')

@login_required
def teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    return render(request, 'dashboard/teacher_profile.html', {'teacher': teacher})

@role_required('teacher')
@login_required
def edit_teacher_profile(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    user = request.user

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        teacher_form = TeacherForm(request.POST, request.FILES, instance=teacher)

        if user_form.is_valid() and teacher_form.is_valid():
            if user_form.has_changed() or teacher_form.has_changed():
                user_form.save()
                teacher_form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
            else:
                messages.info(request, 'No se realizaron cambios en el perfil.')

            # ✅ Redirige SOLO cuando está todo bien
            return redirect('teacher_profile')
        # ⛔ No rediriges si hay errores, solo renderizas la vista actual
    else:
        user_form = UserForm(instance=user)
        teacher_form = TeacherForm(instance=teacher)

    return render(request, 'dashboard/edit_teacher_profile.html', {
        'user_form': user_form,
        'teacher_form': teacher_form,
        'teacher': teacher,
        'user': user
    })

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'dashboard/change_password.html'
    success_url = reverse_lazy('teacher_profile')

    def form_valid(self, form):
        messages.success(self.request, _('Tu contraseña ha sido actualizada correctamente.'))
        return super().form_valid(form)