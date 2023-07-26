from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.models import User
from user.serializers import MyProfileSerializer


class MyProfileView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = MyProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
