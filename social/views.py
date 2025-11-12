from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .permissions import IsOwner
from .models import (
    Profile,
    Post,
    Like,
    Comment,
    Follow
)
from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    PostListSerializer,
    PostDetailSerializer,
    LikeSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
    FollowSerializer,
    FollowerSerializer,
    FollowingSerializer
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileListSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        username = self.request.query_params.get(
            "username"
        )
        queryset = self.queryset
        if username:
            queryset = queryset.filter(
                user__username__icontains=username
            )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description=(
                    "Filter by username "
                    "(ex. ?username='@test_user')"),
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        if self.action in ["follow", "unfollow"]:
            return FollowSerializer
        if self.action == "my_followers":
            return FollowerSerializer
        if self.action == "my_followings":
            return FollowingSerializer
        return ProfileDetailSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow",
        permission_classes=[IsAuthenticated]
    )
    def follow(self, request, pk=None):
        user_to_follow = self.get_object().user
        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        _, created = Follow.objects.get_or_create(
            follower=request.user, following=user_to_follow
        )
        if not created:
            return Response(
                {"detail": "You already following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Successfully followed the user."},
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["POST"],
        detail=True,
        url_path="unfollow",
        permission_classes=[IsAuthenticated]
    )
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object().user

        deleted_count, _ = Follow.objects.filter(
            follower=request.user, following=user_to_unfollow
        ).delete()
        if deleted_count == 0:
            return Response(
                {"detail": "You don't following this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"detail": "Successfully unfollowed the user."},
        )

    @action(
        methods=["GET"],
        detail=False,
        url_path="my-followers",
        permission_classes=[IsAuthenticated]
    )
    def my_followers(self, request):
        queryset = Follow.objects.filter(following=request.user)
        serializer = FollowerSerializer(
            queryset, many=True
        )
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="my-followings",
        permission_classes=[IsAuthenticated]
    )
    def my_followings(self, request):
        queryset = Follow.objects.filter(follower=request.user)
        serializer = FollowingSerializer(
            queryset, many=True
        )
        return Response(serializer.data)
