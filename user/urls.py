from django.urls import path

from user.views import MyProfileView

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
]

app_name = "user"
