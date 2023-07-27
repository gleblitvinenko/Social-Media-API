from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.models import User
from user.permissions import AllowUnauthenticatedOnly
from user.serializers import MyProfileSerializer, UserRegisterSerializer


class MyProfileView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowUnauthenticatedOnly, )
    serializer_class = UserRegisterSerializer
