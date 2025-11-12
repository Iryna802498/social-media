from django.urls import path, include
from rest_framework import routers
from .views import (
    ProfileViewSet,
    PostViewSet,
    LikeViewSet,
    CommentViewSet,
    FollowViewSet
)


router = routers.DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profile")
router.register("posts", PostViewSet, basename="post")
router.register("likes", LikeViewSet, basename="like")
router.register("comments", CommentViewSet, basename="comment")
router.register("follow", FollowViewSet, basename="follow")
urlpatterns = [
    path("", include(router.urls)),
]


app_name = "social"
