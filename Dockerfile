FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

# Install system dependencies
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        wget unzip \
        libxss1 libappindicator1 libindicator7 \
        libasound2 libnss3 libx11-xcb1 libxtst6 xdg-utils && \
    rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Install Chromedriver
RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{ print $3 }' | awk -F'.' '{ print $1 }') && \
    wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION.0.4472.101/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    chmod +x chromedriver && \
    mv chromedriver /usr/local/bin/

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]
