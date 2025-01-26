from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, RedirectView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from accounts.models import UserProfile
from tasks.models import Subtask, Task

# Rank choices
RANK_CHOICES = [
    ('Private', 'Private'),
    ('Corporal', 'Corporal'),
    ('Sergeant', 'Sergeant'),
    ('Staff Sergeant', 'Staff Sergeant'),
    ('Warrant Officer', 'Warrant Officer'),
    ('Second Lieutenant', 'Second Lieutenant'),
    ('First Lieutenant', 'First Lieutenant'),
    ('Captain', 'Captain'),
    ('Major', 'Major'),
    ('Lieutenant Colonel', 'Lieutenant Colonel'),
    ('Colonel', 'Colonel'),
    ('Brigadier General', 'Brigadier General'),
    ('Major General', 'Major General'),
    ('Lieutenant General', 'Lieutenant General'),
    ('General', 'General'),
]

# Mapping from rank to subtask index
RANK_TO_SUBTASK_INDEX = {
    'Private': 0,
    'Corporal': 1,
    'Sergeant': 2,
    'Staff Sergeant': 3,
    'Warrant Officer': 4,
    'Second Lieutenant': 5,
    'First Lieutenant': 6,
    'Captain': 7,
    'Major': 8,
    'Lieutenant Colonel': 9,
    'Colonel': 10,
    'Brigadier General': 11,
    'Major General': 12,
    'Lieutenant General': 13,
    'General': 14,
}


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(
        max_length=150,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg',
            'placeholder': 'Enter your full name',
        })
    )
    rank = forms.ChoiceField(
        choices=RANK_CHOICES,
        required=True,
        label="Rank",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border rounded-lg',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'rank', 'password1', 'password2']


class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the user
        user = form.save(commit=False)
        user.first_name = form.cleaned_data['name']  # Save name as first_name
        user.save()

        # Create UserProfile and assign subtask
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        # Assuming rank is part of the form
        user_profile.rank = form.cleaned_data['rank']
        user_profile.assign_subtask()  # Assign the subtask based on rank
        user_profile.save()

        # Assign tasks based on rank
        self.assign_tasks_to_user(user, user_profile.rank)

        # Log the user in
        login(self.request, user)

        return super().form_valid(form)

    def assign_tasks_to_user(self, user, rank):
        # Get the subtasks based on the user's rank
        index = RANK_TO_SUBTASK_INDEX.get(rank)
        if index is not None:
            subtasks = Subtask.objects.filter(
                task__isnull=False).order_by('task', 'id')
            if index < len(subtasks):
                # Assign the subtask to the user
                subtask = subtasks[index]
                subtask.assignee = user
                subtask.save()


class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('assignee_view')

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, error='Invalid credentials')
        )


class LoginOrSignupView(TemplateView):
    template_name = 'login_or_signup.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return redirect('admin_dashboard')
            return redirect('assignee_view')
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login_or_signup')


class AssigneeView(LoginRequiredMixin, TemplateView):
    template_name = 'assignee_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the user's assigned subtasks
        subtasks = Subtask.objects.filter(assignee=self.request.user)
        context['subtasks'] = subtasks

        # Get the user's rank
        user_profile = UserProfile.objects.get(user=self.request.user)
        context['rank'] = user_profile.rank if user_profile else "No Rank"

        return context

    def post(self, request, *args, **kwargs):
        # Handle completion confirmation
        for subtask_id in request.POST.getlist('subtask_ids'):
            subtask = Subtask.objects.get(id=subtask_id)
            if subtask.assignee == request.user:
                subtask.completed = True  # Mark as completed
                subtask.save()  # Save the change

        return redirect('assignee_view')


class AllUsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserProfile
    template_name = 'all_users.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profiles'] = UserProfile.objects.all()
        return context
