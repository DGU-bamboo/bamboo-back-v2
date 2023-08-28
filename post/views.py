from rest_framework import viewsets, mixins

from .models import *
from .serializers import *
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import filters
from django.shortcuts import get_object_or_404


class PostViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [filters.SearchFilter]
    search_fields = ["content"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        return Post.objects.annotate(report_cnt=Count("report")).order_by("-id")


class CommentViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    def get_serializer_class(self):
        if self.action == "create":
            return CommentSerializer
        return CommentListSerializer

    def get_queryset(self):
        post = self.kwargs.get("post_id")
        queryset = Comment.objects.filter(post=post).order_by("created_at")
        return queryset

    def create(self, request, post_id=None):
        post = get_object_or_404(Post, id=post_id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post)
        return Response(serializer.data)
