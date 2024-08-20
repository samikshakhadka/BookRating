
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
- **Unit Testing**: Comprehensive unit tests written using Factory Boy and Mock.

## Technology Stack

- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **Caching**: Redis
- **Task Scheduling**: Celery
- **Testing**: Factory Boy, Mock
- **Authentication**: Token-based

## Setup Instructions

### Prerequisites

- Python 3.x
- PostgreSQL
- Redis
- Virtualenv

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/samikshakhadka/BookRating.git
   cd BookRating
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup PostgreSQL Database**:
   Create a PostgreSQL database and configure the database settings in `settings.py`.

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Start Redis and Celery**:
   Ensure Redis is running and start Celery with the following command:
   ```bash
   celery -A BookRating worker --loglevel=info
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
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
python manage.py test
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss the changes you would like to make.
