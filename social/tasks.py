from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Post


@shared_task
def create_post(user_id: int, content: str):
    User = get_user_model()
    user = User.objects.get(id=user_id)
    Post.objects.create(user=user, content=content)