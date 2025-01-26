from django.contrib import admin
from django.urls import path, include
from accounts.views import LoginOrSignupView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginOrSignupView.as_view(), name='login_or_signup'),
    path('accounts/', include('accounts.urls')),
    path('tasks/', include('tasks.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
