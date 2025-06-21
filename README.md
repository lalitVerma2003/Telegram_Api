# Telegram API Integration with Django and Celery

This project integrates the Telegram Bot API with a Django Rest Framework (DRF) backend, featuring user authentication, background task processing with Celery and Redis, and secure API endpoints.

## Table of Contents

* [Features](#features)

* [Project Structure](#project-structure)

* [Setup Instructions](#setup-instructions)

  * [Prerequisites](#prerequisites)

  * [Clone the Repository](#clone-the-repository)

  * [Environment Variables](#environment-variables)

  * [Install Dependencies](#install-dependencies)

  * [Database Migrations](#database-migrations)

  * [Running Redis and Celery](#running-redis-and-celery)

* [How to Run Locally](#how-to-run-locally)

  * [Run Django Server](#run-django-server)

  * [Run Celery Worker](#run-celery-worker)

  * [Run Telegram Bot Script](#run-telegram-bot-script)

* [API Documentation](#api-documentation)

  * [Base URL](#base-url)

  * [API Key](#api-key)

  * [Authentication](#authentication)

  * [Endpoints](#endpoints)

    * [1. Register (Public)](#1-register-public)

    * [2. Login (Public)](#2-login-public)

    * [3. Profile (Protected)](#3-profile-protected)

* [Telegram Bot Integration](#telegram-bot-integration)

* [Login for Web-based Access](#login-for-web-based-access)

* [License](#license)

## Features

* **Django Project Setup**: Configured with Django Rest Framework for robust API development.

* **Secure Settings**: `DEBUG=False` for production-ready settings with environment variables for sensitive data.

* **API Development**:

  * **Public Endpoints**: Accessible with an API key (e.g., Register, Login).

  * **Protected Endpoints**: Accessible only to authenticated users using JWT (e.g., Profile).

* **Django Login**: Implemented for traditional web-based access (admin panel).

* **Celery Integration**: Background task processing with Redis as the broker.

  * Example task: Sending an email after user registration.

* **Telegram Bot Integration**:

  * Collects Telegram usernames when users send a `/start` command to the bot.

  * Stores Telegram usernames in the Django database.

## Project Structure

.
├── YourDjangoProjectName/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│   └── celery.py (for Celery tasks)
├── YourApp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── serializers.py
├── manage.py
├── requirements.txt
├── .env.example
├── telegram_bot.py # Assuming this is your bot's script
└── README.md


## Setup Instructions

### Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python 3.8+**

* **pip** (Python package installer)

* **Redis Server**: Used as the Celery broker.

  * [Installation Guide for Redis](https://redis.io/docs/getting-started/installation/)

### Clone the Repository

First, clone the project repository to your local machine:

git clone https://github.com/lalitVerma2003/Telegram_Api.git
cd Telegram_Api


### Environment Variables

This project uses environment variables to manage sensitive information and configuration settings.

1. Create a `.env` file in the root directory of your project. You can copy the `.env.example` file:

cp .env.example .env


2. Open the `.env` file and fill in the following variables:

| Variable | Description | Example Value | 
 | ----- | ----- | ----- | 
| `DB_NAME` | Database name. | `your_db_name` | 
| `DB_USER` | Database user. | `your_db_user` | 
| `DB_PASSWORD` | Database password. | `your_db_password` | 
| `DB_HOST` | Database host. | `localhost` | 
| `DB_PORT` | Database port. | `5432` | 
| `CELERY_BROKER_URL` | URL for the Redis server. | `redis://localhost:6379/0` | 
| `CELERY_RESULT_BACKEND` | URL for the Redis server. | `redis://localhost:6379/0` | 
| `TELEGRAM_BOT_TOKEN` | Your Telegram Bot API token (obtained from BotFather). | `YOUR_TELEGRAM_BOT_TOKEN_HERE` | 
| `X_API_KEY` | The custom API key required for public endpoints. | `telegram@12345api` | 
| `EMAIL_HOST_USER` | Email address for sending emails. | `your_email@example.com` | 
| `EMAIL_HOST_PASSWORD` | Password for the email account. | `your_email_password` | 

**Note:** For `SECRET_KEY`, you can generate a new one using `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`.

### Install Dependencies

Install the required Python packages using `pip`:

pip install -r requirements.txt


### Database Migrations

Apply the database migrations to create the necessary tables:

python manage.py migrate


Optionally, create a superuser for accessing the Django admin panel:

python manage.py createsuperuser


### Running Redis and Celery

Ensure your Redis server is running. If you installed it locally, you can usually start it with:

redis-server


## How to Run Locally

### Run Django Server

Start the Django development server:

python manage.py runserver


The API will be accessible at `http://localhost:8000`.

### Run Celery Worker

In a **separate terminal**, start the Celery worker to process background tasks:

celery -A YourDjangoProjectName worker --loglevel=info


*(Replace `YourDjangoProjectName` with the actual name of your Django project directory, usually the one containing `settings.py`)*

### Run Telegram Bot Script

If your Telegram bot logic is implemented in a separate Python script (e.g., `telegram_bot.py`), run it in **another separate terminal**:

python telegram_bot.py


## API Documentation

The API endpoints are designed for interaction with your application.

### Base URL

All API requests should be prefixed with: `http://localhost:8000/api/v1/auth/`

### API Key

A custom API key is required for all API endpoints. Include it in the `x-api-key` header:

`x-api-key: telegram@12345api` (This value is configured in your `.env` as `DJANGO_API_KEY`)

### Authentication

* **Public Endpoints**: Require the `x-api-key` header.

* **Protected Endpoints**: Require both the `x-api-key` header and a `Bearer` token in the `Authorization` header, obtained after a successful login.

### Endpoints

#### 1. Register (Public)

Registers a new user in the system. After successful registration, a background task (e.g., sending a welcome email) is triggered via Celery.

* **URL:** `/api/v1/auth/register/`

* **Method:** `POST`

* **Headers:**

  * `x-api-key: telegram@12345api`

  * `Content-Type: application/json`

* **Request Body (JSON):**

{
"email": "lalitverma1650@gmail.com",
"fullname": "Lalit",
"password": "Test@1234",
"phone_no": "94792742694297",
"country_code": "+91",
"profile_pic_url": "https://example.com/profile.jpg",
"device_token": "abcd1234fffefgh5678987",
"device_id": "ABC12345fef",
"device_type": "mobile",
"os": "android"
}


* **Example cURL:**

curl --location 'http://localhost:8000/api/v1/auth/register/'

--header 'x-api-key: telegram@12345api'

--header 'Content-Type: application/json'

--data-raw '{
"email": "lalitverma1650@gmail.com",
"fullname": "Lalit",
"password":"Test@1234",
"phone_no": "94792742694297",
"country_code": "+91",
"profile_pic_url": "https://example.com/profile.jpg",
"device_token": "abcd1234fffefgh5678987",
"device_id": "ABC12345fef",
"device_type": "mobile",
"os": "android"
}'


#### 2. Login (Public)

Authenticates a user and returns JWT access and refresh tokens.

* **URL:** `/api/v1/auth/login/`

* **Method:** `POST`

* **Headers:**

* `x-api-key: telegram@12345api`

* `Content-Type: application/json`

* **Request Body (JSON):**

{
"email": "lalit.verma@yopmail.com",
"password": "Test@1234",
"device_token": "abcd1234fffefgh5678987",
"device_id": "ABC12345fef",
"device_type": "mobile",
"os": "android"
}


* **Example cURL:**

curl --location 'http://localhost:8000/api/v1/auth/login/'

--header 'x-api-key: telegram@12345api'

--header 'Content-Type: application/json'

--data-raw '{
"email": "lalit.verma@yopmail.com",
"password":"Test@1234",
"device_token": "abcd1234fffefgh5678987",
"device_id": "ABC12345fef",
"device_type": "mobile",
"os": "android"
}'


#### 3. Profile (Protected)

Retrieves the authenticated user's profile information. This endpoint requires a valid JWT access token.

* **URL:** `/api/v1/auth/profile/`

* **Method:** `GET`

* **Headers:**

* `x-api-key: telegram@12345api`

* `Authorization: Bearer <YOUR_JWT_ACCESS_TOKEN>`

* **Example cURL:**

curl --location 'http://localhost:8000/api/v1/auth/profile/'

--header 'x-api-key: telegram@12345api'

--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTg3NzUwLCJpYXQiOjE3NTA1MDEzNTAsImp0aSI6ImYzODE4NGIxMzgwNzQ0NTg5YWEzZTRiZjZlZTY5Njk3IiwidXNlcl9pZCI6IjU3MmM3ODFhLTM2YjUtNDIwYi04N2I4LWZkYWNmNjRiZjcwOSJ9.XY3lFmZjb9XPaz2AuSef3DMxQsjUrWOrqC1a3qUSAJ8'


*(**Note:** Replace the example JWT token with a fresh one obtained from the login endpoint.)*

## Telegram Bot Integration

To enable the Telegram Bot functionality:

1. **Create a Telegram Bot**: Talk to [@BotFather](https://t.me/BotFather) on Telegram and create a new bot. You will receive an API token.

2. **Set `TELEGRAM_BOT_TOKEN`**: Add this token to your `.env` file.

3. **Run the Bot Script**: Ensure your `telegram_bot.py` script (or equivalent) is running as described in the [How to Run Locally](#run-telegram-bot-script) section. If your bot's `/start` command handler is part of your Django application (e.g., via webhooks), ensure your Django application is accessible to Telegram (e.g., using ngrok for local development).

When a user sends the `/start` command to your Telegram bot, the bot will collect their Telegram username and store it in your Django database.

## Login for Web-based Access

You can access the Django admin panel at `http://localhost:8000/admin/` using the superuser credentials you created earlier. This allows for web-based management of your Django models and data.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
