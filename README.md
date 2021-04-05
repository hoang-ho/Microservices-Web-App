# Multi-tier Microservices WebApp
Programming Lab2 for the course CS 677: Distributed OS. In this lab we have to implement a microservices architecture using REST APIs.

## To deploy to EC2

Create 3 EC2 instances using ami-061bda79b8ea8bbe2 (this is a customized image with docker, docker-composed and git installed and security group and networks set up).
> Note: If you want to use your own ami, you need to set up docker, git and security group beforehand

```
$ s 
$ aws ec2 describe-instances --instance-id $INSTANCE_ID
```

From the last command, save down the Public IPv4 DNS and the Private IPv4 addresses for each instance. Next, ssh into the instance

```
$ ssh -i "677kp.pem" ec2-user@$PUBLIC_IPv4_DNS
```

Clone the repo inside the instance

```
$ git clone https://github.com/hoang-ho/Microservices-Web-App.git
$ cd Microservices-Web-App
```

For the instance you choose to server the catalog-service, put its Private IPv4 address to the config_env, similarly for order-service. You repeat this step for EC2 instances that you choose to server front-end-service and the order-service.
> Note: If you want to change the port, please use ports from range 5000 - 6000 because the security group is set up for port in that range. Remember to update the config_env accordingly!

```
# Modify the config_env
$ vim config_env
```

Now we're done setting up and will start deploying:

In the instance you choose to be front-end-service

```
$ docker-compose up --build front-end-service
```

In the instance you choose to be catalog-service

```
$ docker-compose up --build catalog-service
```

In the instance you choose to be order-service

```
$ docker-compose up --build order-service
```

From your local machine, to test the API

```
$ curl --request GET $FRONT_END_PUBLIC_IPv4_DNS:5004/search/graduate-school

{
    "items": {
        "Cooking for the Impatient Graduate Student.": 4,
        "Xen and the Art of Surviving Graduate School.": 3
    }
}
```

```
$ curl --request GET $FRONT_END_PUBLIC_IPv4_DNS:5004/search/distributed-systems

{
    "items": {
        "How to get a good grade in 677 in 20 minutes a day.": 1,
        "RPCs for Dummies.": 2
    }
}
```

```
$ curl --request POST $FRONT_END_PUBLIC_IPv4_DNS:5004/buy/2

{
    "message": "book bought successful"
}
```

```
$ curl --request GET $FRONT_END_PUBLIC_IPv4_DNS:5004/lookup/2

{
    "cost": 10.0,
    "stock": 999
}
```

Example output:

```
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request GET ec2-107-22-145-248.compute-1.amazonaws.com:5004/search/distributed-systems
{
    "items": {
        "How to get a good grade in 677 in 20 minutes a day.": 1,
        "RPCs for Dummies.": 2
    }
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request GET ec2-107-22-145-248.compute-1.amazonaws.com:5004/search/graduate-school
{
    "items": {
        "Cooking for the Impatient Graduate Student.": 4,
        "Xen and the Art of Surviving Graduate School.": 3
    }
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request POST ec2-107-22-145-248.compute-1.amazonaws.com:5004/buy/2
{
    "message": "something went wrong. Please try again"
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --header "Content-Type: application/json" --request PUT --data '{"id": 2}' ec2-100-27-24-110.compute-1.amazonaws.com:5007/order
curl: (7) Failed to connect to ec2-100-27-24-110.compute-1.amazonaws.com port 5007: Connection refused
(base) Hoangs-MacBook-Pro:~ hoangho$ 
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request GET ec2-107-22-145-248.compute-1.amazonaws.com:5004/search/graduate-school
{
    "items": {
        "Cooking for the Impatient Graduate Student.": 4,
        "Xen and the Art of Surviving Graduate School.": 3
    }
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request GET ec2-107-22-145-248.compute-1.amazonaws.com:5004/search/distributed-systems
{
    "items": {
        "How to get a good grade in 677 in 20 minutes a day.": 1,
        "RPCs for Dummies.": 2
    }
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request POST ec2-107-22-145-248.compute-1.amazonaws.com:5004/buy/2
{
    "message": "book bought successful"
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request POST ec2-107-22-145-248.compute-1.amazonaws.com:5004/lookup/2
{
    "message": "The method is not allowed for the requested URL."
}
(base) Hoangs-MacBook-Pro:~ hoangho$ curl --request GET ec2-107-22-145-248.compute-1.amazonaws.com:5004/lookup/2
{
    "cost": 10.0,
    "stock": 999
}
```

## Simulate Concurrency

To simulate a concurrency situation with buy and update, run the SimulateConcurrency.py. Example Output:

```
(base) Hoangs-MacBook-Pro:Microservices-Web-App hoangho$ python3 SimulateConcurrency.py --front-end-dns ec2-3-84-157-29.compute-1.amazonaws.com --catalog-dns ec2-54-164-223-101.compute-1.amazonaws.com
INFO:root:Look up the book stock and cost after update and buy: {
    "cost": 10.0,
    "stock": 1000
}
 
INFO:root:Main    : create and start thread 0.
INFO:root:Calling request http://ec2-54-164-223-101.compute-1.amazonaws.com:5002/catalog/update at timestamp 1617647399.7801511
INFO:root:Calling request http://ec2-54-164-223-101.compute-1.amazonaws.com:5002/catalog/update at timestamp 1617647399.7802508
INFO:root:Main    : create and start thread 1.
INFO:root:Calling request http://ec2-3-84-157-29.compute-1.amazonaws.com:5004/buy/2 at timestamp 1617647399.7807848
INFO:root:Main    : create and start thread 2.
INFO:root:Calling request http://ec2-54-164-223-101.compute-1.amazonaws.com:5002/catalog/update at timestamp 1617647399.781227
INFO:root:Main    : before joining thread 0.
INFO:root:Calling request http://ec2-54-164-223-101.compute-1.amazonaws.com:5002/catalog/update at timestamp 1617647399.7819872
INFO:root:Response: {
  "book": "RPCs for Dummies.", 
  "message": "Done update"
}
 at time stamp 1617647399.89176
INFO:root:Main    : thread 0 done
INFO:root:Main    : before joining thread 1.
INFO:root:Response: {
  "book": "RPCs for Dummies.", 
  "message": "Done update"
}
 at time stamp 1617647399.896009
INFO:root:Response: {
    "message": "book bought successful"
}
 at time stamp 1617647399.9221802
INFO:root:Main    : thread 1 done
INFO:root:Main    : before joining thread 2.
INFO:root:Main    : thread 2 done
INFO:root:Look up the book stock and cost after update and buy: {
    "cost": 2000.0,
    "stock": 1999
}
```

TODO: Please update the response for buy request and update the example output for SimulateConcurrency.py 

As we can see from the terminal log, we have 2 update requests and 1 buy requests. The two update requests are done first, and thus, the stock for book 2 is set to 2000.0 and its cost is set to 2000.0. When the buy request comes in, the stock is set to 1999 and the cost remains the same!

## Milestone 1

**Deliverables:** A bookstore running on a single server with a single buyer. The bookstore components (front-end, catalogue and order) are deployed as three processes and a fourth process representing the client performing interface calls to the front-end process.

**Assumption:** As per the documentation, the `search` operation returns only `id and topic` fields and the `lookup` operation returns only `cost and stock` fields.

### Overview 
The following is a brief description of each microservice implemented.

- Front End Server: The users will interact with this server. It is responsible for the processing and abstracting back-end servers from the users. The implementation of this server is under the folder `./FrontendService`. It consists of only one microservice that has the functionality of search for a book by topic, looking up for a book by it's id and buying the book by it's id.

- Catalog Server: This in one of the microservices that forms the back-end server. It is responsible of maintaining the catalog of the books availables and the cost and quantity of the books. Also, it implements the functionality of querying the catalog by `topic or id` and also updating the cost and quantity of books available. The implementation of this microservice is under the folder `./CatalogService`.

- Order Server: This is the second microservice in the back-end server. It is responsible for updating the quantity of the books available everytime it receives a request if the book is available in the catlaog. It also maintains a log of all the purchase orders it receives. The implementation of this microservice is under the folder `./OrderService`.

> Note: For more details on each service, please refer the individual README files in the folders.

### Setting up the code locally
**Prerequisites:** Please make sure that docker is installed and running locally.

To deploy locally, git clone the repo. Then perform the following steps in the mentioned order:

```
1. $ cd Microservices-web-app
2. $ docker-compose up --build -d
```

The last command will build images and run containers for each of the services in detach mode.

To run the services in the foreground run the following command:

```
$ docker-compose up --build
```

Also, to run only a particular container run the following command:

```
$ docker-compose up --build <service-name>
```
> Note: The available services are: front-end-service, catalog-service, order-service.

### Available commands to run from the client
**Prerequisites:** Please make sure the environment is runnning by following the above commands.

1. To search for books by topic:
> API Endpoint: GET http://localhost:5004/search/topic-name

```
$ curl --request GET http://localhost:5004/search/distributed-systems
{
    "items": {
        "How to get a good grade in 677 in 20 minutes a day.": 1,
        "RPCs for Dummies.": 2
    }
}
```
```
$ curl --request GET http://localhost:5004/search/graduate-school 
{
    "items": {
        "Cooking for the Impatient Graduate Student.": 4,
        "Xen and the Art of Surviving Graduate School.": 3
    }
}
```

2. To lookup books by id:
> API Endpoint: GET http://localhost:5004/lookup/book-id

```
$ curl --request GET http://localhost:5004/lookup/1
{
    "cost": 1.0,
    "stock": 1000
}
```

3. To buy a book by id:
> API Endpoint: POST http://localhost:5004/buy/book-id

```
$ curl --request POST http://localhost:5004/buy/2 
{
    "message": "book bought successful"
}
```

4. To hit the catalog service directly to update the cost or the stock of an item
   
```
$ curl --header "Content-Type: application/json" --request PUT  --data '{"id": 1, "stock":2000, "cost":2000}' http://localhost:5002/catalog/update
{
  "success": true
}
```

### Stopping and Removing the Containers
To stop and remove containers and images run the following command:

```
$ docker-compose down -v --rmi all --remove-orphans
```

### Test Script
Run test.sh to test the APIs. The output of the test is in a newly created txt file, out.txt.

### Logging for CatalogService

Logging happens in logfile.json inside the Docker container catalog-service, to check if the logging is there:

```
$ docker exec -it catalog-service bash 
```

Inside the container, check the logfile.json:

```
$ cat logfile.json
```

A buy request will be logged in the "buy" key of the json object. A query request will be logged in the "query" key of the json object. 