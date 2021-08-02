FROM python:3.8
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt /requirements.txt
COPY ./app /app
WORKDIR /app
RUN pip install -r /requirements.txt


EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - selfity.wsgi:application