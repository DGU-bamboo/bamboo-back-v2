import os

import requests
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

from core.utils.discord import send_to_discord
from report.models import Report


def thumbnail_generator(image_text, post_type):
    if post_type == "NEMO":
        default_img = os.path.join(settings.BASE_DIR, 'core', 'utils', 'nemo.png')
    else:
        default_img = os.path.join(settings.BASE_DIR, 'core', 'utils', 'common.png')

    image = Image.open(default_img)

    image_width, image_height = image.size
    # draw 객체 생성
    draw = ImageDraw.Draw(image)
    # 폰트 설정
    font_path = os.path.join(settings.BASE_DIR, 'core', 'utils', 'JalnanOTF.otf')
    font = ImageFont.truetype(font_path, size=50)
    # 텍스트 위치 및 색상 설정
    _, _, text_width, text_height = draw.textbbox((0, 0), image_text, font=font)
    text_position = ((image_width - text_width) // 2, 388)
    text_color = "#04C96B"

    # 텍스트 그리기
    draw.text(text_position, image_text, fill=text_color, font=font)
    # 이미지 저장
    save_path = os.path.join(settings.MEDIA_ROOT, f'latest_thumbnail.png')
    # for debug
    send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, f"NEMO 이미지 저장 전, {save_path}")

    image.save(save_path)

    # for debug
    send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, f"NEMO 이미지 저장 후, {save_path}")
    # 절대 경로 반환
    absolute_path = os.path.abspath(save_path)
    return absolute_path


def thumbnail_generator_v2(image_text, post):
    if post.type == "NEMO":
        return thumbnail_generator(image_text, "NEMO")
    return common_thumbnail_with_text(image_text, post)


def common_thumbnail_with_text(image_text, post):
    overflow = False
    front = post.content.find("\n")
    rear = post.content.find("\n#동국대학교대나무숲")
    post_content = post.content[front + 1:rear]

    lines = []
    content_idx = 0
    while len(lines) < 8:
        if (idx := post_content[content_idx:content_idx + 12].find("\n")) != -1:
            lines.append(post_content[content_idx:content_idx + idx])
            content_idx += idx + 1
        else:
            lines.append(post_content[content_idx:content_idx + 12])
            content_idx += 12

    if lines[7] != "":
        overflow = True
        lines[6] = lines[6][:9] + "..."

    default_img = os.path.join(settings.BASE_DIR, 'core', 'utils', 'common.png')
    image = Image.open(default_img)
    image_width, image_height = image.size
    # draw 객체 생성
    draw = ImageDraw.Draw(image)
    # 폰트 설정 (폰트 파일에 따라 다르게 설정 가능)
    font_path = os.path.join(settings.BASE_DIR, 'core', 'utils', 'JalnanOTF.otf')
    main_font = ImageFont.truetype(font_path, size=60)
    overflow_font = ImageFont.truetype(font_path, size=45)
    text_color = "#04C96B"

    # 제보 ID 작성
    _, _, text_width, text_height = draw.textbbox((0, 0), image_text, font=main_font)
    text_position = ((image_width - text_width) // 2, 177)
    draw.text(text_position, image_text, fill=text_color, font=main_font)

    # 제보 내용 작성
    text_position = [126, 287]
    for i in range(7):
        draw.text(text_position, lines[i].lstrip(), fill=text_color, font=main_font)
        text_position[1] += 75

    # 본문에서 이어서 작성
    if overflow:
        draw.text((525, 831), "본문에서 이어서", fill="#76D8A9", font=overflow_font)

    # 이미지 저장
    save_path = os.path.join(settings.MEDIA_ROOT, f'latest_thumbnail.png')
    # for debug
    send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, f"COMMON 이미지 저장 전, {save_path}")

    image.save(save_path)

    # for debug
    send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, f"COMMON 이미지 저장 후, {save_path}")

    # 절대 경로 반환
    absolute_path = os.path.abspath(save_path)
    return absolute_path


def send_thumbnail_to_discord(image_path):
    with open(file=image_path, mode='rb') as f:
        files = {
            "file": ('created_thumbnail.png', f)
        }
        requests.post(settings.DISCORD_WEBHOOK_URL_UPLOAD, files=files)
