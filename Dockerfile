#FROM python:3.8
#
#WORKDIR /app
#
#COPY . .
#
#RUN pip install -r requirements.txt
#
#RUN python3 manage.py collectstatic --noinput
#
#CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]

FROM python:3.8

# Install prerequisites
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4

# Install Chrome
RUN wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install \
    && rm -f google-chrome-stable_current_amd64.deb

# Install Chrome Driver
RUN wget -N https://chromedriver.storage.googleapis.com/92.0.4515.43/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin \
    && chmod +x /usr/local/bin/chromedriver

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]
