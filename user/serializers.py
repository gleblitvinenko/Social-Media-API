from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.paginator import Paginator
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext as _

from post.models import Post, Comment
from user.models import User


class MyProfileSerializer(serializers.ModelSerializer):
    # TODO Posts i like.

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
            "birth_date",
            "number_of_followers",
            "number_of_following"
        )
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password is not None:
            user.set_password(password)
            user.save()

        return user


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            "email",
            "password",
            "password2",
            "username",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        user.first_name = validated_data["first_name"]
        user.last_name = validated_data["last_name"]
        user.save()

        return user


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "number_of_followers",
            "number_of_following",
        )


class UserPostsSerializer(serializers.ModelSerializer):
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "image",
            "content",
            "number_of_likes",
            "number_of_comments",
            "created_at",
        )

    @staticmethod
    def get_number_of_comments(obj):
        return Comment.objects.filter(post=obj).count()


class UserDetailSerializer(serializers.ModelSerializer):
    number_of_posts = serializers.SerializerMethodField()
    user_posts = serializers.SerializerMethodField('paginated_user_posts')

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "profile_picture",
            "bio",
            "birth_date",
            "number_of_followers",
            "number_of_following",
            "number_of_posts",
            "user_posts"
        )

    @staticmethod
    def get_number_of_posts(obj):
        return Post.objects.filter(user=obj).count()

    def paginated_user_posts(self, obj):
        page_size = 1
        paginator = Paginator(obj.posts.all(), page_size)
        page = self.context['request'].query_params.get('page') or 1

        user_posts = paginator.page(page)
        serializer = UserPostsSerializer(user_posts, many=True)

        return serializer.data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "profile_picture")


class LikedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "created_at", "content", "image")
