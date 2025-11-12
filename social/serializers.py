from rest_framework import serializers
from .models import (
    Profile,
    Hashtag,
    Post,
    Like,
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


class HashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hashtag
        fields = (
            "id",
            "text"
        )


class PostListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    hashtag = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="text"
    )
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "media",
            "content",
            "hashtag",
            "publishing_at",
            "likes_count"
        )

    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username"
    )
    post = serializers.StringRelatedField()

    class Meta:
        model = Like
        fields = (
            "id",
            "user",
            "post",
            "created_at"
        )
