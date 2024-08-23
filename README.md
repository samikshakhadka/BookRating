Given that you're using Docker, it's important to include specific instructions and details related to Docker in the `README.md`. Here's the updated content with Docker-specific instructions:

---

# BookRating Site

Welcome to the **BookRating Site**! This project is a Django-based web application designed to manage and rate books through a RESTful API. The application utilizes Django Rest Framework (DRF) for API implementation, Postgres for database management, Redis for caching, and Celery for task scheduling. It also features token-based authentication, custom permissions, and unit tests.

## Features

- **CRUD Operations**: Full CRUD operations for managing books and ratings through RESTful APIs.
- **Authentication**: Token-based authentication to secure the API.
- **Custom Permissions**: Custom permission classes to manage access control.
- **Caching**: Utilizes Redis for efficient caching of frequently accessed data.
- **Task Scheduling**: Celery is integrated for background task processing.
- **Filtering**: Django Filters are applied to filter API responses.
- **Rating System**: Calculate and display book ratings and average ratings.
- **Custom Django Command**: A custom Django management command that fetches data from the [Google Books API](https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}) and populates the book model.
- **Unit Testing**: Comprehensive unit tests written using Factory Boy and Mock.

## Technology Stack

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: PostgreSQL (Locally hosted)
- **Caching**: Redis
- **Task Scheduling**: Celery
- **Testing**: Factory Boy, Mock
- **Authentication**: Token-based

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- PostgreSQL (Locally hosted)
- Redis

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samikshakhadka/BookRating.git
   cd BookRating
   ```

2. **Create and Configure Environment Variables**:
   - Create a `.env` file in the root directory and add the necessary environment variables such as `DJANGO_DB_NAME`, `DJANGO_DB_USER`, `DJANGO_DB_PASSWORD`, `DJANGO_DB_HOST`, and `DJANGO_DB_PORT`.
   - Ensure that `DJANGO_DB_HOST` is set to your host's IP address or `host.docker.internal` (depending on your operating system).

3. **Build and Start the Docker Containers**:
   - Build and start the Docker containers using Docker Compose:
     ```bash
     docker-compose up --build
     ```

4. **Run Migrations**:
   - Once the containers are up, run the database migrations:
     ```bash
     docker-compose run web python manage.py migrate
     ```

5. **Start Redis and Celery**:
   - Ensure Redis is running (this should be handled by Docker Compose) and start Celery within the Docker container:
     ```bash
     docker-compose run worker
     ```

6. **Run the Development Server**:
   - The development server should already be running inside the Docker container, accessible at `http://localhost:8000` or the appropriate IP address.

7. **Run the Custom Django Command**:
   - To fetch book data from the Google Books API and populate the book model, run:
     ```bash
     docker-compose run web python manage.py fetch_books
     ```

## Usage

### Authentication

The API uses token-based authentication. To access the secured endpoints, include the token in the `Authorization` header:
```bash
Authorization: Token <your_token>
```

### Testing

Unit tests are written using Factory Boy and Mock. To run the tests, use the following command:
```bash
docker-compose run web python manage.py test
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss the changes you would like to make.

---

This version of the `README.md` includes Docker-specific instructions for setting up and running the project. It also emphasizes the need to configure environment variables correctly, particularly the database host, which is crucial when using a locally hosted database with Docker.
