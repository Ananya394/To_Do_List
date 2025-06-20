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
from .forms import ActivityForm, ChecklistItemForm,ActivityQuickForm
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
        return "orange"
    else:
        return "red"

@login_required
def activity_list(request):
    activities = Activity.objects.filter(user=request.user).order_by('date')
    today = date.today()

    for activity in activities:
        activity.is_completed = activity.completed
        if activity.date:
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

        activity.days_left = (activity.date - today).days

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

            if not activity.tags.strip():
             activity.tags = "#general"
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
    referer = request.POST.get('referer') or request.META.get('HTTP_REFERER') or '/'

    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect(referer)
    else:
        form = ActivityForm(instance=activity)
    return render(request, 'routine/activity_form.html', {'form': form, 'referer': referer})
    

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

# def activity_complete(request, pk):
#     activity = get_object_or_404(Activity, pk=pk, user=request.user)
#     activity.status = 'C'
#     activity.save()
#     return redirect('activity_list')




from django.shortcuts import render, redirect, get_object_or_404
from .models import Activity
from .forms import ActivityForm
from datetime import date, timedelta
@login_required
def activity_board(request):
    today = date.today()
    next_week = today + timedelta(days=7)

    activities = Activity.objects.filter(user=request.user)  # filter by user

    category = {
        'today': [],
        'next_week': [],
        'later': [],
        'no_date': [],
    }

    for activity in activities:
        if activity.completed:
            continue
        if not activity.date:
            category['no_date'].append(activity)
        elif activity.date == today:
            category['today'].append(activity)
        elif activity.date <= next_week:
            category['next_week'].append(activity)
        else:
            category['later'].append(activity)

    form = ActivityQuickForm()
    return render(request, 'routine/activity_board.html', {'columns': category, 'form': form})


@login_required
def add_activity(request, category):
    if request.method == 'POST':
        form = ActivityQuickForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            if category == 'today':
                activity.date = date.today()
            elif category == 'next_week':
                activity.date = date.today() + timedelta(days=3)
            elif category == 'later':
                activity.date = date.today() + timedelta(days=10)
            else:
                activity.date = None       

            if not activity.tags.strip():
                activity.tags = "#general"    
            activity.user = request.user  # always assign user
            activity.save()
    return redirect('activity_board')


@login_required
def complete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)  # ensure user owns it
    activity.completed = True
    activity.save()
    return redirect(request.META.get('HTTP_REFERER', 'activity_board'))


# @login_required
# def edit_activity(request, pk):
#     activity = get_object_or_404(Activity, pk=pk, user=request.user)  # ensure user owns it
#     if request.method == 'POST':
#         form = ActivityQuickForm(request.POST, instance=activity)
#         if form.is_valid():
#             form.save()
#             return redirect('activity_board')
#     else:
#         form = ActivityForm(instance=activity)
#     return render(request, 'edit_activity.html', {'form': form})


from datetime import timedelta
from collections import defaultdict
from django.utils import timezone

@login_required
    # filter_range = request.GET.get('filter', 'all')
    # now = timezone.now().date()

    # if filter_range == 'weekly':
    #     start_date = now - timedelta(days=7)
    # elif filter_range == 'monthly':
    #     start_date = now - timedelta(days=30)
    # else:
    #     start_date = None  # All time

    # activities = Activity.objects.filter(user=request.user)
    # if start_date:
    #     activities = activities.filter(date__gte=start_date)

    # tag_stats = defaultdict(lambda: {'total': 0, 'completed': 0})

    # for activity in activities:
    #     tags = activity.tags.split()
    #     for tag in tags:
    #         tag_stats[tag]['total'] += 1
    #         if activity.completed:
    #             tag_stats[tag]['completed'] += 1
    #         if activity.status=='C':
    #             tag_stats[tag]['completed'] += 1

    # review_data = []
    # for tag, data in tag_stats.items():
    #     percent = (data['completed'] / data['total']) * 100 if data['total'] else 0
    #     review_data.append({
    #         'tag': tag,
    #         'completed': data['completed'],
    #         'total': data['total'],
    #         'percent': round(percent, 1),
    #     })

    # return render(request, 'routine/activity_review.html', {
    #     'review_data': review_data,
    #     'filter_range': filter_range
    # })@login_required
def combined_review_summary(request):
    filter_range = request.GET.get('filter', 'all')
    now = timezone.now().date()

    if filter_range == 'weekly':
        start_date = now - timedelta(days=7)
    elif filter_range == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    activities = Activity.objects.filter(user=request.user)
    if start_date:
        activities = activities.filter(date__gte=start_date)

    # --- TAG REVIEW ---
    tag_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
    for activity in activities:
        tags = activity.tags.split()
        for tag in tags:
            tag_stats[tag]['total'] += 1
            if activity.completed:
                tag_stats[tag]['completed'] += 1
            # if activity.status=='C':
            #     tag_stats[tag]['completed'] += 1

    tag_summary = {}  # use this name in the template
    for tag, data in tag_stats.items():
        percent = (data['completed'] / data['total']) * 100 if data['total'] else 0
        tag_summary[tag] = {
            'completed': data['completed'],
            'total': data['total'],
            'percent': round(percent, 1),
        }

    # --- SUMMARY GROUPED BY DATE ---
    summary = defaultdict(list)
    for activity in activities.order_by('date'):
        summary[activity.date].append(activity)

    return render(request, 'routine/activity_review.html', {
        'filter_range': filter_range,
        'tag_summary': tag_summary,
        'summary': dict(summary),
    })
import json

@login_required
def efficiency_report(request):
    now = timezone.now().date()
    filter_range = request.GET.get('filter', 'all')

    if filter_range == 'weekly':
        start_date = now - timedelta(days=7)
    elif filter_range == 'monthly':
        start_date = now - timedelta(days=30)
    else:
        start_date = None

    activities = Activity.objects.filter(user=request.user)
    if start_date:
        activities = activities.filter(date__gte=start_date)

    tag_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
    for activity in activities:
        tags = activity.tags.split()
        for tag in tags:
            tag_stats[tag]['total'] += 1
            if activity.completed:
                tag_stats[tag]['completed'] += 1
            # if activity.status=='C':
            #     tag_stats[tag]['completed'] += 1

    labels = []
    percentages = []
    for tag, data in tag_stats.items():
        if data['total'] == 0:
            continue
        percent = round((data['completed'] / data['total']) * 100, 1)
        labels.append(tag)
        percentages.append(percent)

    context = {
        'labels': labels,
        'percentages': percentages,
        'filter_range': filter_range,
    }
    return render(request, 'routine/efficiency_report.html', context)
