from django import forms
from .models import ClassRoutine,ExamRoutine

class ClassRoutineForm(forms.ModelForm):
    class Meta:
        model = ClassRoutine
        fields = ['subject', 'day', 'start_time', 'end_time', 'location']
        
    widgets = {
    'subject': forms.TextInput(attrs={'class': 'form-control'}),
    'day': forms.TextInput(attrs={'class': 'form-control'}),
    
    'start_time':forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
    'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
    'location': forms.TextInput(attrs={'class': 'form-control'}),
}
class ExamForm(forms.ModelForm):
    class Meta:
        model = ExamRoutine
        fields = ['course_name', 'exam_date', 'start_time', 'end_time', 'location', 'note']
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

        widgets = {
    'exam_date': forms.DateInput(attrs={'type': 'date'}),
    'start_time': forms.TimeInput(attrs={'type': 'time'}),
    'end_time': forms.TimeInput(attrs={'type': 'time'}),
}


from .models import MyNote

class MyNoteForm(forms.ModelForm):
    class Meta:
        model = MyNote
<<<<<<< Updated upstream
        fields = ['title', 'description', 'attachment', 'memory_prompt', 'attended']
=======
        fields = ['title', 'description', 'attachment', 'memory_prompt', 'attended', 'priority', 'due_date']

    # You can add any custom validation or styling here if needed


from django import forms
from .models import Activity, ChecklistItem

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            'title',
            'description',
            'category',
            'tags',
            'priority',
            'duration',
            'start_time',
            'end_time',
            'date',
            'status',
            'reminder_time',
        ]
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. #study #revision'}),
        }


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'is_done']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Checklist item'}),
        }
>>>>>>> Stashed changes
