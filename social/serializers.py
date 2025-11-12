from rest_framework import serializers
from .models import (
    Profile,
)


class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "avatar",
            "bio"
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    posts = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "avatar",
            "bio",
            "posts",
            "followers_count",
            "following_count"
        )

    def get_posts(self, obj):
        posts = obj.user.posts.all()
        return PostListSerializer(posts, many=True).data

    def get_followers_count(self, obj):
        return obj.user.followers.count()

    def get_following_count(self, obj):
        return obj.user.followings.count()
