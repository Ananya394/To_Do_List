from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegistrationForm, ClassRoutineForm, MyNoteForm, ExamForm,LoginForm
from .models import UserProfile, ClassRoutine, MyNote, ExamRoutine
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from collections import defaultdict
from django.utils import timezone
from .models import Activity, ChecklistItem
from .forms import ActivityForm, ChecklistItemForm,ActivityQuickForm
from datetime import date, timedelta
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test

#eti 
def home(request):
    login_form = LoginForm()
    register_form = RegistrationForm()
    return render(request, 'routine/home.html', {
        'login_form': login_form,
        'register_form': register_form
    })



def custom_login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('activity_board')  # or wherever
    else:
        form = LoginForm()
    return render(request, 'routine/login.html', {'form': form})



def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Fetch all activities and users
    activities = Activity.objects.all()
    users = UserProfile.objects.all()  # Assuming you have a UserProfile model for additional user details
    
    context = {
        'activities': activities,
        'users': users,
    }
    
    return render(request, 'routine/admin_dashboard.html', context)  # Corrected 'context' here

from django.shortcuts import render, redirect
from .models import Activity
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

@login_required
def dashboard(request):
    # Check if the user is an admin
    if is_admin(request.user):
        return redirect('admin_dashboard')  # Redirect admin to a separate admin dashboard

    today = date.today()
    next_week = today + timedelta(days=7)

    activities = Activity.objects.filter(user=request.user).order_by('date')
    pending_activities = activities.filter(status='P')
    completed_activities = activities.filter(status='C')

    # Calculate progress
    total_activities = activities.count()
    completed_count = completed_activities.count()
    progress_percentage = (completed_count / total_activities) * 100 if total_activities > 0 else 0

    # Categorize tasks
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

    # Handle quick task form submission
    if request.method == 'POST':
        form = ActivityQuickForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            # After adding the task, redirect to the same page
            return redirect('dashboard')  # Stay on the same page after task creation

    # Render the dashboard with the task list
    form = ActivityQuickForm()

    return render(request, 'routine/dashboard.html', {
        'columns': category,
        'form': form,
        'activities': activities,
        'pending_activities': pending_activities,
        'completed_activities': completed_activities,
        'progress_percentage': progress_percentage,
        'total_activities': total_activities,
        'completed_count': completed_count,
    })


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

# Dashboard view for both Admin and Student
# @login_required
# def dashboard(request):
#     # Check if the user is an admin
#     if is_admin(request.user):
#         return redirect('admin_dashboard')  # Redirect admin to a separate admin dashboard

#     # Get activities for student (user is not an admin)
#     activities = Activity.objects.filter(user=request.user).order_by('date')
#     pending_activities = activities.filter(status='P')
#     completed_activities = activities.filter(status='C')

#     # Calculate progress for student
#     total_activities = activities.count()
#     completed_count = completed_activities.count()
#     progress_percentage = (completed_count / total_activities) * 100 if total_activities > 0 else 0

#     # Render student dashboard with their activities
#     return render(request, 'routine/dashboard.html', {
#         'activities': activities,
#         'pending_activities': pending_activities,
#         'completed_activities': completed_activities,
#         'progress_percentage': progress_percentage,
#     })
    
#admin views 

def edit_user(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after saving
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'routine/edit_user.html', {'form': form, 'user': user})
from django.shortcuts import render, get_object_or_404
from .models import Activity, UserProfile

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Activity, UserProfile

@login_required
def user_task_details(request, pk):
    user_profile = get_object_or_404(UserProfile, pk=pk)
    tasks = Activity.objects.filter(user=user_profile.user)
    
    completed_tasks_list = tasks.filter(status='C')
    pending_tasks_list = tasks.filter(status='P')

    context = {
        'user': user_profile,
        'tasks': tasks,
        'completed_tasks_list': completed_tasks_list,
        'pending_tasks_list': pending_tasks_list,
        'total_tasks': tasks.count(),
        'completed_tasks': completed_tasks_list.count(),
        'pending_tasks': pending_tasks_list.count()
    }

    return render(request, 'routine/user_task_details.html', context)


def delete_user(request, pk):
    user = get_object_or_404(UserProfile, pk=pk)
    user.delete()  # Delete the user
    return redirect('admin_dashboard')  # Redirect to admin dashboard after deletion

def edit_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')  # Redirect to admin dashboard after saving
    else:
        form = ActivityForm(instance=activity)
    
    return render(request, 'routine/edit_activity.html', {'form': form, 'activity': activity})
                  
 
# def delete_activity(request, pk):
#     activity = get_object_or_404(Activity, pk=pk)
#     activity.delete()  # Delete the activity
#     return redirect('admin_dashboard')  # Redirect to admin dashboard after deletion
 
from django.shortcuts import get_object_or_404, redirect
from .models import Activity
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from .models import Activity

def delete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk)
    user_profile_pk = activity.user.userprofile.pk  # ✅ Get UserProfile PK

    activity.delete()

    return redirect('user_task_details', pk=user_profile_pk)

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
            user = form.save()
            if not UserProfile.objects.filter(user=user).exists():
                UserProfile.objects.create(user=user)
            login(request, user)  
            messages.success(request, "Registration successful!")
            return redirect('profile') 
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

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  

# Profile view for logged-in user
@login_required
def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)  # Get the user's profile
    return render(request, 'routine/profile.html', {'profile': profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # Update the session user to avoid the user being logged out
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('login')  # Redirect to login page after successful password change
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'routine/change_password.html', {'form': form})
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


@login_required
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





# List of all user activities



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
    today = date.today()
    priority_filter = request.GET.get('priority', '')
    date_filter = request.GET.get('date', '')

    activities = Activity.objects.filter(user=request.user).order_by('date')

    # Apply filters if given (priority and date)
    if priority_filter:
        activities = activities.filter(priority=priority_filter)
    if date_filter:
        activities = activities.filter(date=date_filter)

    pending = []
    overdue = []
    completed = []

    for activity in activities:
        activity.is_completed = activity.completed
        days_left = (activity.date - today).days if activity.date else None

        if days_left is not None:
            # Urgency width & color logic
            if days_left >= 7:
                activity.urgency_width = 0
            elif days_left <= 0:
                activity.urgency_width = 100
            else:
                activity.urgency_width = int(((7 - days_left) / 7) * 100)

            activity.urgency_color = get_urgency_color(days_left)

            if days_left < 0:
                activity.days_left_text = f"{abs(days_left)} day(s) overdue"
            elif days_left == 0:
                activity.days_left_text = "Due today"
            else:
                activity.days_left_text = f"{days_left} day(s) left"
        else:
            activity.urgency_width = 0
            activity.urgency_color = "green"
            activity.days_left_text = "No due date"

        activity.days_left = days_left

        if activity.completed:
            completed.append(activity)
        else:
            if days_left is not None and days_left < 0:
                overdue.append(activity)
            else:
                pending.append(activity)

    context = {
        'pending': pending,
        'overdue': overdue,
        'completed': completed,
        'priority_filter': priority_filter,
        'date_filter': date_filter,
    }

    return render(request, 'routine/activity_list.html', context)




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
    next_url = request.POST.get('next') or 'dashboard'  # fallback if 'next' not provided
    return redirect(next_url)


# @login_required
# def complete_activity(request, pk):
#     activity = get_object_or_404(Activity, pk=pk, user=request.user)  # ensure user owns it
#     activity.completed = True
#     activity.save()
#     activity.status = 'C'
#     #return redirect(request.META.get('HTTP_REFERER', 'activity_board'))
#     return redirect('dashboard')

@login_required
def complete_activity(request, pk):
    activity = get_object_or_404(Activity, pk=pk, user=request.user)  # Ensure user owns the activity
    
    # Update both the completed and status fields
    activity.completed = True
    activity.status = 'C'  # 'C' for Completed
    
    # Save the activity with the updated fields
    activity.save()

    # Redirect to the dashboard or a different page
    return redirect('dashboard')

@login_required
def complete_task(request, pk):
    task = get_object_or_404(MyNote, pk=pk, user=request.user)
    task.attended = True
    task.save()
    return redirect('dashboard')
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
@login_required
def delete_selected_activities(request):
    if request.method == 'POST':
        selected_activities = request.POST.getlist('selected_activities')
        Activity.objects.filter(id__in=selected_activities).delete()
        return redirect('dashboard')  # Redirect to the dashboard after deletion
    
@login_required
def delete_selected_completed_activities(request):
    if request.method == 'POST':
        selected_completed_activities = request.POST.getlist('selected_completed_activities')
        Activity.objects.filter(id__in=selected_completed_activities).delete()  # Bulk delete
        return redirect('dashboard')  # Redirect to dashboard after deletion    
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

# @login_required
# def efficiency_report(request):
#     now = timezone.now().date()
#     filter_range = request.GET.get('filter', 'all')

#     if filter_range == 'weekly':
#         start_date = now - timedelta(days=7)
#     elif filter_range == 'monthly':
#         start_date = now - timedelta(days=30)
#     else:
#         start_date = None

#     activities = Activity.objects.filter(user=request.user)
#     if start_date:
#         activities = activities.filter(date__gte=start_date)

#     tag_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
#     for activity in activities:
#         tags = activity.tags.split()
#         for tag in tags:
#             tag_stats[tag]['total'] += 1
#             if activity.completed:
#                 tag_stats[tag]['completed'] += 1
#             # if activity.status=='C':
#             #     tag_stats[tag]['completed'] += 1

#     labels = []
#     percentages = []
#     for tag, data in tag_stats.items():
#         if data['total'] == 0:
#             continue
#         percent = round((data['completed'] / data['total']) * 100, 1)
#         labels.append(tag)
#         percentages.append(percent)

#     context = {
#         'labels': labels,
#         'percentages': percentages,
#         'filter_range': filter_range,
#     }
#     return render(request, 'routine/efficiency_report.html', context)

def efficiency_report(request):
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]  # Last 7 days

    labels = [d.strftime("%b %d") for d in dates]
    efficiency = []

    user_activities = Activity.objects.filter(user=request.user)

    for d in dates:
        tasks = user_activities.filter(date=d)
        total = tasks.count()
        completed = tasks.filter(completed=True).count()
        percent = round((completed / total) * 100, 2) if total > 0 else 0
        efficiency.append(percent)

    # === TAG SUMMARY ===
    tag_stats = defaultdict(lambda: {'total': 0, 'completed': 0})
    tag_priority_stats = defaultdict(lambda: {
        'H': {'total': 0, 'completed': 0},
        'M': {'total': 0, 'completed': 0},
        'L': {'total': 0, 'completed': 0}
    })

    for activity in user_activities:
        tags = activity.tags.split()
        for tag in tags:
            tag_stats[tag]['total'] += 1
            if activity.completed:
                tag_stats[tag]['completed'] += 1

            # Track by priority
            priority = activity.priority
            tag_priority_stats[tag][priority]['total'] += 1
            if activity.completed:
                tag_priority_stats[tag][priority]['completed'] += 1

    # Clean tag summary
    tag_summary = {}
    for tag, data in tag_stats.items():
        percent = (data['completed'] / data['total']) * 100 if data['total'] else 0
        tag_summary[tag] = {
            'completed': data['completed'],
            'total': data['total'],
            'percent': round(percent, 1),
        }

    # Tag-based by priority
    tag_priority_summary = {}
    for tag, levels in tag_priority_stats.items():
        tag_priority_summary[tag] = {}
        for level in ['H', 'M', 'L']:
            total = levels[level]['total']
            completed = levels[level]['completed']
            percent = (completed / total) * 100 if total else 0
            tag_priority_summary[tag][level] = {
                'percent': round(percent, 1)
            }

    # Overall summary by priority
    priority_totals = {'H': {'completed': 0, 'total': 0},
                       'M': {'completed': 0, 'total': 0},
                       'L': {'completed': 0, 'total': 0}}

    for tag_data in tag_priority_stats.values():
        for level in ['H', 'M', 'L']:
            priority_totals[level]['completed'] += tag_data[level]['completed']
            priority_totals[level]['total'] += tag_data[level]['total']

    priority_efficiency = {}
    for level in ['H', 'M', 'L']:
        total = priority_totals[level]['total']
        completed = priority_totals[level]['completed']
        percent = (completed / total) * 100 if total else 0
        priority_efficiency[level] = round(percent, 1)

    # Final context
    context = {
        'labels': labels,
        'efficiency': efficiency,
        'tag_summary': dict(tag_summary),
        'tag_priority_summary': tag_priority_summary,
        'priority_efficiency': priority_efficiency,
    }

    return render(request, 'routine/efficiency_report.html', context)
