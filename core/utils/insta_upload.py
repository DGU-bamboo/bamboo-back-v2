import os

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from core.utils.discord import send_to_discord
from core.utils.image_generator import thumbnail_generator, thumbnail_generator_v2, send_thumbnail_to_discord


def upload_insta_post(post):
    try:
        image_text, content = create_post_content(post)  # 이미지에 넣을 텍스트, 게시글 문구
        image_path = thumbnail_generator_v2(image_text, post)  # 이미지 만들어서 저장
        send_thumbnail_to_discord(image_path)  # 디스코드에 썸네일 전송
        # upload_with_selenium(image_path, content)  # 셀레니움으로 업로드
        # send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, "인스타 업로드 성공!")  # 성공하면 디코 알림
    except Exception as e:
        exception_message = "썸네일 생성 실패: " + str(e)
        send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, exception_message)
        # exception_message = "인스타 업로드 실패: " + str(e)
        # send_to_discord(settings.DISCORD_WEBHOOK_URL_UPLOAD, exception_message) # 실패하면 디코 알림
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


def upload_with_selenium(image_path, content):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537")
    chrome_options.add_argument('window-size=1920x1080')
    #Product용
    chrome_services = Service(executable_path='/usr/bin/chromedriver', log_path='chromedriver.log')
    driver = webdriver.Chrome(service=chrome_services, options=chrome_options)

    # #Local test용
    # driver = webdriver.Chrome(options=chrome_options)

    username = settings.INSTAGRAM_USERNAME
    password = settings.INSTAGRAM_PASSWORD

    # 로그인
    driver.get('https://www.instagram.com/accounts/login/')
    driver.implicitly_wait(25)
    driver.save_screenshot('login.png')
    # 유저네임 입력
    driver.find_element(By.NAME, 'username').send_keys(username)
    # 패스워드 입력
    driver.find_element(By.NAME, 'password').send_keys(password)
    # 로그인 버튼 클릭
    driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)
    driver.implicitly_wait(20)
    # 알림 설정 무시
    try:
        driver.find_element(By.CLASS_NAME, '_ac8f').click()
        driver.implicitly_wait(10)
    except:
        pass
    try:
        driver.find_element(By.CLASS_NAME, '_a9_1').click()
    except:
        pass
    driver.implicitly_wait(10)
    # 게시물 생성 클릭
    driver.find_element(By.XPATH, '//*[@aria-label="New post"]').click()
    driver.implicitly_wait(10)
    # 내 컴퓨터에서 열기
    driver.find_element(By.XPATH, '//*[@class="_acan _acap _acas _aj1-"]')
    # 파일 입력
    driver.find_element(By.CSS_SELECTOR, "input[type='file']").send_keys(image_path)
    # 다음1
    driver.find_element(By.XPATH, '//div[text()="Next"]').click()
    driver.implicitly_wait(10)
    # 다음2
    driver.find_element(By.XPATH, '//div[text()="Next"]').click()
    driver.implicitly_wait(10)
    # 게시글 입력
    div_content = driver.find_element(By.XPATH, '//div[@aria-label="Write a caption..."]')
    div_content.send_keys(content)
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH, '//div[text()="Share"]').click()
    driver.implicitly_wait(10)
    driver.quit()

    return True
