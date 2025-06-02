# from django.shortcuts import render, redirect, get_object_or_404
# from .models import ClassRoutine, MyNote, ExamRoutine
# from .forms import ClassRoutineForm, MyNoteForm,ExamForm
# from django.http import JsonResponse
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.forms import AuthenticationForm
# from .forms import RegistrationForm
# from django.contrib import messages

# from .models import UserProfile
# from django.contrib.auth.decorators import login_required

# @login_required
# def user_profile(request):
#     # Get the user's profile
#     profile = get_object_or_404(UserProfile, user=request.user)
    
#     # Render the profile page
#     return render(request, 'profile.html', {'profile': profile})

# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             login(request, user)
#             return redirect('login')  # Redirect to the task list
#     else:
#         form = RegistrationForm()
#     return render(request, 'routine/register.html', {'form': form})  # Correct path to 'base/register.html'


# def user_login(request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)  # This will log the user in
#             messages.success(request, "Login successful!")
#             return redirect('profile')  # Redirect to profile page after successful login
#         else:
#             messages.error(request, "Invalid credentials.")
#     else:
#         form = AuthenticationForm()
#     return render(request, 'routine/login.html', {'form': form})
# # CLASS ROUTINE VIEWS
# def class_routine_list(request):
#     routines = ClassRoutine.objects.all()
#     return render(request, 'routine/class_routine_list.html', {'routines': routines})

# def add_class_routine(request):
#     if request.method == 'POST':
#         form = ClassRoutineForm(request.POST)
#         if form.is_valid():
#             routine = form.save(commit=False)
#             # routine.user = request.user  ← remove user assignment
#             routine.save()
#             return redirect('class_routine_list')
#     else:
#         form = ClassRoutineForm()
#     return render(request, 'routine/class_routine_form.html', {'form': form})

# def edit_class_routine(request, pk):
#     routine = get_object_or_404(ClassRoutine, pk=pk)
#     if request.method == 'POST':
#         form = ClassRoutineForm(request.POST, instance=routine)
#         if form.is_valid():
#             form.save()
#             return redirect('class_routine_list')
#     else:
#         form = ClassRoutineForm(instance=routine)
#     return render(request, 'routine/class_routine_form.html', {'form': form})

# def delete_class_routine(request, pk):
#     routine = get_object_or_404(ClassRoutine, pk=pk)
#     routine.delete()
#     return redirect('class_routine_list')
# #exam

# def exam_list(request):
#     exams = ExamRoutine.objects.order_by('exam_date', 'start_time')
#     return render(request, 'routine/exam_list.html', {'exams': exams})

# def add_exam(request):
#     if request.method == 'POST':
#         form = ExamForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('exam_list')
#     else:
#         form = ExamForm()
#     return render(request, 'routine/add_exam.html', {'form': form})

# def edit_exam(request, exam_id):
#     exam = get_object_or_404(ExamRoutine, id=exam_id)
#     if request.method == 'POST':
#         form = ExamForm(request.POST, instance=exam)
#         if form.is_valid():
#             form.save()
#             return redirect('exam_list')
#     else:
#         form = ExamForm(instance=exam)
#     return render(request, 'routine/edit_exam.html', {'form': form})

# def delete_exam(request, exam_id):
#     exam = get_object_or_404(ExamRoutine, id=exam_id)
#     exam.delete()
#     return redirect('exam_list')


# #filter:
# def class_routine_list(request):
#     day_filter = request.GET.get('day')
#     search_query = request.GET.get('q')

#     routines = ClassRoutine.objects.all()

#     # Apply day filter only if it's selected
#     if day_filter:
#         routines = routines.filter(day=day_filter)

#     # Apply search filter only if query is provided
#     # if search_query:
#     #     routines = routines.filter(subject__icontains=search_query)

#     days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

#     return render(request, 'routine/class_routine_list.html', {
#         'routines': routines,
#         'day_filter': day_filter,
#         # 'search_query': search_query,
#         'days': days,
#     })


# def my_notes_view(request):
#     notes = MyNote.objects.all().order_by('-created_at')

#     if request.method == 'POST':
#         form = MyNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('my_notes')
#     else:
#         form = MyNoteForm()

#     return render(request, 'routine/my_notes.html', {'form': form, 'notes': notes})

# from django.shortcuts import get_object_or_404

# def edit_note(request, pk):
#     note = get_object_or_404(MyNote, pk=pk)
#     if request.method == 'POST':
#         form = MyNoteForm(request.POST, request.FILES, instance=note)
#         if form.is_valid():
#             form.save()
#             return redirect('routine/my_notes')
#     else:
#         form = MyNoteForm(instance=note)
#     return render(request, 'routine/edit_note.html', {'form': form, 'note': note})

# def delete_note(request, pk):
#     note = get_object_or_404(MyNote, pk=pk)
#     note.delete()
#     return redirect('routine/my_notes')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, ClassRoutineForm, MyNoteForm, ExamForm
from .models import UserProfile, ClassRoutine, MyNote, ExamRoutine
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def class_routine_list(request):
    day_filter = request.GET.get('day')
    routines = ClassRoutine.objects.filter(user=request.user)
    if day_filter:
        routines = routines.filter(day=day_filter)

    days = ClassRoutine.objects.filter(user=request.user).values_list('day', flat=True).distinct()

    return render(request, 'routine/class_routine_list.html', {
        'routines': routines,
        'days': sorted(days),
        'selected_day': day_filter,
    })


@login_required
def exam_list(request):
    exams = ExamRoutine.objects.filter(user=request.user).order_by('exam_date', 'start_time')  # Fetch exams for the logged-in user
    return render(request, 'routine/exam_list.html', {'exams': exams})


def edit_task(request, pk):
    task = get_object_or_404(MyNote, pk=pk)

    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES, instance=task)
        if form.is_valid():
            form.save()
            return redirect('my_notes')  # Redirect after saving the task
    else:
        form = MyNoteForm(instance=task)

    return render(request, 'routine/my_note_form.html', {'form': form})


@login_required
def dashboard(request):
    # Get tasks related to the logged-in user
    tasks = MyNote.objects.filter(user=request.user).order_by('-created_at')
    
    # You can also filter tasks by completion status or other criteria
    pending_tasks = tasks.filter(attended=False)
    completed_tasks = tasks.filter(attended=True)

    # Optionally, pass task progress, e.g., completed vs pending
    total_tasks = tasks.count()
    completed = completed_tasks.count()
    progress_percentage = (completed / total_tasks) * 100 if total_tasks > 0 else 0

    return render(request, 'routine/dashboard.html', {
        'tasks': tasks,
        'pending_tasks': pending_tasks,
        'completed_tasks': completed_tasks,
        'progress_percentage': progress_percentage
    })

@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect back to the profile page
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'routine/edit_profile.html', {'form': form})


# Register view

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Save the user and hash the password
            user = form.save()

            # Check if the user already has a profile; if not, create one
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)

            login(request, user)  # Log the user in
            messages.success(request, "Registration successful!")
            return redirect('profile')  # Redirect to the profile page after registration
    else:
        form = RegistrationForm()

    return render(request, 'routine/register.html', {'form': form})


# Login view
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            messages.success(request, "Login successful!")
            return redirect('dashboard')  # Redirect to profile page after successful login
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'routine/login.html', {'form': form})

# Profile view for logged-in user
@login_required
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)  # Get the user's profile
    return render(request, 'routine/profile.html', {'profile': profile})

# Class Routine Views
###
# def class_routine_list(request):
#     routines = ClassRoutine.objects.all()
#     return render(request, 'routine/class_routine_list.html', {'routines': routines})





def add_class_routine(request):
    if request.method == 'POST':
        form = ClassRoutineForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)  # Don't save to DB yet
            routine.user = request.user        # Assign the current logged-in user
            routine.save()                     # Now save to DB
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

# Exam Routine Views
# def exam_list(request):
#     exams = ExamRoutine.objects.order_by('exam_date', 'start_time')
#     return render(request, 'routine/exam_list.html', {'exams': exams})

def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            routine = form.save(commit=False)  # Don't save to DB yet
            routine.user = request.user        # Assign the current logged-in user
            routine.save() 
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

# # Note Views
# def my_notes_view(request):
#     notes = MyNote.objects.all().order_by('-created_at')

#     if request.method == 'POST':
#         form = MyNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('my_notes')
#     else:
#         form = MyNoteForm()

#     return render(request, 'routine/my_notes.html', {'form': form, 'notes': notes})



# def my_notes_view(request):
#     notes = MyNote.objects.filter(user=request.user).order_by('-created_at')  # Filter notes for the logged-in user

#     if request.method == 'POST':
#         form = MyNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = request.user  # Set the user explicitly
#             note.save()
#             return redirect('dashboard')
#     else:
#         form = MyNoteForm()

#     return render(request, 'routine/my_notes.html', {'form': form, 'notes': notes})

@login_required
def my_notes_view(request):
    notes = MyNote.objects.filter(user=request.user).order_by('-created_at')  # Filter notes for the logged-in user

    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Set the user explicitly
            note.save()
            return redirect('my_notes')  # Redirect after saving the note
    else:
        form = MyNoteForm()

    return render(request, 'routine/my_notes.html', {'form': form, 'notes': notes})



def edit_note(request, pk):
    note = get_object_or_404(MyNote, pk=pk)
    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('my_notes')
    else:
        form = MyNoteForm(instance=note)
    return render(request, 'routine/edit_note.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(MyNote, pk=pk)
    note.delete()
    return redirect('my_notes')



# def add_task(request):
#     if request.method == 'POST':
#         form = MyNoteForm(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = request.user  # Assign the logged-in user to the task
#             note.save()
#             return redirect('my_notes')  # Redirect to the list of notes
#     else:
#         form = MyNoteForm()

#     return render(request, 'routine/my_note_form.html', {'form': form})

def add_task(request):
    if request.method == 'POST':
        form = MyNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user  # Associate the logged-in user
            note.save()  # Save the note
            return redirect('dashboard')  # Redirect to the dashboard after saving the task
        else:
            # Debugging: Add a message or log to check why the form isn't valid
            print(form.errors)  # This will print form validation errors to the console
    else:
        form = MyNoteForm()

    return render(request, 'routine/my_note_form.html', {'form': form})
