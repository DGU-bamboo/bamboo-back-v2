FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1

# 특정 버전의 Chrome 설치
RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_91.0.4472.101-1_amd64.deb \
    && dpkg -i google-chrome-stable_91.0.4472.101-1_amd64.deb; apt-get -fy install

# 특정 버전의 ChromeDriver 설치
RUN wget https://chromedriver.storage.googleapis.com/91.0.4472.19/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && chown root:root /usr/bin/chromedriver \
    && chmod +x /usr/bin/chromedriver

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]