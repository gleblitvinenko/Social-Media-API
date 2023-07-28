from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="posts", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    image = models.URLField()

    def __str__(self):
        return f"{self.content[:10]} posted by {self.user.username} at {self.created_at}"


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_comments", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_comments", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.content[:10]} added by {self.user.username} at {self.created_at}"


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_post_likes", on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post, related_name="post_post_likes", on_delete=models.CASCADE
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post: {self.post.content[:10]} was liked by {self.user.username} at {self.liked_at}"


class CommentLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="user_comment_likes", on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        Comment, related_name="comment_comment_likes", on_delete=models.CASCADE
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment: {self.comment.content[:10]} was liked by {self.user.username} at {self.liked_at}"
