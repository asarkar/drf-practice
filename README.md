# DRF Practice

This repository contains practice code for various Django REST Framework applications.

[![](https://github.com/asarkar/drf-practice/workflows/CI/badge.svg)](https://github.com/asarkar/drf-practice/actions)

## Projects

### quiz-api

A Quiz API based on the [Django REST Framework Quiz API](https://youtu.be/8QLCaye3YjQ) YouTube tutorial.

**Key Concepts:**
* Generic class-based views
* Nested serializers for related objects
* Translation
* Inline model editing (`InlineModelAdmin` objects)

**API Endpoints:**

| Method | Endpoint           | Description                           |
|--------|--------------------|---------------------------------------|
| GET    | `/quiz/`           | List all quizzes                      |
| GET    | `/quiz/r/<topic>/` | Retrieve a random question for a quiz |
| GET    | `/quiz/q/<topic>/` | Retrieve all questions for a quiz     |

### rental

A rental platform API based on the tutorial [Building APIs With Django REST Framework](https://www.jetbrains.com/help/pycharm/building-apis-with-django-rest-framework.html).

**Key Concepts:**
* Generic class-based views
* Nested serializers for related objects
* User authentication and authorization
* Custom permissions

**API Endpoints:**

| Method | Endpoint         | Description                                      |
|--------|------------------|--------------------------------------------------|
| GET    | `/offers/`       | List all offers                                  |
| POST   | `/offers/`       | Create a new offer (authenticated users only)    |
| GET    | `/offers/<id>/`  | Retrieve an offer                                |
| PUT    | `/offers/<id>/`  | Update an offer (author only)                    |
| PATCH  | `/offers/<id>/`  | Partially update an offer (author only)          |
| DELETE | `/offers/<id>/`  | Delete an offer (author only)                    |
| GET    | `/users/`        | List all users                                   |
| GET    | `/users/<id>/`   | Retrieve a user                                  |

### taskmanager

A task management API based on the tutorial [Building Web APIs with Django Rest Framework: A Beginner's Guide](https://betterstack.com/community/guides/scaling-python/introduction-to-drf/).

**Key Concepts:**
* Model-level validation
* Different serializers for different actions (create, update, read)
* Filtering via query parameters
* Pagination

**API Endpoints:**

| Method | Endpoint             | Description                                          |
|--------|----------------------|------------------------------------------------------|
| GET    | `/api/tasks/`        | List all tasks (supports `?completed=true/false`)    |
| POST   | `/api/tasks/`        | Create a new task                                    |
| GET    | `/api/tasks/<id>/`   | Retrieve a task                                      |
| PUT    | `/api/tasks/<id>/`   | Update a task                                        |
| PATCH  | `/api/tasks/<id>/`   | Partially update a task                              |
| DELETE | `/api/tasks/<id>/`   | Delete a task                                        |

## Development

### Setup

```bash
# Install dependencies
uv sync

# Activate virtual environment (optional, uv run handles this)
source .venv/bin/activate

# Delete cache
find . -type d \( -name '*_cache' -o -name '__pycache__' \) -exec rm -rf {} +
```

### Running an App

```bash
# Run migrations
uv run --directory <project> manage.py migrate

# Start development server
uv run --directory <project> manage.py runserver
```

**Example:**
```bash
uv run --directory taskmanager manage.py migrate
uv run --directory taskmanager manage.py runserver
```

### Running Tests

```bash
# Run tests for a specific app
uv run --directory <project> manage.py test

# Or use the CI script
./.github/run.sh <project>
```

**Example:**
```bash
uv run --directory taskmanager manage.py test
./.github/run.sh taskmanager
```
