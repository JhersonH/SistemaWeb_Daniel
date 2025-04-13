from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from class_assignment.models import ClassAssignment
from document.models import Document
from document.forms import DocumentUploadForm

@login_required
def teacher_dashboard(request):
    user = request.user
    assignments = ClassAssignment.objects.filter(teacher__user=user)
    documents = Document.objects.filter(class_assignment__teacher__user=user)

    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        form.fields['class_assignment'].queryset = assignments
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = DocumentUploadForm()
        form.fields['class_assignment'].queryset = assignments

    return render(request, 'dashboard/dashboard.html', {
        'user': user,
        'class_assignments': assignments,
        'documents': documents,
        'form': form
    })
