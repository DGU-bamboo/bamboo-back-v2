import os

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from core.utils.discord import send_to_discord


def upload_insta_post(post):
    try:
        image_text, content = create_post_content(post)  # 이미지에 넣을 텍스트, 게시글 문구
        image_path = thumbnail_generator(image_text, post.type)  # 이미지 만들어서 저장
        upload_with_selenium(image_path, content)  # 셀레니움으로 업로드
        send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, "인스타 업로드 성공!")  # 성공하면 디코 알림
    except Exception as e:
        exception_message = "인스타 업로드 실패: " + str(e)
        send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, exception_message) # 실패하면 디코 알림
    return True


def create_post_content(post):
    if post.type == "NEMO":
        image_text = post.title.split("시")[0]
        content = "⠀\n" + post.content + f" #{post.id}번째뿌우"
        return image_text, content
    elif post.type == "COMMON":
        image_text = f"#{post.id}번째 뿌우"
        content = "⠀\n" + post.content + f" #{post.id}번째뿌우"
        return image_text, content

    raise Exception(f"게시글 내용 생성 실패 - NEMO, COMMON에 해당하는 타입이 없습니다. 현재 타입: {post.type}")


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
    image.save(save_path)

    # 절대 경로 반환
    absolute_path = os.path.abspath(save_path)
    return absolute_path


def upload_with_selenium(image_path, content):
    service = Service("/root/.cache/selenium/chromedriver/linux64/116.0.5845.96/chromedriver")
    service.log_path = 'chromedriver.log'
    service.enable_tracing = True

    options = webdriver.ChromeOptions(executable_path='/usr/bin/chromedriver')
    options.add_argument('--headless')  # 헤드리스 모드
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    username = settings.INSTAGRAM_USERNAME
    password = settings.INSTAGRAM_PASSWORD

    # 로그인
    driver.get('https://www.instagram.com/accounts/login/')
    time.sleep(5)
    # 유저네임 입력
    driver.find_element(By.NAME, 'username').send_keys(username)
    # 패스워드 입력
    driver.find_element(By.NAME, 'password').send_keys(password)
    # 로그인 버튼 클릭
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    time.sleep(5)
    # 알림 설정 무시
    try:
        driver.find_element(By.CLASS_NAME, '_ac8f').click()
        time.sleep(3)
    except:
        pass
    try:
        driver.find_element(By.CLASS_NAME, '_a9_1').click()
    except:
        pass
    time.sleep(2)
    # 게시물 생성 클릭
    driver.find_element(By.XPATH, '//*[@aria-label="New post"]').click()
    # 내 컴퓨터에서 열기
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@class="_acan _acap _acas _aj1-"]')
    # 파일 입력
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(image_path)
    # 다음1
    driver.find_element(By.XPATH, '//div[text()="Next"]').click()
    time.sleep(2)
    # 다음2
    driver.find_element(By.XPATH, '//div[text()="Next"]').click()

    time.sleep(2)
    div_content = driver.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]')
    div_content.send_keys(content)
    time.sleep(5)
    driver.find_element(By.XPATH, '//div[text()="Share"]').click()
    time.sleep(5)
    driver.quit()

    return True
