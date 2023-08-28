from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from report.models import Report
from report.serializers import ReportSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from post.models import Post
from rest_framework import views
from django.utils import timezone


class ReportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    @action(methods=["GET"], detail=True, permission_classes=[IsAdminUser])
    def reject(self, request, *args, **kwargs):
        report = self.get_object()
        report.is_approved = False
        report.save(update_fields=["is_approved"])
        return Response()

    @action(
        methods=["POST"],
        detail=False,
        url_path="nemo-force",
        permission_classes=[IsAdminUser],
    )
    def nemo_force(self, request, *args, **kwargs):
        queryset = Report.objects.filter(type="NEMO", is_approved=True, post=None)
        content = ""
        priority = 1
        if queryset.exists():
            for q in queryset:
                content += f"({priority})" + q.postify + "\n\n"
                priority += 1
            content += "#니모를찾아서 #동국대학교대나무숲 #동대나무숲"
            title = timezone.now().strftime("%Y-%m-%d %p %I시 %M분") + " 니모"
            post = Post.objects.create(title=title, content=content, type="NEMO")
            queryset.update(post=post)
        return Response()
