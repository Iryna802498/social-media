from django.contrib import admin
from .models import (
    Profile,
    Post,
    Hashtag,
    Like,
    Comment,
    Follow
)


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Hashtag)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
