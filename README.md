# Multi-tier Microservices WebApp

To deploy locally, git clone the repo

```
$ cd Microservices-web-app
$ docker-compose up --build -d
```

The last command will build images and run containers for each services. 

To search for books by topic:

```
$ curl --request GET http://localhost:5004/search/distributed-systems
{
    "Books": [
        {
            "cost": 1.0,
            "id": 1,
            "stock": 1000,
            "title": "How to get a good grade in 677 in 20 minutes a day.",
            "topic": "distributed systems"
        },
        {
            "cost": 10.0,
            "id": 2,
            "stock": 1000,
            "title": "RPCs for Dummies.",
            "topic": "distributed systems"
        }
    ]
}

$ curl --request GET http://localhost:5004/search/graduate-school 
{
    "Books": [
        {
            "cost": 100.0,
            "id": 3,
            "stock": 1000,
            "title": "Xen and the Art of Surviving Graduate School.",
            "topic": "graduate school"
        },
        {
            "cost": 1000.0,
            "id": 4,
            "stock": 1000,
            "title": "Cooking for the Impatient Graduate Student.",
            "topic": "graduate school"
        }
    ]
}
```

To lookup books by id:

```
$ curl --request GET http://localhost:5004/lookup/1
{
    "Books": [
        {
            "cost": 1.0,
            "id": 1,
            "stock": 1000,
            "title": "How to get a good grade in 677 in 20 minutes a day.",
            "topic": "distributed systems"
        }
    ]
}
```

To buy a book by id:

```
$ curl --request POST http://localhost:5004/buy/2 
"{\"message\": \"Buy request successful\"}"
```

To stop and remove containers and images:

```
$ docker-compose down -v --rmi all --remove-orphans
```

Code for each microservice is in the corresponding folder.