from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.pagination import FollowerPagination
from user.permissions import AllowUnauthenticatedOnly
from user.serializers import (
    MyProfileSerializer,
    UserRegisterSerializer,
    CustomAuthTokenSerializer,
    UserListSerializer,
    UserDetailSerializer, FollowSerializer,
)


class MyProfileView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (AllowUnauthenticatedOnly,)
    serializer_class = UserRegisterSerializer


class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomAuthTokenSerializer
    permission_classes = (AllowUnauthenticatedOnly,)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Successfully logged out."})


class UserListView(generics.ListAPIView):
    queryset = get_user_model().objects.prefetch_related("followers", "following")
    serializer_class = UserListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ["username", "first_name", "last_name", "birth_date"]


class UserDetailView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.prefetch_related("followers", "following", "posts")
    serializer_class = UserDetailSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = "username"


class GetFollowersView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowerPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(
            username=username).followers.all()
        return queryset


class GetFollowingView(generics.ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = FollowerPagination
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = self.kwargs['username']
        queryset = get_user_model().objects.get(
            username=username).following.all()
        return queryset
