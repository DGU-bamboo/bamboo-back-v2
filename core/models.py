from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def delete(self, force=False, *args, **kwargs):
        if force:
            return super().delete(*args, **kwargs)
        else:
            self.deleted_at = timezone.now()
            return self.save(update_fields=["deleted_at"])

    def restore(self):
        self.deleted_at = None
        return self.save(update_fields=["deleted_at"])

    class Meta:
        abstract = True
