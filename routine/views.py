from django.shortcuts import render, redirect, get_object_or_404
from .models import ClassRoutine, MyNote, ExamRoutine
from .forms import ClassRoutineForm, MyNoteForm,ExamForm
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('tasks')  # Redirect to the task list
    else:
        form = RegistrationForm()
    return render(request, 'routine/register.html', {'form': form})  # Correct path to 'base/register.html'


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # This will log the user in
            messages.success(request, "Login successful!")
            return redirect('tasks')  # Redirect to task list or home
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'routine/login.html', {'form': form})

 
# CLASS ROUTINE VIEWS
def class_routine_list(request):
    routines = ClassRoutine.objects.all()
    return render(request, 'routine/class_routine_list.html', {'routines': routines})

def add_class_routine(request):
    if request.method == 'POST':
        form = ClassRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)
            # routine.user = request.user  ← remove user assignment
            routine.save()
            return redirect('class_routine_list')
    else:
        form = ClassRoutineForm()
    return render(request, 'routine/class_routine_form.html', {'form': form})

def edit_class_routine(request, pk):
    routine = get_object_or_404(ClassRoutine, pk=pk)
    if request.method == 'POST':
        form = ClassRoutineForm(request.POST, instance=routine)
        if form.is_valid():
            form.save()
            return redirect('class_routine_list')
    else:
        form = ClassRoutineForm(instance=routine)
    return render(request, 'routine/class_routine_form.html', {'form': form})

def delete_class_routine(request, pk):
    routine = get_object_or_404(ClassRoutine, pk=pk)
    routine.delete()
    return redirect('class_routine_list')
#exam

def exam_list(request):
    exams = ExamRoutine.objects.order_by('exam_date', 'start_time')
    return render(request, 'routine/exam_list.html', {'exams': exams})

def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm()
    return render(request, 'routine/add_exam.html', {'form': form})

def edit_exam(request, exam_id):
    exam = get_object_or_404(ExamRoutine, id=exam_id)
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            return redirect('exam_list')
    else:
        form = ExamForm(instance=exam)
    return render(request, 'routine/edit_exam.html', {'form': form})

def delete_exam(request, exam_id):
    exam = get_object_or_404(ExamRoutine, id=exam_id)
    exam.delete()
    return redirect('exam_list')


#filter:
def class_routine_list(request):
    day_filter = request.GET.get('day')
    search_query = request.GET.get('q')

    routines = ClassRoutine.objects.all()

    # Apply day filter only if it's selected
    if day_filter:
        routines = routines.filter(day=day_filter)

    # Apply search filter only if query is provided
    # if search_query:
    #     routines = routines.filter(subject__icontains=search_query)

    days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    return render(request, 'routine/class_routine_list.html', {
        'routines': routines,
        'day_filter': day_filter,
        # 'search_query': search_query,
        'days': days,
    })


def my_notes_view(request):
    notes = MyNote.objects.all().order_by('-created_at')

    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('my_notes')
    else:
        form = MyNoteForm()

    return render(request, 'routine/my_notes.html', {'form': form, 'notes': notes})

from django.shortcuts import get_object_or_404

def edit_note(request, pk):
    note = get_object_or_404(MyNote, pk=pk)
    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('routine/my_notes')
    else:
        form = MyNoteForm(instance=note)
    return render(request, 'routine/edit_note.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(MyNote, pk=pk)
    note.delete()
    return redirect('routine/my_notes')


