from rest_framework import viewsets, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from post.models import Post
from post.permissions import IsOwnerOrReadOnly
from post.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("user").prefetch_related(
        "post_comments"
    )  # TODO FULL FIX N+1 PROBLEM
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (TokenAuthentication,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFeedView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        queryset = Post.objects.select_related("user").filter(user__in=following_users)  # TODO FULL FIX N+1 PROBLEM
        return queryset
