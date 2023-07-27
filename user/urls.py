from django.urls import path

from user.views import MyProfileView, RegisterView, LoginView, LogoutView

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
]

app_name = "user"
