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
        if instance.type == "COMMON":
            if instance.deleted_at:
                return "작성자의 요청에 의해 삭제된 게시글입니다."
            return instance.content[:20]
        elif instance.type == "NEMO":
            return instance.created_at.strftime("%Y-%m-%d %p %I시 %M분") + " 니모"

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
        return "#" + str(instance.id) + "번째 뿌우"

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
    password = serializers.CharField(write_only=True)

    def get_is_deleted(self, instance):
        if instance.deleted_at:
            return True
        return False

    class Meta:
        model = Comment
        fields = ["id", "content", "is_deleted", "created_at", "password"]
        read_only_fields = ["post", "is_deleted"]


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
