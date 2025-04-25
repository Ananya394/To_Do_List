from django import forms
from .models import ClassRoutine,ExamRoutine
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']  # Allow the user to update bio and profile picture

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

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
