from django.urls import path

from user.views import (
    MyProfileView,
    RegisterView,
    LoginView,
    LogoutView,
    UserListView,
    UserDetailView,
    GetFollowersView,
    GetFollowingView,
    FollowUserView,
    LikedPostListView,
)

urlpatterns = [
    path("me/", MyProfileView.as_view(), name="my-profile"),
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("logout/", LogoutView.as_view(), name="auth-logout"),
    path("", UserListView.as_view(), name="user-list"),
    path("<slug:username>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "<slug:username>/get-followers/",
        GetFollowersView.as_view(),
        name="get-followers",
    ),
    path(
        "<slug:username>/get-following/",
        GetFollowingView.as_view(),
        name="get-following",
    ),
    path("<slug:username>/follow/", FollowUserView.as_view(), name="follow-user"),
    path("me/liked-posts/", LikedPostListView.as_view(), name="liked-posts"),
]

app_name = "user"
