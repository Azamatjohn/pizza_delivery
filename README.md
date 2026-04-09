# 🍕 Pizza Delivery — Backend API

A RESTful backend API for a pizza delivery service, built with FastAPI. Covers user authentication, product management, and order handling with a clean, modular route structure.

---

## 🚀 Features

- **User authentication** — register, login, JWT-based access control
- **Product management** — full CRUD for pizza menu items
- **Order management** — place, view, update, and delete orders
- **Pydantic v2 schemas** — strict request/response validation
- **Modular routing** — auth, products, and orders in separate route files
- **Auto-generated API docs** — interactive Swagger UI at `/docs`

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI 0.121 |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Auth | JWT |
| Database | PostgreSQL (SQLAlchemy) |
| Config | python-decouple |

---

## 📁 Project Structure

```
pizza_delivery/
├── main.py            # App entry point, router registration
├── auth_routes.py     # Register & login endpoints
├── order_routes.py    # Order CRUD endpoints
├── product_routes.py  # Product/menu CRUD endpoints
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic request/response schemas
├── database.py        # Database connection & session
├── init_db.py         # Database initialization
├── test_main.http     # HTTP request tests
└── requirements.txt   # Dependencies
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Azamatjohn/pizza_delivery.git
cd pizza_delivery
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/delivery_db
```

### 5. Initialize the database
```bash
python init_db.py
```

### 6. Start the server
```bash
uvicorn main:app --reload
```

The API will be running at `http://localhost:8000`
Interactive docs available at `http://localhost:8000/docs`

---

## 🔑 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and receive JWT token |

### Products
| Method | Endpoint | Description |
|---|---|---|
| GET | `/products/` | List all products |
| POST | `/products/` | Create a product |
| GET | `/products/{id}` | Get a product |
| PUT | `/products/{id}` | Update a product |
| DELETE | `/products/{id}` | Delete a product |

### Orders
| Method | Endpoint | Description |
|---|---|---|
| GET | `/orders/` | List all orders |
| POST | `/orders/` | Place a new order |
| GET | `/orders/{id}` | Get an order |
| PUT | `/orders/{id}` | Update an order |
| DELETE | `/orders/{id}` | Delete an order |

---

## 🔐 Authentication

Protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## 👤 Author

**Azamatjon Abdulazizov**
- LinkedIn: [azamatjon-abdulazizov](https://linkedin.com/in/azamatjon-abdulazizov)
- GitHub: [@Azamatjohn](https://github.com/Azamatjohn)
- Email: abdulazizovjohn@gmail.com
