from django.urls import path
from .views import SignUpView, CustomLoginView, LoginOrSignupView, CustomLogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
