from django.db import models
from core.models import BaseModel


class Notification(BaseModel):
    image = models.ImageField(blank=True, null=True, upload_to="notice/")
    url = models.URLField(max_length=2048, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=50)
    content = models.TextField()


class Modal(BaseModel):
    image = models.ImageField(blank=True, null=True, upload_to="modal/")
    url = models.URLField(max_length=2048, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)


class MaintainerNotification(Notification):
    class Meta:
        proxy = True
        verbose_name = "공지글 (관리자용)"
        verbose_name_plural = "공지글들 (관리자용)"


class MaintainerModal(Modal):
    class Meta:
        proxy = True
        verbose_name = "모달창 (관리자용)"
        verbose_name_plural = "모달창들 (관리자용)"
