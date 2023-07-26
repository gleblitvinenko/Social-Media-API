from django.contrib.auth import get_user_model
from rest_framework import serializers


class MyProfileSerializer(serializers.ModelSerializer):
    # TODO followers, followings, likes
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "password", "bio", "profile_picture", "birth_date")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
            user.save()

        return user
