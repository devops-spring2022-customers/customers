
[![Build Status](https://github.com/devops-spring2022-customers/customers/actions/workflows/tdd.yml/badge.svg)](https://github.com/devops-spring2022-customers/customers/actions)
[![Build Status](https://github.com/devops-spring2022-customers/customers/actions/workflows/bdd.yml/badge.svg)](https://github.com/devops-spring2022-customers/customers/actions)
[![codecov](https://codecov.io/gh/devops-spring2022-customers/customers/branch/master/graph/badge.svg?token=8HK1MKH1PX)](https://codecov.io/gh/devops-spring2022-customers/customers)

# Customers Microservice

This is a Customer microservice for users and developers.

## Overview

This repository is an implementation of the Customer microservice supporting Create, Read, Update, Delete, and List functions as well as Post, Get, Put, and Delete API calls.

## Base URL

localhost:8000

## Service Endpoints

Methods | Rule |
--- | --- |
POST | /customers |
POST | /customers/{customer_id}/addresses
GET | / |
GET | /customers |
GET | /customers/{customer_id} |
GET | /customers/{customer_id}/addresses |
GET | /customers/{customer_id}/addresses/{address_id} |
PUT | /customers/{customer_id} |
PUT | /customers/{customer_id}/addresses/{address_id} |
DELETE | /customers/{customer_id} |
DELETE | /customers/{customer_id}/addresses/{address_id}|

## Usage

Open the repository in docker container and run flask in terminal:

```console
flask run
```

Open new terminal and run the following commands for different endpoints: 

To create a customer:
```console
curl -X POST localhost:8000/customers -H 'Content-Type: application/json' -d '{"first_name":"myfirstname", "last_name":"mylastname", "userid":"myuserid","password":"my_password", "addresses":[]}'
```

To create customer address:
```console
curl -X POST localhost:8000/customers/{customer_id}/addresses -H 'Content-Type: application/json' -d '{"address": "myaddress"}'
```

To retrieve customer address:
```console
curl -X GET localhost:8000/customers/{customer_id}/addresses/{address_id}
```

To retrieve all customer
```console
curl -X GET localhost:8000/customers
```

To retrieve customer by id
```console
curl -X GET localhost:8000/customers/{customer_id}
```

Base URL
```console
curl -X GET localhost:8000
```

To update customer by id
```console
curl -X PUT localhost:8000/customers/{id} -H 'Content-Type: application/json' -d '{"first_name":"myfirstnameupdated", "last_name":"mylastnameupdated", "userid":"myuserid","password":"my_password","addresses":[]}'
```

To update customer address
```console
curl -X PUT localhost:8000/customers/{customer_id}/addresses/{address_id} -H 'Content-Type: application/json' -d '{"addresses":"newaddress"}'
```

To delete customer
```console
curl -X DELETE localhost:8000/customers/{customer_id} -H 'Content-Type: application/json'
```

To delete customer address
```console
curl -X DELETE localhost:8000/customers/{customer_id}/addresses/{address_id} -H 'Content-Type: application/json'
```

This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.
