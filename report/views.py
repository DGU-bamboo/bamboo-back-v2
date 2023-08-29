from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from report.models import Report
from report.serializers import ReportSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from post.models import Post
from rest_framework import views
from django.utils import timezone
from rest_framework import status


class ReportViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        response_data = {
            "success": True,
            "error": None,
        }

        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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
