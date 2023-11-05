# MY-API
## Overview

Briefly describe your project and its purpose.

## Prerequisites

List any prerequisites that need to be installed or set up before using your API.

- Python 3.x
- FastAPI
- Firebase Admin SDK
- Redis (if used for rate limiting)
- Other dependencies

## Installation

Provide step-by-step instructions on how to install and set up your project.

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
3. Configure your environment variables, including Firebase credentials.
4. (If applicable) Set up and configure your Redis server for rate limiting.

## Usage

Explain how to use your API, including:

- Starting the FastAPI application.
- Making API requests (e.g., using Postman or cURL).
- Authentication requirements.
- Common use cases and examples.

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

## Rate Limiting

Explain any rate limiting mechanism used in your project and how it's configured.

## Testing

Provide instructions on how to run unit tests for your project.

## API Documentation

If available, include a link to your Postman collection or equivalent API documentation.
