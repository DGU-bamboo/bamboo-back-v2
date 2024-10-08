from django.db.models.signals import post_save
from django.dispatch import receiver
from core.utils.discord import send_to_discord
from django.conf import settings

from core.utils.insta_upload import upload_insta_post
from post.models import Post, Comment, MaintainerPost
from django.utils import timezone
from post.signals import send_discord_upload


@receiver(send_discord_upload)
def post_discord_sender(post, **kwargs):
    url = settings.DISCORD_WEBHOOK_URL_UPLOAD
    if post.type == "NEMO":
        admin_link = f"{settings.WEB_URL}/admin/post/maintainerpost/{post.id}/change/"
        web_link = f"{settings.FE_WEB_URL}/suggestion/{post.id}"
        message = f"""
                    > 🐠 **니모 제보**가 모여 [게시글]({web_link}) 업로드 완료!📋
                    > 인스타에 업로드 되었는지 확인해 주세요!
                    > 관리자 페이지🧑🏼‍💻 [바로가기]({admin_link})
                    """
        send_to_discord(url, message)
    elif post.type == "COMMON":
        admin_link = f"{settings.WEB_URL}/admin/post/maintainerpost/{post.id}/change/"
        web_link = f"{settings.FE_WEB_URL}/suggestion/{post.id}"
        message = f"""
                    > 💌 **일반 제보**로 [게시글]({web_link}) 업로드 완료!📋
                    > 인스타에 업로드 되었는지 확인해 주세요!
                    > 관리자 페이지🧑🏼‍💻 [바로가기]({admin_link})
                    """
        send_to_discord(url, message)


@receiver(post_save, sender=Post)
def add_id_hashtag_in_post(sender, instance, created, **kwargs):
    if created:
        hashtag = " #" + str(instance.id) + "번째뿌우"
        instance.content += hashtag
        instance.save(update_fields=["content"])
        send_discord_upload.send(sender="add id hashtag in post", post=instance)
        upload_insta_post(instance)
