# Catalog service
## API

The service exposes two API calls: a GET request (query API) and a PUT request (update API).

You can run with Docker or you can run locally in your computer. 

To run with Docker:

```
$ docker build -t catalog_service .
```

```
$ docker run -p 5002:5002 catalog_service
```

**Query request**:

In terminal:

```
$ curl --header "Content-Type: application/json" --request GET  --data '{"topic":"distributed systems"}' http://localhost:5002/catalog/query
{
  "Books": [
    {
      "id": 1, 
      "stock": 3, 
      "title": "How to get a good grade in 677 in 20 minutes a day.", 
      "topic": "distributed systems"
    }, 
    {
      "id": 2, 
      "stock": 3, 
      "title": "RPCs for Dummies.", 
      "topic": "distributed systems"
    }
  ]
}
```

```
$ curl --header "Content-Type: application/json" --request GET  --data '{"title":"graduate school"}' http://localhost:5002/catalog/query
{
  "Books": [
    {
      "id": 3, 
      "stock": 3, 
      "title": "Xen and the Art of Surviving Graduate School.", 
      "topic": "graduate school"
    }, 
    {
      "id": 4, 
      "stock": 3, 
      "title": "Cooking for the Impatient Graduate Student.", 
      "topic": "graduate school"
    }
  ]
}
```

```
$ curl --header "Content-Type: application/json" --request GET  --data '{"id": 1}' http://localhost:5002/catalog/query
{
  "Books": [
    {
      "id": 1, 
      "stock": 3, 
      "title": "How to get a good grade in 677 in 20 minutes a day.", 
      "topic": "distributed systems"
    }
  ]
}
```

In python

```python
>>> import requests
>>> r = requests.get("http://localhost:5002/catalog/query", json={"topic":"distributed systems"}) 
>>> r.text
'{\n  "Books": [\n    {\n      "id": 1, \n      "stock": 3, \n      "title": "How to get a good grade in 677 in 20 minutes a day.", \n      "topic": "distributed systems"\n    }, \n    {\n      "id": 2, \n      "stock": 3, \n      "title": "RPCs for Dummies.", \n      "topic": "distributed systems"\n    }\n  ]\n}\n'
>>> r = requests.get("http://localhost:5002/catalog/query", json={"id": 1}) 
>>> r.text
'{\n  "Books": [\n    {\n      "id": 1, \n      "stock": 3, \n      "title": "How to get a good grade in 677 in 20 minutes a day.", \n      "topic": "distributed systems"\n    }\n  ]\n}\n'
```

**Update request**:

Here, I assume that we use the book id above to buy. However, we can discuss about this!

In terminal, 

```
$ curl --header "Content-Type: application/json" --request PUT  --data '{"id": 1}' http://localhost:5002/catalog/update
{
  "success": true
}
```

In python,

```python
>>> r = requests.put("http://localhost:5002/catalog/update", json={"id": 1}) 
>>> r.text
'{\n  "success": true\n}\n'
```

## Logging

Logging happens in logfile.json inside the Docker container catalog-service, to check if the logging is there:

```
$ docker exec -it catalog-service bash 
```

Inside the container, check the logfile.json:

```
$ cat logfile.json
```

A buy request will be logged in the "buy" key of the json object. A query request will be logged in the "query" key of the json object. 