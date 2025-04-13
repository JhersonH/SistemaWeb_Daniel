# views.py (en tu app principal o una app general)
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from class_assignment.models import ClassAssignment
from document.forms import DocumentUploadForm
from document.models import Document
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login')

@login_required
def teacher_dashboard(request):
    return render(request, 'dashboard/dashboard.html')

@login_required
def teacher_courses(request):
    assignments = ClassAssignment.objects.filter(teacher__user=request.user).select_related('course')
    paginator = Paginator(assignments, 15)  # 6 cards por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dashboard/teacher_courses.html', {'page_obj': page_obj})

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
