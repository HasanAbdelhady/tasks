from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginOrSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginOrSignupView.as_view(), name='login_or_signup'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
]
