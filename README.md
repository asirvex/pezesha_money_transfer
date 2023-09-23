
**Pezesha Money Transfer**

**README**

## Overview

Pezesha money transfer is a platform where you can register, sign in, and transfer money.

## Installation

To install the Pezesha money transfer application, follow these steps:

1. Install PostgreSQL.
2. Install Python version 3.10.
3. Clone the Pezesha money transfer repository:

```
git clone https://github.com/Pezesha/money-transfer.git
```

4. Install Pipenv:

```
pip install pipenv
```

5. Install the Pezesha money transfer application dependencies:

```
cd money-transfer
pipenv install
```

## Running the app

To run the Pezesha money transfer application, execute the following command:

```
python manage.py runserver
```

This will start the application on port 8000. You can access the application in your web browser at `http://localhost:8000`.

## Testing the app

To test the Pezesha money transfer application, execute the following command:

```
pytest
```

This will run all of the unit tests for the application.

## Usage

**To use the Pezesha money transfer application:**

1. Register for an account by sending a POST request to the `/api/accounts/users` endpoint with the following JSON body:

JSON

```
{
  "first_name": "Your first name",
  "last_name": "Your last name",
  "balance": "Your initial balance",
  "email": "Your email address",
  "password": "Your password"
}
```

Use code with caution. [Learn more](https://bard.google.com/faq#coding)

content_copy

2. Get your access token by sending a POST request to the `/api/accounts/token/get_token/` endpoint with the following JSON body:

JSON

```
{
  "email": "Your email address",
  "password": "Your password"
}
```

Use code with caution. [Learn more](https://bard.google.com/faq#coding)

content_copy

3. Transfer money by sending a POST request to the `/api/accounts/tranfer_money` endpoint with the following JSON body:

JSON

```
{
  "recipient_email": "Recipient's email address",
  "amount": "Amount to transfer"
}
```

Use code with caution. [Learn more](https://bard.google.com/faq#coding)

content_copy

You must include your access token in the `Authorization` header of the request to transfer money. For example, if your access token is `1234567890`, you would include the following header in your request:

```
Authorization: Bearer 1234567890
```

**Example transfer money request with access token:**

```
POST /api/accounts/tranfer_money HTTP/1.1
Host: example.com
Authorization: Bearer 1234567890
Content-Type: application/json

{
  "recipient_email": "asava2@gmail.com",
  "amount": "10"
}
```

## Swagger documentation

The Swagger documentation for the Pezesha money transfer application can be accessed at the following URL:

```
{base_url}/swagger
```

The Swagger documentation provides a detailed overview of the application's API.
