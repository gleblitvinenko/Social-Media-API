from django.urls import path

from user.views import (
    MyProfileView,
    RegisterView,
    LoginView,
    LogoutView,
    UserListView,
    UserDetailView,
)

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]

app_name = "user"
