from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, UserFeedView, LikeView

router = routers.DefaultRouter()

router.register("", PostViewSet)

urlpatterns = [
    path("feed/", UserFeedView.as_view(), name="feed"),
    path("", include(router.urls)),
    path("like/<int:post_id>/", LikeView.as_view(), name="like"),
]

app_name = "post"
