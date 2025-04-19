from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('courses/', views.teacher_courses, name='teacher_courses'),
    path('my-courses/<int:assignment_id>/', views.course_detail, name='course_detail'),
    path('documents/', views.teacher_documents, name='teacher_documents'),
    path('documents/delete/<int:document_id>/', views.delete_document, name='delete_document'),
    path('schedules/', views.teacher_schedule, name='teacher_schedule'),
    path('schedules/register/', views.add_schedule, name='add_schedule'),
    path('schedules/delete/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),
    path('profile/', views.teacher_profile, name='teacher_profile'),
    path('profile/edit/', views.edit_teacher_profile, name='edit_teacher_profile'),
    path('profile/password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
]
