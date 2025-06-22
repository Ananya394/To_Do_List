

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Authentication Views
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # Profile Page
    path('profile/', views.user_profile, name='profile'),  # Profile URL
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='password_change'),
    
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # User Management
    path('user/edit/<int:pk>/', views.edit_user, name='edit_user'),  # URL for editing a user
    path('user/delete/<int:pk>/', views.delete_user, name='delete_user'),  # URL for deleting a user
    
    # Activity Management
    path('activity/edit/<int:pk>/', views.edit_activity, name='edit_activity'),  # URL for editing an activity
    path('activity/delete/<int:pk>/', views.delete_activity, name='delete_activity'),  # URL for deleting an activity
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('tasks/complete/<int:pk>/', views.complete_task, name='complete_task'),

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

    #task
    path('activities/', views.activity_list, name='activity_list'),
    path('activities/create/', views.activity_create, name='activity_create'),
    path('activities/<int:pk>/edit/', views.activity_edit, name='activity_edit'),
    path('activities/<int:pk>/delete/', views.activity_delete, name='activity_delete'),
    path('activities/<int:activity_id>/checklist/add/', views.checklist_add, name='checklist_add'),
    path('activities/<int:pk>/complete/', views.complete_activity, name='complete_activity'),
    path('activities/delete_selected/', views.delete_selected_activities, name='delete_selected_activities'),
    path('activities/delete_selected_completed/', views.delete_selected_completed_activities, name='delete_selected_completed_activities'),
    path('', views.activity_board, name='activity_board'),
    path('add/<str:category>/', views.add_activity, name='add_activity'),
    path('complete/<int:pk>/', views.complete_activity, name='complete_activity'),
    path('edit/<int:pk>/', views.activity_edit, name='activity_edit'),



    path('activities/review/', views.combined_review_summary, name='activity_review'),
    path('report/', views.efficiency_report, name='efficiency_report'),


]


# Serve media files during development (for profile picture, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
