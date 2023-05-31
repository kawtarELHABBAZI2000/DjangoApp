# FROM python:3.10.2-slim-bullseye

# ENV PIP_DISABLE_PIP_VERSION_CHECK 1
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /code

# COPY ./req.txt .

# RUN apt-get update -y && \
# pip install --upgrade pip && \
# pip install --no-cache-dir -r req.txt

# COPY ./entrypoint.sh .
# RUN chmod +x entrypoint.sh

# COPY . .

# ENTRYPOINT ["/code/entrypoint.sh"]

FROM python:3.10.4-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code


# Install dependencies
COPY . .

ENV DJANGO_SETTINGS_MODULE=imageNetProj.settings

RUN pip install -r requirements.txt
CMD bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
