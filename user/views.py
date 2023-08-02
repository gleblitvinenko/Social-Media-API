from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from post.models import Post
from user.pagination import FollowerPagination
from user.permissions import AllowUnauthenticatedOnly
from user.serializers import (
    MyProfileSerializer,
    UserRegisterSerializer,
    CustomAuthTokenSerializer,
    UserListSerializer,
    UserDetailSerializer,
    FollowSerializer,
    LikedPostSerializer,
)


@extend_schema(
    description="This endpoint gives user opportunity to manage his/her profile"
)
class MyProfileView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user


@extend_schema(
    description="This endpoint gives user opportunity to sign up for the platform"
)
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowUnauthenticatedOnly,)
    serializer_class = UserRegisterSerializer


@extend_schema(
    description="This endpoint gives user opportunity to login for the platform"
)
class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomAuthTokenSerializer
    permission_classes = (AllowUnauthenticatedOnly,)


@extend_schema(
    description="This endpoint gives user opportunity to logout for the platform"
)
class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Successfully logged out."})


@extend_schema(
    description="This endpoint gives user opportunity check all profiles on the platform"
                " and search profiles by username, first_name, last_name, birth_date"
)
class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.prefetch_related("followers", "following")
    serializer_class = UserListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ["username", "first_name", "last_name", "birth_date"]


@extend_schema(
    description="This endpoint gives user opportunity to check current profile details"
)
class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.prefetch_related(
        "followers", "following", "posts"
    )
    serializer_class = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "username"


@extend_schema(
    description="This endpoint gives user opportunity to see all followers current user has"
)
class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowerPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = get_user_model().objects.get(username=username).followers.all()
        return queryset


@extend_schema(
    description="This endpoint gives user opportunity to see all followings current user has"
)
class GetFollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowerPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.kwargs["username"]
        queryset = get_user_model().objects.get(username=username).following.all()
        return queryset


@extend_schema(
    description="This endpoint gives user opportunity to follow another user"
)
class FollowUserView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None, username=None):
        to_user = get_object_or_404(get_user_model(), username=username)
        from_user = request.user
        follow = None
        if from_user != to_user:
            if from_user in to_user.followers.all():
                follow = False
                from_user.following.remove(to_user)
                to_user.followers.remove(from_user)
            else:
                follow = True
                from_user.following.add(to_user)
                to_user.followers.add(from_user)
        from_user.save()
        to_user.save()

        data = {"follow": follow}
        return Response(data)


@extend_schema(
    description="This endpoint gives user opportunity to see posts he/she has liked"
)
class LikedPostListView(generics.ListAPIView):
    serializer_class = LikedPostSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        post_ids = user.user_post_likes.values_list("post_id", flat=True)
        queryset = Post.objects.filter(id__in=post_ids)
        return queryset
