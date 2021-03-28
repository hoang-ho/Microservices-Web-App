# Multi-tier Microservices WebApp

To deploy locally, git clone the repo

```
$ cd Microservices-web-app
$ docker compose up
```

For your service to be built with docker compose, append your service in the docker-compose.yml, specify the container_name, build and port

To call the catalog service, use "http://catalog-service:5002/catalog". Use the container_name as the host!

Code for each microservice is in the corresponding folder.