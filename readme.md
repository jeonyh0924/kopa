# KOPA

- python 3.7.4
- django 2.2.12

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