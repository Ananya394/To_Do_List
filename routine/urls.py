from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # Class Routine
    path('classes/', views.class_routine_list, name='class_routine_list'),
    path('classes/add/', views.add_class_routine, name='add_class_routine'),
    path('classes/edit/<int:pk>/', views.edit_class_routine, name='edit_class_routine'),
    path('classes/delete/<int:pk>/', views.delete_class_routine, name='delete_class_routine'),

    # Exam Routine
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),

    #note
    path('my-notes/', views.my_notes_view, name='my_notes'),
    path('my-notes/edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('my-notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
]

