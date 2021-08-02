# selfity

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/e94eb13f476eef237d86?action=collection%2Fimport)

Check out the project's [documentation](http://LopsanAMO.github.io/selfity/).


# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)  

# Initialize the project

Copie the .env.sample file to a new file called .env.

```bash
cp .env.sample .env
```
update the .env entries to real values:

```bash
DB_NAME=dbname
DB_USER=rootuser
DB_PASS=changeme
ALLOWED_HOSTS=127.0.0.1
SMSURL=http://example.com
SMSAPIKEY=XXXXX-XXXX
DJANGO_AWS_STORAGE_BUCKET_NAME=XXXXXXX
DJANGO_AWS_SECRET_ACCESS_KEY=XXXXX
DJANGO_AWS_ACCESS_KEY_ID=XXXXXXX
DJANGO_CONFIGURATION=Production
DJANGO_SECRET_KEY=local
```


Start the dev server for local development:
```bash
docker-compose up
```

Run a command inside the docker container:

```bash
docker-compose run --rm web [command]
```

# Documentation


#### [Documentation](http://ec2-3-128-185-203.us-east-2.compute.amazonaws.com/api/schema/swagger-ui/) ```http://ec2-3-128-185-203.us-east-2.compute.amazonaws.com/api/schema/swagger-ui/```