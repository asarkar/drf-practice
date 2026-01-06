# DRF Practice

This repository contains practice code for various Django REST Framework applications.

[![](https://github.com/asarkar/drf-practice/workflows/CI/badge.svg)](https://github.com/asarkar/drf-practice/actions)

## Projects

### quiz-api

A Quiz API based on the [Django REST Framework Quiz API](https://youtu.be/8QLCaye3YjQ) YouTube tutorial.

**Key concepts:**
* Generic class-based views
* Nested serializers for related objects
* Translation
* Edit models on the same page as a parent model (`InlineModelAdmin` objects)

## API Endpoints

| Method | Endpoint           | Description                           |
|--------|--------------------|---------------------------------------|
| GET    | `/quiz/`           | List all quizzes                      |
| GET    | `/quiz/r/<topic>/` | Retrieve a random question for a quiz |
| GET    | `/quiz/q/<topic>/` | Retrieve all questions for a quiz     |

### rental

A rental platform API based on the tutorial [Building APIs With Django REST Framework](https://www.jetbrains.com/help/pycharm/building-apis-with-django-rest-framework.html).

**Key concepts:**
* Generic class-based views
* Nested serializers for related objects
* User authentication and authorization
* Custom permissions

### taskmanager

A task management API based on the tutorial [Building Web APIs with Django Rest Framework: A Beginner's Guide](https://betterstack.com/community/guides/scaling-python/introduction-to-drf/).

**Key concepts:**
* Model-level validation
* Different serializers for different actions (create, update, read)
* Filtering via query parameters
* Pagination

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
