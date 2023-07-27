from django.urls import path

from user.views import MyProfileView, RegisterView

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("register/", RegisterView.as_view(), name="auth-register"),
]

app_name = "user"
