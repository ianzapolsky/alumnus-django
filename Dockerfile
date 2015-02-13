FROM ubuntu

MAINTAINER Ian Zapolsky

EXPOSE 8000

RUN apt-get update && apt-get install -y \
    python \
    python-dev \
    curl \
    git \
    libpq-dev \
    python-pip

COPY . /home/alumnus-django

RUN sudo pip install -r /home/alumnus-django/requirements.txt

WORKDIR /home/alumnus-django/

RUN python manage.py syncdb --noinput --settings=alumnus.settings.prod

RUN python manage.py migrate --noinput --settings=alumnus.settings.prod

RUN python manage.py collectstatic --noinput --settings=alumnus.settings.prod

CMD gunicorn -b 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=alumnus.settings.prod alumnus.wsgi

