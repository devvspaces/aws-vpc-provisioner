# Docker Compose Example

Using docker to start and configure the applications.

## Requirements

- Docker

## Installation

1. Git clone or download the zip repository.
2. Update the .env file with your AWS credentials.

```bash
cp env.example .env
```

## Running the applications

```bash
docker compose up --build --detach
```

## How It Works

The `docker-compose.yml` file defines the services that make up the application. In this case, we have two services: `backend` and `frontend`.

The `backend` service is built using the `Dockerfile` in the `backend` directory. The `frontend` service is built using the `Dockerfile` in the `frontend` directory.

The `docker-compose.yml` file also defines the environment variables that are passed to the services. The `backend` service requires the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables to be set. These are set in the `.env` file available in the `backend` root directory.
