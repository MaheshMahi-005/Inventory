# Inventory API

A REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL** for managing products, categories, and user authentication.

## Features

- User authentication (JWT-based)
- Category management (create, list)
- Product management (CRUD)
- MySQL database integration via SQLAlchemy ORM

## Tech Stack

- **Backend Framework:** FastAPI
- **Database:** MySQL
- **ORM:** SQLAlchemy
- **Auth:** JWT (python-jose) + bcrypt
- **Language:** Python 3.x

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- [Python 3.10+](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/downloads/mysql/)
- [Git](https://git-scm.com/downloads)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/MaheshMahi-005/Product_Inventory.git
cd Product_Inventory
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **Windows (PowerShell):**
  ```bash
  venv\Scripts\activate
  ```
- **Windows (Git Bash):**
  ```bash
  source venv/Scripts/activate
  ```

### 3. Install dependencies

All required packages are listed in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a MySQL database for the project, then update your database connection details in `database.py` (or in a `.env` file if you're using one).

Example `.env` (not committed to GitHub):
```
DATABASE_URL=mysql+pymysql://username:password@localhost/db_name
SECRET_KEY=your_secret_key
```

### 5. Run the application

```bash
uvicorn main:app --reload
```

The API will be available like this:
```
http://127.0.0.1:8000
```

Interactive API docs (Swagger UI):
-- add /docs at end of the url
```
http://127.0.0.1:8000/docs
```

## Project Structure

```
Product_Inventory/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── categories.py
│   └── products.py
├── requirements.txt
└── .gitignore
```

## API Endpoints

| Method | Endpoint            | Description             |
|--------|----------------------|--------------------------|
| GET    | `/categories`        | Get all categories      |
| POST   | `/categories`        | Create a new category   |
| GET    | `/products`          | Get all products        |
| POST   | `/products`          | Create a new product    |
| PUT    | `/products\{id}`     | update all product by id|
| DELETE | `/products\{id}`     | Delete  product by id   |
| POST   | `/auth/register`     | Register a new user     |
| POST   | `/auth/login`        | Login and get JWT token |


## Screenshots
<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/22ea9e19-e8c2-47bd-a91c-ea621413787b" />

<img width="1366" height="768" alt="image" src="https://github.com/user-attachments/assets/c59f43fe-3b75-45fc-8552-534ddcb68e80" />



## Author

**Mahesh Chandra **
GitHub: [@MaheshMahi-005](https://github.com/MaheshMahi-005)
