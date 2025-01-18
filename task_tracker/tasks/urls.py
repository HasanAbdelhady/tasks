from django.urls import path
from .views import HomeView, AdminDashboardView, AssigneeView, AllUsersView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin_dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('assignee_view/', AssigneeView.as_view(), name='assignee_view'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
]
