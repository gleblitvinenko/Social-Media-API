from rest_framework import viewsets, generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, PostLike, Comment, CommentLike
from post.permissions import IsOwnerOrReadOnly
from post.serializers import PostSerializer, AuthorSerializer, GetLikerSerializer, CommentSerializer


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
        queryset = Post.objects.select_related("user").filter(
            user__in=following_users
        )  # TODO FULL FIX N+1 PROBLEM
        return queryset.prefetch_related(
        )


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Toggle like"""

    def post(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user

        try:
            like = PostLike.objects.get(user=user, post=post)
            like.delete()
            liked = False
        except PostLike.DoesNotExist:
            PostLike.objects.create(user=user, post=post)
            liked = True

        data = {
            'liked': liked
        }
        return Response(data, status=status.HTTP_200_OK)


class GetLikersView(generics.ListAPIView):
    serializer_class = GetLikerSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        queryset = PostLike.objects.filter(post_id=post_id)
        return queryset


class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, post_id=None):
        post = Post.objects.get(pk=post_id)
        serializer = CommentSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save(post=post, user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentDetailView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    lookup_field = "id"


class LikeCommentView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    """Toggle Comment like"""

    def post(self, request, format=None, comment_id=None, post_id=None):
        comment = Comment.objects.get(pk=comment_id)
        user = self.request.user

        try:
            like = CommentLike.objects.get(user=user, comment=comment)
            like.delete()
            liked = False
        except CommentLike.DoesNotExist:
            CommentLike.objects.create(user=user, comment=comment)
            liked = True

        data = {
            'liked': liked
        }
        return Response(data, status=status.HTTP_200_OK)


