# KOPA

- python 3.7.4
- django 2.2.12

## installation
```shell
  pip freeze > requirements.txt
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
