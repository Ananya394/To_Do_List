# from .models import ClassRoutine, ExamRoutine
# from django.contrib import admin

# admin.site.register(ClassRoutine)
# admin.site.register(ExamRoutine)

from django.contrib import admin
from .models import ClassRoutine, ExamRoutine, MyNote

# Register ClassRoutine Model
@admin.register(ClassRoutine)
class ClassRoutineAdmin(admin.ModelAdmin):
    list_display = ('subject', 'day', 'start_time', 'end_time', 'location')  # Fields to display in admin list view

# Register ExamRoutine Model
@admin.register(ExamRoutine)
class ExamRoutineAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'exam_date', 'start_time', 'end_time', 'location', 'note')  # Fields to display in admin list view

# Register MyNote Model
@admin.register(MyNote)
class MyNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'priority', 'due_date', 'attended', 'created_at')  # Fields to display in admin list view
    search_fields = ('title', 'description')  # Add search fields for easier filtering
    list_filter = ('priority', 'attended')  # Add filters for easy filtering in the admin
