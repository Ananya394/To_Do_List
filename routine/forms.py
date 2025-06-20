from django import forms
from .models import ClassRoutine,ExamRoutine
from django.contrib.auth.models import User
from .models import MyNote
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']  

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

    def save(self, commit=True):
      
        user = super().save(commit=False)
      
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save() 
        
        return user

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






class MyNoteForm(forms.ModelForm):
    class Meta:
        model = MyNote
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
            #'category',
            'tags',
            'priority',
            #'duration',
            #'start_time',
            #'end_time',
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
            #'tags': forms.TextInput(attrs={'placeholder': 'e.g. #study #revision'}),
            'tags': forms.TextInput(attrs={'placeholder': 'e.g. #study #revision',
                    'value': '#general'  # Default tag shown in form
            }),

        }


class ChecklistItemForm(forms.ModelForm):
    class Meta:
        model = ChecklistItem
        fields = ['description', 'is_done']
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Checklist item'}),
        }


class ActivityQuickForm(forms.ModelForm):  # used for board-style quick add
    class Meta:
        model = Activity
        fields = ['title', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
