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
