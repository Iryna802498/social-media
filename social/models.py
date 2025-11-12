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
