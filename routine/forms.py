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
        fields = ['title', 'description', 'attachment', 'memory_prompt', 'attended']
