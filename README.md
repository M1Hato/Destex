# Destex API

Destex is a task management REST API built with FastAPI.
The project demonstrates a production-style backend architecture with secure authentication, database integration, migrations, testing, and containerization.
Destex is designed to help manage tasks and workflows efficiently and showcases modern Python backend development practices.

## 📌 About the project

Destex provides a structured workflow for managing personal tasks and projects.
It allows users to create, update, and organize tasks with priorities and deadlines, apply role-based access control, and maintain modular, maintainable code.

The project demonstrates backend development skills including:

* **REST API design**

* **JWT-based authentication**

* **Database integration and migrations with Alembic**

* **Unit testing with pytest**

* **Dockerized deployment**

Destex is as a portfolio project to showcase Python backend skills and knowledge of production-ready API development.

## 🚀 Features

* User registration and authentication (JWT)

* Task CRUD operations

* Task priorities and deadlines

* Filtering and pagination

* Soft delete for tasks

* Database migrations with Alembic

* API documentation with Swagger

* Unit testing with pytest

* Docker support

## 🧱 Tech Stack

* **Python**
* **FastAPI**
* **PostgreSQL**
* **SQLAlchemy**
* **Alembic**
* **Pydantic**
* **JWT Authentication**
* **Docker**
* **Pytest**


## 📂 Project Structure

```
Destex
│
├── app
│   ├── api
│   │   ├── routers
│   ├── core
│   ├── models
│   ├── repositories
│   ├── schemas
│   ├── services
│   ├── utils
│   ├── config.py
│   ├── database.py
│   ├── logging.py
│   └── main.py
│
├── tests
│   ├── integration
│   ├── unit
│   └── conftest.py
│
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

## ⚙️ Installation
Installation instructions will be added soon.
