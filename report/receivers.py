from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from core.utils.discord import send_to_discord
from report.models import Report, MaintainerNemoReport, MaintainerCommonReport
from django.conf import settings
from post.models import Post
from django.utils import timezone


@receiver(post_save, sender=Report)
@receiver(post_save, sender=MaintainerCommonReport)
@receiver(post_save, sender=MaintainerNemoReport)
def suggestion_discord_sender(sender, instance, created, **kwargs):
    if created:
        reject_url = f"{settings.API_URL}/reports/{instance.id}/reject"
        if instance.type == "NEMO":
            admin_link = f"{settings.WEB_URL}/admin/report/maintainernemoreport/{instance.id}/change/"
            url = settings.DISCORD_WEBHOOK_URL_NEMO
            message = f"""
                        > 🐟 두근세근! **[니모 한 마리]({admin_link})**가 도착했어요!
                        > 제보 내용 : {instance.content}
                        > [거절하기]({reject_url})
                        """

            send_to_discord(url, message)
        elif instance.type == "COMMON":
            admin_link = f"{settings.WEB_URL}/admin/report/maintainercommonreport/{instance.id}/change/"
            url = settings.DISCORD_WEBHOOK_URL_COMMON
            message = f"""
                        > 🙉 임금님 귀는 당나귀 귀! **[일반 제보]({admin_link})**가 도착했어요!
                        > 제보 내용 : {instance.content[:50]}
                        > [거절하기]({reject_url})
                        """
            send_to_discord(url, message)


@receiver(pre_save, sender=Report)
@receiver(pre_save, sender=MaintainerCommonReport)
def common_approve_to_post(sender, instance, **kwargs):
    if instance.type == "COMMON":
        try:
            old_instance = Report.objects.get(pk=instance.pk)
        except Report.DoesNotExist:
            return
        if old_instance.is_approved != True and instance.is_approved == True:
            post = Post.objects.create(
                title=instance.filtered_content[:30],
                content=instance.postify + "\n\n#동국대학교대나무숲 #동대나무숲",
                type="COMMON",
            )
            instance.post = post


@receiver(pre_save, sender=Report)
@receiver(pre_save, sender=MaintainerCommonReport)
@receiver(pre_save, sender=MaintainerNemoReport)
def edit_post_after_report_deleted(sender, instance, **kwargs):
    try:
        old_instance = Report.objects.get(pk=instance.pk)
    except Report.DoesNotExist:
        return
    if old_instance.deleted_at == None and instance.deleted_at:
        find_content = old_instance.postify
        instance.post.content = instance.post.content.replace(
            find_content, instance.postify
        )
        if instance.type == "COMMON":
            instance.post.deleted_at = timezone.now()
        instance.post.save(update_fields=["content", "deleted_at"])
