from django.urls import path, include
from rest_framework import routers

from post.views import PostViewSet, UserFeedView, LikeView, GetLikersView, AddCommentView, CommentDetailView, \
    LikeCommentView

router = routers.DefaultRouter()

router.register("", PostViewSet)

urlpatterns = [
    path("feed/", UserFeedView.as_view(), name="feed"),
    path("", include(router.urls)),
    path("like/<int:post_id>/", LikeView.as_view(), name="like"),
    path("<int:post_id>/get-likers/", GetLikersView.as_view(), name="get-likers"),
    path("comment/<int:post_id>/", AddCommentView.as_view(), name="add-comment"),
    path("comment/<int:post_id>/<int:id>/", CommentDetailView.as_view(), name="comment-detail"),
    path("comment/<int:post_id>/<int:comment_id>/like/", LikeCommentView.as_view(), name="comment-like"),

]

app_name = "post"
