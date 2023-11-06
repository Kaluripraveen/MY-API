# MY-API
## Overview

user management system backend using Firebase.The system will provide
APIs to perform user registrations, user logins, and the ability to retrieve, update, and delete
user profiles and also reset-password.file system is used in this project where user password is stored in 
separate JSON file with respected email address.for security purpose password are encode and hashed using 
base64 library.

## Prerequisites

- Python 3.x
- FastAPI
- uvicorn
- Firebase Admin SDK
- Redis (if used for rate limiting)
-  fastapi-limiter
- bcrypt
- base64
- pytest
- requests
- httpx
- pytest-asyncio(Unit testing)

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
3. Configure your environment variables, including Firebase credentials.
4. (If applicable) Set up and configure your Redis server for rate limiting.

## Usage

- Starting the FastAPI application.
- Making API requests (e.g., using Postman or cURL).

## API Endpoints

### `/register` (POST)

- Description: Register a new user.
- Parameters: `email`, `password`, `username`, `full_name`

### `/login` (POST)

- Description: Log in a user and receive a custom token.
- Parameters: `email`, `password`

### `/user/{email}` (GET)

- Description: Get user profile by email.
- Parameters: `email`

### `/user/{email}` (PUT)

- Description: Update user profile by email.
- Parameters: `email`, `username`, `full_name`

### `/user/{email}` (DELETE)

- Description: Delete a user by email.
- Parameters: `email`
- 
### `/reset-pasword` (PUT)
- Description: Update user password.
- Parameters: `email`.`new_password`

## Testing

For Unit Testing 
run command in your terminal pytest Test_main.py
note:don't run command twice,if u want to run agian change user data in new_user_data funtion

## API Documentation

Postman Collections is provided in this respository:MY API.postman_collection.json
import this file to your postman application.
