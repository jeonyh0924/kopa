# KOPA
- 관광공사에서 제공하는 Open API를 활용하여 디바이스 주변의 관광지를 추천
- 유명 셀럽들이 운영하는 장소 추천.
- 서울시에서 제공하는 테마 관광을 제공
- 지정한 관광지에 따른 데이터를 ios에서 동적으로 제공

## installation
- python 3.7.4
- django 2.2.12

```shell

  pyenv virtualenv 3.7.4 <가상환경 이름>
  pyenv local <가상환경 이름>
  pip install django

  pip install -r requiremens.text
  cd app
  ./manage.py makemigrations
  ./manage.py migrate
  ./manage.py createsuperuser
```

```shell
# secret.json
{
  "SECRET_KEY": "<django key>",
  "AWS_ACCESS_KEY_ID":"< AWS s3 KEY>",
  "AWS_SECRET_ACCESS_KEY": "< AWS s3 secret key>",
  "TourAPI" :"<관광공사 open api >"
}

# dev.json, production.json
{
  "DATABASES": {
    "default": {
      "ENGINE": "django.db.backends.sqlite3",
      "NAME": "db.sqlite3"
    }
  }
}

```

# deploy

- ecs

작업 정의 : 작업 정의 이름 : KopaECS

컨테이너 정의 : 컨테이너 이름 : container-Kopa

클러스터 이름 : kopa-cluster

keypair : kopa-keypair.pem

서비스 이름 : service-kopa

로드벨런서 이름 : kopa-deploy-loadbalancer

- s3 

버킷 이름: kopadeploys3
