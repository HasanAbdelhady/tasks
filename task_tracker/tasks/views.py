from accounts.models import UserProfile
from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Task, Subtask, DailyProgress


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
            yesterday = now().date() - timedelta(days=1)
            subtasks = Subtask.objects.filter(assignee__isnull=False)

            # Reset subtask completion status
            subtasks.update(completed=False)

            # Reset task deadlines
            for task in Task.objects.all():
                minutes_to_add = (task.id % 11 + 1) * 10
                task.deadline = now() + timedelta(minutes=minutes_to_add)
                task.save()

            # Archive daily progress
            for subtask in subtasks:
                progress, created = DailyProgress.objects.get_or_create(
                    date=yesterday,
                    task=subtask.task,
                    assignee=subtask.assignee,
                    defaults={
                        'completed_subtasks': 0,
                        'total_subtasks': 0,
                    }
                )
                progress.completed_subtasks = Subtask.objects.filter(
                    task=subtask.task, assignee=subtask.assignee, completed=True
                ).count()
                progress.total_subtasks = Subtask.objects.filter(
                    task=subtask.task, assignee=subtask.assignee
                ).count()
                progress.save()

            messages.success(request, 'تم بدء يوم جديد بنجاح.')
            return redirect('admin_dashboard')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = now()

        # Fetch the most urgent task
        active_task = Task.objects.order_by('deadline').first()
        if not active_task:
            context['message'] = 'لا توجد مهام'
            return context

        # Fetch subtasks and group them by assignees
        subtasks = Subtask.objects.filter(
            task=active_task, assignee__is_superuser=False
        )
        assignees = {}
        for subtask in subtasks:
            if subtask.assignee:
                username = subtask.assignee.username
                if username not in assignees:
                    assignees[username] = []
                assignees[username].append({
                    'subtask': subtask.name,
                    'completed': subtask.completed
                })

        # Fetch user profiles and their assigned subtasks
        user_profiles = UserProfile.objects.select_related(
            'user', 'subtask'
        ).all()
        profiles_data = [
            {
                'username': profile.user.username,
                'rank': profile.rank,
                'subtask': profile.subtask.name if profile.subtask else None,
                'task': profile.subtask.task.name if profile.subtask else None,
                'completed': profile.subtask.completed if profile.subtask else False,
            }
            for profile in user_profiles
        ]

        # Fetch daily progress history
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

        # Update the context
        context.update({
            'task': active_task,
            'assignees': assignees,
            'user_profiles': profiles_data,
            'time_remaining': active_task.deadline - current_time,
            'is_expired': active_task.deadline <= current_time,
            'daily_progress': progress_by_date,
        })
        return context


class AssigneeView(LoginRequiredMixin, TemplateView):
    template_name = 'assignee_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch all subtasks assigned to the current user
        subtasks = Subtask.objects.filter(assignee=self.request.user)

        context.update({
            'subtasks': subtasks,
        })
        return context

    def post(self, request, *args, **kwargs):
        # Handle subtask completion
        for subtask in Subtask.objects.filter(assignee=request.user):
            subtask.completed = str(subtask.id) in request.POST
            subtask.save()

        messages.success(request, "تم تحديث حالة المهام بنجاح.")
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
            subtasks = Subtask.objects.filter(
                task=task, assignee__is_superuser=False
            )
            assignee_data = {}

            for subtask in subtasks:
                if not subtask.assignee:
                    continue

                username = subtask.assignee.username
                if username not in assignee_data:
                    assignee_data[username] = {'total': 0, 'completed': 0}
                assignee_data[username]['total'] += 1
                if subtask.completed:
                    assignee_data[username]['completed'] += 1

            if assignee_data:
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

        context.update({
            'tasks': task_data,
            'daily_progress': progress_by_date,
        })
        return context
