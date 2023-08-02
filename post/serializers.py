from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from rest_framework import serializers

from post.models import Comment, Post, PostLike, CommentLike


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "profile_picture")


class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "user", "content", "created_at", "number_of_likes")
        read_only_fields = ("user", "id", "posted_on", "number_of_likes")

    @staticmethod
    def get_number_of_likes(obj):
        return CommentLike.objects.filter(comment=obj).count()


class PostSerializer(serializers.ModelSerializer):
    user = AuthorSerializer(read_only=True)
    number_of_comments = serializers.SerializerMethodField()
    post_comments = serializers.SerializerMethodField("paginated_post_comments")
    number_of_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "image",
            "content",
            "created_at",
            "number_of_comments",
            "post_comments",
            "number_of_likes",
        )

    @staticmethod
    def get_number_of_comments(obj):
        return Comment.objects.filter(post=obj).count()

    @staticmethod
    def get_number_of_likes(obj):
        return PostLike.objects.filter(post=obj).count()

    def paginated_post_comments(self, obj):
        page_size = 2
        paginator = Paginator(obj.post_comments.all(), page_size)
        page = self.context["request"].query_params.get("page") or 1

        post_comments = paginator.page(page)
        serializer = CommentSerializer(post_comments, many=True)

        return serializer.data


class GetLikerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    profile_picture = serializers.URLField(source="user.profile_picture")

    class Meta:
        model = PostLike
        fields = ("username", "profile_picture")
