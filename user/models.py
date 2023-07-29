from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if email is None:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=50, blank=True)
    email = models.EmailField(_("email address"), unique=True)
    profile_picture = models.URLField()
    bio = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_followers",
        blank=True,
        symmetrical=False  # one-way communication
    )
    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="user_following",
        blank=True,
        symmetrical=False  # one-way communication
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def number_of_followers(self):
        if self.followers.count():
            return self.followers.count()
        return 0

    def number_of_following(self):
        if self.following.count():
            return self.following.count()
        return 0



    def __str__(self):
        return self.username
