from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    is_deleted = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    report_cnt = serializers.IntegerField()

    def get_is_deleted(self, instance):
        if instance.deleted_at:
            return True
        return False

    def get_title(self, instance):
        if instance.deleted_at:
            return "작성자의 요청에 의해 삭제된 게시글입니다."
        return instance.title

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "type",
            "is_deleted",
            "created_at",
            "report_cnt",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    is_deleted = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_is_deleted(self, instance):
        if instance.deleted_at:
            return True
        return False

    def get_title(self, instance):
        if instance.deleted_at:
            return "작성자의 요청에 의해 삭제된 게시글입니다."
        return instance.title

    def get_content(self, instance):
        if instance.deleted_at:
            return "작성자의 요청에 의해 삭제된 게시글입니다."
        return instance.content

    class Meta:
        model = Post
        fields = ["id", "title", "content", "type", "is_deleted", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    is_deleted = serializers.SerializerMethodField()
    content = serializers.CharField()

    def get_is_deleted(self, instance):
        if instance.deleted_at:
            return True
        return False

    class Meta:
        model = Comment
        fields = ["id", "content", "is_deleted", "created_at"]
        read_only_fields = ["post", "is_deleted"]
        write_only_fields = ["password"]


class CommentListSerializer(serializers.ModelSerializer):
    is_deleted = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_is_deleted(self, instance):
        if instance.deleted_at:
            return True
        return False

    def get_content(self, instance):
        if instance.deleted_at:
            return "< 작성자의 요청에 의해 삭제된 댓글입니다. >"
        return instance.content

    class Meta:
        model = Comment
        fields = ["id", "content", "is_deleted", "created_at"]
