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
INFO:root:Look up the book stock and cost before update and buy: {
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