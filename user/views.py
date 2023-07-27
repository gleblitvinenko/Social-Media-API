from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from user.models import User
from user.permissions import AllowUnauthenticatedOnly
from user.serializers import MyProfileSerializer, UserRegisterSerializer, CustomAuthTokenSerializer


class MyProfileView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowUnauthenticatedOnly, )
    serializer_class = UserRegisterSerializer


class LoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = CustomAuthTokenSerializer
    permission_classes = (AllowUnauthenticatedOnly,)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Successfully logged out."})
