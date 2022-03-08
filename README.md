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
GET | / |
GET | /customers |
GET | /customers/{id} |
GET | /customers/{id}/addresses |
PUT | /customers/{id} |
DELETE | /customers/{id} |
DELETE | /customers/{id}/addresses |

## Usage

Open the repository in docker container and run flask in terminal:

```console
flask run
```

Open new terminal and run the following commands for different endpoints: 

To create a customer:
```console
curl -X POST localhost:8000/customers -H 'Content-Type: application/json' -d '{"first_name":"myfirstname", "last_name":"mylastname", "userid":"myuserid","password":"my_password","addresses":["myaddress1"]}'
```

To retrieve all customers:
```console
curl -X GET localhost:8000/customers
```

To retrieve a valid customer by id:
```console
curl -X GET localhost:8000/customers/{id}
```

To update a valid customer by id:
```console
curl -X PUT localhost:8000/customers/{id} -H 'Content-Type: application/json' -d '{"first_name":"myfirstnameupdated", "last_name":"mylastnameupdated", "userid":"myuserid","password":"my_password","addresses":["myaddress1","myaddress2"]}'
```

To delete a valid customer by id:
```console
curl -X DELETE localhost:8000/customers/{id}
```

This repository is part of the NYU class **CSCI-GA.2810-001: DevOps and Agile Methodologies** taught by John Rofrano, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science.