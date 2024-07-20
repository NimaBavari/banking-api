# Entrix Simple Banking System

by Tural Mahmudov

**time spent:** 8 hours

## Overview

This documentation provides an in-depth explanation of a microservice with a REST API designed to handle banking operations. The microservice is structured into five layers, each responsible for specific functionalities, and integrates with a PostgreSQL database. The microservice uses Flask for the HTTP API, SQLAlchemy for ORM, and unittest for unit testing. Gunicorn is used as the production server with four threads, and data isolation is implemented to prevent race conditions.

The microservice consists of the following layers, from the lowest to the highest:

1. **DB Layer:** Integrates with PostgreSQL.
2. **ORM Layer:** Defines data object models using SQLAlchemy.
3. **Repository Layer:** Contains repositories for each object model.
4. **Service Layer:** Provides an interface for all banking operations.
5. **HTTP API Layer:** Handles HTTP requests and responses using Flask.

Custom exceptions are defined and used to handle errors across different layers. Exceptions are chained from the lowest to the highest level, providing detailed error information.

The microservice is fully dockerized and integrates with a Postgres service (waiting for it to be ready before connecting at start up).

It uses a simple logger with stdout handler.

The code is clean, type-checked. It uses the best practices in Python, REST API design, microservices architecture, and virtualization for easy deployment.

## Usage

### Start Up

You can start the system by running

```sh
docker-compose up -d
```

### Monitoring

You can get the entire docker logs by running

```sh
docker-compose logs --follow
```

or, alternately, you can get the logs from an individual container by running

```sh
docker container logs <container-name> --follow
```

### REST API

The API allows you to create customers and accounts, check balances, transfer amounts between accounts, and fetch transfer history. The service ensures robust error handling and logging for better debugging and maintenance.

#### Create A Customer

```http
POST /customers HTTP/1.1
Content-Type: application/json

{
    "name": "John Doe"
}
```

Response on success:

```http
{
    "id": 1,
    "name": "John Doe"
}, 201
```

Response on error:

```
400 Malformed request.
```

or

```
503 Customer not created.
```

#### Create an Account

```http
POST /accounts HTTP/1.1
Content-Type: application/json

{
    "customer_id": 1,
    "initial_deposit": 100.0
}
```

Response on success:

```http
{
    "id": 1,
    "customer_id": 1,
    "balance": 100.0
}, 201
```

Response on error:

```
400 Malformed request.
```

or

```
503 Account not created.
```

#### Get Account Balance

```http
GET /accounts/<int:account_id>/balance HTTP/1.1
```

Response on success:

```http
{
    "balance": 100.0
}, 200
```

Response on error:

```
404 Account not found.
```

#### Transfer Amount

```http
POST /transfers HTTP/1.1
Content-Type: application/json

{
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": 50.0
}
```

Response on success:

```http
{
    "id": 1,
    "from_account_id": 1,
    "to_account_id": 2,
    "amount": 50.0,
    "timestamp": "2024-07-20T12:34:56Z"
}, 200
```

Response on error:

```
400 Malformed request.
```

or

```
404 Account not found.
```

or

```
403 Insufficient funds.
```

or

```
503 Account not created.
```

#### Get Transfer History

```http
GET /accounts/<int:account_id>/transfers HTTP/1.1
```

Response on success:

```http
[
    {
        "id": 1,
        "from_account_id": 1,
        "to_account_id": 2,
        "amount": 50.0,
        "timestamp": "2024-07-20T12:34:56Z"
    },
    {
        "id": 2,
        "from_account_id": 1,
        "to_account_id": 3,
        "amount": 25.0,
        "timestamp": "2024-07-21T14:56:78Z"
    }
], 200
```

### Testing

To run tests, run:

```sh
docker exec banking-api-tswpbk_api_1 python3 -m unittest
```

## Scripts

To lint, format, and check static typing, run:

```sh
chmod +x cleanup.sh
./cleanup.sh
```

from the project root.
