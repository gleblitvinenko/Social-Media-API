from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, UserFeedView

router = routers.DefaultRouter()

router.register("", PostViewSet)

urlpatterns = [
    path("feed/", UserFeedView.as_view(), name="feed"),
    path("", include(router.urls)),
]

app_name = "post"
