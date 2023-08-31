FROM python:3.8

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic --noinput

CMD ["python3", "manage,py", "migrate"]

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "project.wsgi:application"]
