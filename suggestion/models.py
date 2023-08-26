from django.db import models
from core.models import BaseModel


class Suggestion(BaseModel):
    content = models.TextField(default="")
    contact = models.EmailField(blank=True, null=True)
    memo = models.TextField(blank=True, default="")


class MaintainerSuggestion(Suggestion):
    class Meta:
        proxy = True
        verbose_name = "건의사항 (관리자용)"
        verbose_name_plural = "건의사항들 (관리자용)"
