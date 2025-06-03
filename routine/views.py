from django.shortcuts import render, redirect, get_object_or_404
from .models import ClassRoutine, MyNote, ExamRoutine
from .forms import ClassRoutineForm, MyNoteForm,ExamForm
from django.http import JsonResponse

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


<<<<<<< Updated upstream
=======

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




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Activity, ChecklistItem
from .forms import ActivityForm, ChecklistItemForm
from django.utils import timezone

# List of all user activities
from datetime import date

from datetime import date

def get_urgency_color(days_left):
    if days_left >= 7:
        return "green"
    elif days_left >= 4:
        return "yellow"
    elif days_left >= 0:
        return "red"

@login_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user).order_by('date')
    today = date.today()

    for activity in activities:
        activity.is_completed = activity.status == "C"
        days_left = (activity.date - today).days

        # For width (how much of the row should be filled)
        if days_left >= 7:
            activity.urgency_width = 0
        elif days_left <= 0:
            activity.urgency_width = 100
        else:
            activity.urgency_width = int(((7 - days_left) / 7) * 100)

        # For color (how critical it is)
        activity.urgency_color = get_urgency_color(days_left)

        if days_left < 0:
            activity.days_left_text = f"{abs(days_left)} day(s) overdue"
        elif days_left == 0:
            activity.days_left_text = "Due today"
        else:
            activity.days_left_text = f"{days_left} day(s) left"

    return render(request, 'routine/activity_list.html', {
        'activities': activities,
    })


# Add a new activity
@login_required
def activity_create(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('activity_list')
    else:
        form = ActivityForm()
    return render(request, 'routine/activity_form.html', {'form': form})

# Edit an existing activity
@login_required
def activity_edit(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_list')
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'routine/activity_form.html', {'form': form})

# Delete an activity
@login_required
def activity_delete(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    activity.delete()
    return redirect('activity_list')

# Checklist: Add item
@login_required
def checklist_add(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, user=request.user)
    if request.method == 'POST':
        form = ChecklistItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.activity = activity
            item.save()
            return redirect('activity_list')
    else:
        form = ChecklistItemForm()
    return render(request, 'routine/checklist_form.html', {'form': form, 'activity': activity})

def activity_complete(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)
    activity.status = 'C'
    activity.save()
    return redirect('activity_list')
>>>>>>> Stashed changes
