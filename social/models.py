import os
import uuid
from django.db import models
from social_media import settings


def user_profile_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    user_id = instance.user.id if hasattr(instance, "user") else instance.id
    filename = f"user-id-{user_id}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/users/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE
    )
    avatar = models.ImageField(
        blank=True,
        null=True,
        upload_to=user_profile_image_path
    )
    bio = models.TextField(
        blank=True,
        null=True
    )

    def __str__(self) -> str:
        return self.user.email


class Hashtag(models.Model):
    text = models.CharField(max_length=150, unique=True)

    def __str__(self) -> str:
        return self.text


def post_media_file_image_path(instance, filename):
    _, extension = os.path.splitext(filename)
    user_id = instance.user.id if hasattr(instance, "user") else instance.id
    filename = f"user-id-{user_id}-post-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/posts/", filename)


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE
    )
    media = models.ImageField(
        upload_to=post_media_file_image_path,
        blank=True,
        null=True
    )
    content = models.TextField()
    hashtag = models.ManyToManyField(
        Hashtag,
        related_name="posts",
        blank=True
    )
    publishing_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Post by {self.user.email}"

    class Meta:
        ordering = ["-publishing_at"]


class Like(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="likes",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "post"]

    def __str__(self) -> str:
        return f"Like by {self.user.email} to post {self.post.id}"
