from django.urls import path, include
from .views import PostViewSet, CommentViewSet
from rest_framework import routers

default_router = routers.SimpleRouter(trailing_slash=False)
default_router.register("posts", PostViewSet, basename="posts")


comment_router = routers.SimpleRouter(trailing_slash=False)
comment_router.register("comments", CommentViewSet, basename="comments")


urlpatterns = [
    path("", include(default_router.urls)),
    path("posts/<int:post_id>/", include(comment_router.urls)),
]
