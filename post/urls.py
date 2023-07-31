from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, UserFeedView, LikeView, GetLikersView

router = routers.DefaultRouter()

router.register("", PostViewSet)

urlpatterns = [
    path("feed/", UserFeedView.as_view(), name="feed"),
    path("", include(router.urls)),
    path("like/<int:post_id>/", LikeView.as_view(), name="like"),
    path("<int:post_id>/get-likers/", GetLikersView.as_view(), name="get-likers"),
]

app_name = "post"
