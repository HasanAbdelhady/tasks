from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task, Subtask, DailyProgress
from django.contrib import messages
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone

class HomeView(RedirectView):
    template_name = 'home.html'
    
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return '/admin-dashboard/'  # Use reverse_lazy in production
            return '/assignee-view/'
        return None
    
    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        if url:
            return redirect(url)
        return render(request, self.template_name)

class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin_dashboard.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def post(self, request, *args, **kwargs):
        if 'start_new_day' in request.POST:
            # Store yesterday's progress (if any) in DailyProgress
            yesterday = timezone.now().date() - timedelta(days=1)
            subtasks = Subtask.objects.filter(assignee__isnull=False)
            
            # Reset all subtask progress
            subtasks.update(completed=False)
            
            # Reset all task deadlines to today + their original duration
            for task in Task.objects.all():
                minutes_to_add = (task.id % 11 + 1) * 10  # Same logic as create_sample_tasks
                task.deadline = timezone.now() + timedelta(minutes=minutes_to_add)
                task.save()
            
            messages.success(request, 'تم بدء يوم جديد بنجاح')
            return redirect('admin_dashboard')
        return super().post(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        
        # Get current task data
        active_task = Task.objects.order_by('deadline').first()
        
        if not active_task:
            context['message'] = 'لا توجد مهام'
            return context
            
        # Get current progress
        subtasks = Subtask.objects.filter(task=active_task)
        assignees = {}
        
        for subtask in subtasks:
            if not subtask.assignee:
                continue
            username = subtask.assignee.username
            if username not in assignees:
                assignees[username] = []
            assignees[username].append(subtask.completed)
        
        # Get daily progress history
        daily_progress = DailyProgress.objects.all().order_by('-date')
        progress_by_date = {}
        
        for progress in daily_progress:
            date_str = progress.date.strftime('%Y-%m-%d')
            if date_str not in progress_by_date:
                progress_by_date[date_str] = []
            progress_by_date[date_str].append({
                'user': progress.assignee.username,
                'task': progress.task.name,
                'completed': progress.completed_subtasks,
                'total': progress.total_subtasks
            })
            
        context.update({
            'task': active_task,
            'assignees': assignees,
            'time_remaining': active_task.deadline - current_time,
            'is_expired': active_task.deadline <= current_time,
            'daily_progress': progress_by_date
        })
        return context

class AssigneeView(LoginRequiredMixin, TemplateView):
    template_name = 'assignee_view.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = now()
        
        # Get all active tasks
        active_tasks = Task.objects.filter(deadline__gt=current_time).order_by('deadline')
        
        # Get the user's current task (if any)
        user_subtasks = Subtask.objects.filter(assignee=self.request.user).first()
        current_task = user_subtasks.task if user_subtasks else None
        
        context.update({
            'available_tasks': active_tasks,
            'current_task': current_task,
            'subtasks': Subtask.objects.filter(task=current_task, assignee=self.request.user) if current_task else None
        })
        return context
    
    def post(self, request, *args, **kwargs):
        task_id = request.POST.get('task_id')
        
        if task_id == '':
            # User wants to unassign from current task
            Subtask.objects.filter(assignee=request.user).update(assignee=None, completed=False)
            return redirect('assignee_view')
            
        if task_id:
            # User is selecting a new task
            try:
                # First, unassign from any current tasks
                Subtask.objects.filter(assignee=request.user).update(assignee=None, completed=False)
                
                # Then assign to the new task
                new_task = Task.objects.get(id=task_id)
                subtasks = Subtask.objects.filter(task=new_task)
                for subtask in subtasks:
                    subtask.assignee = request.user
                    subtask.save()
            except Task.DoesNotExist:
                pass  # Handle invalid task_id gracefully
        else:
            # User is updating subtask status
            current_subtasks = Subtask.objects.filter(assignee=request.user)
            for subtask in current_subtasks:
                subtask.completed = str(subtask.id) in request.POST
                subtask.save()
                
        return redirect('assignee_view')

class AllUsersView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'all_users.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.all()
        task_data = []

        for task in tasks:
            subtasks = Subtask.objects.filter(task=task)
            assignee_data = {}

            for subtask in subtasks:
                # Skip unassigned subtasks
                if not subtask.assignee:
                    continue
                    
                username = subtask.assignee.username
                if username not in assignee_data:
                    assignee_data[username] = {'total': 0, 'completed': 0}
                assignee_data[username]['total'] += 1
                if subtask.completed:
                    assignee_data[username]['completed'] += 1

            if assignee_data:  # Only add tasks that have assigned users
                task_data.append({'task': task, 'assignees': assignee_data})

        # Add daily progress data
        daily_progress = DailyProgress.objects.all().order_by('-date')
        progress_by_date = {}
        
        for progress in daily_progress:
            date_str = progress.date.strftime('%Y-%m-%d')
            if date_str not in progress_by_date:
                progress_by_date[date_str] = []
            progress_by_date[date_str].append({
                'user': progress.assignee.username,
                'task': progress.task.name,
                'completed': progress.completed_subtasks,
                'total': progress.total_subtasks
            })

        context['tasks'] = task_data
        context['daily_progress'] = progress_by_date
        return context
