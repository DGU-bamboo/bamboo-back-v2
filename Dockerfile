FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

#RUN apt-get update && apt-get install -y \
#    wget \
#    unzip \
#    libglib2.0-0 \
#    libnss3 \
#    libgconf-2-4 \
#    libfontconfig1
#
## 특정 버전의 Chrome 설치
#RUN wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_114.0.5735.90-1_amd64.deb
#RUN dpkg -i google-chrome-stable_114.0.5735.90-1_amd64.deb; apt-get -fy install
#RUN mv /usr/bin/google-chrome-stable /usr/bin/google-chrome
#
## 특정 버전의 ChromeDriver 설치
#RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip
#RUN mv chromedriver /usr/bin/chromedriver
#RUN chown root:root /usr/bin/chromedriver
#RUN chmod +x /usr/bin/chromedriver
#
## ipv6 비활성화
#RUN echo 'net.ipv6.conf.all.disable_ipv6 = 1' > /etc/sysctl.d/disableipv6.conf

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]