from django.urls import path
from . import views

urlpatterns = [
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


    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    path('activities/<int:activity_id>/checklist/add/', views.checklist_add, name='checklist_add'),
    path('activities/<int:pk>/complete/', views.activity_complete, name='activity_complete'),

]

