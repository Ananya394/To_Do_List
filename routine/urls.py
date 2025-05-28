# from django.urls import path
# from . import views

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     # Class Routine
#     path('classes/', views.class_routine_list, name='class_routine_list'),
#     path('classes/add/', views.add_class_routine, name='add_class_routine'),
#     path('classes/edit/<int:pk>/', views.edit_class_routine, name='edit_class_routine'),
#     path('classes/delete/<int:pk>/', views.delete_class_routine, name='delete_class_routine'),

#     # Exam Routine
#     path('exams/', views.exam_list, name='exam_list'),
#     path('exams/add/', views.add_exam, name='add_exam'),
#     path('exams/edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
#     path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),

#     #note
#     path('my-notes/', views.my_notes_view, name='my_notes'),
#     path('my-notes/edit/<int:pk>/', views.edit_note, name='edit_note'),
#     path('my-notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
# ]

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Authentication Views
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),

    # Profile Page
    path('profile/', views.user_profile, name='profile'),  # Profile URL
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'), 
    
    # Class Routine Views
    path('classes/', views.class_routine_list, name='class_routine_list'),
    path('classes/add/', views.add_class_routine, name='add_class_routine'),
    path('classes/edit/<int:pk>/', views.edit_class_routine, name='edit_class_routine'),
    path('classes/delete/<int:pk>/', views.delete_class_routine, name='delete_class_routine'),

    # Exam Routine Views
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/add/', views.add_exam, name='add_exam'),
    path('exams/edit/<int:exam_id>/', views.edit_exam, name='edit_exam'),
    path('exams/delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),

    # Notes Views
    path('class-routines/', views.class_routine_list, name='class_routine_list'),
    path('exam-routines/', views.exam_list, name='exam_list'),
    path('my-notes/edit/<int:pk>/', views.edit_task, name='edit_task'), 
    path('my-notes/add/', views.add_task, name='add_task'), 
    path('my-notes/', views.my_notes_view, name='my_notes'),
    path('my-notes/edit/<int:pk>/', views.edit_note, name='edit_note'),
    path('my-notes/delete/<int:pk>/', views.delete_note, name='delete_note'),
]

# Serve media files during development (for profile picture, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
