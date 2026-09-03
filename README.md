# 🎫 EventHub — Event Ticketing REST API & Web Platform

**EventHub** is a production-style, full-stack **Event Ticketing REST API** and interactive web interface built with **Django**, **Django REST Framework (DRF)**, **Simple JWT**, and modern **Vanilla HTML5/CSS3/JavaScript**.

Designed as an architecture-grade school project, it balances clean code structure, concurrency-safe business logic, and a professional visual presentation.

---

## 🌟 Key Features

* **JWT Authentication**: User registration, login with JWT tokens, token refresh, and user profile management.
* **Event Management (CRUD)**: Full event creation, reading, editing, and deletion with category/location filtering, text search, and featured event highlighting.
* **Ticket Booking & Concurrency Protection**: Atomic ticket reservations using `select_for_update()` database transactions to guarantee ticket availability integrity and prevent overbooking.
* **Unique Booking References**: Automatic generation of unique alphanumeric booking codes (e.g. `EVT-8F4K29`).
* **Ticket Returns on Cancellation**: Returning tickets to the event pool automatically upon booking cancellation.
* **Dual Dashboard Interface**:
  * **User Dashboard**: Track upcoming and past event tickets with status indicators and cancellation options.
  * **Admin Dashboard**: System-wide metrics (total events, bookings, revenue, tickets sold) and live event/booking management.
* **Responsive Modern UI**: Built from scratch using standard CSS Custom Properties, modern typography, glassmorphism, responsive grid layouts, and zero heavy JS frameworks.

---

## 🛠️ Technology Stack

* **Backend**: Python 3, Django 6, Django REST Framework (DRF)
* **Authentication**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
* **Database**: SQLite 3 with Django ORM
* **Frontend**: HTML5, CSS3 (Modern Flexbox/Grid), Vanilla JavaScript (ES6+ Fetch API)
* **Image Processing**: Pillow

---

## 📁 Project Architecture

```text
ticket/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── eventhub/                   # Django Project Core Configuration
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                   # User Authentication App
│   ├── models.py               # Custom User model (Email-based)
│   ├── serializers.py          # Register, Login, Profile serializers
│   ├── views.py                # JWT Auth & Profile views
│   ├── urls.py                 # /api/auth/ routes
│   └── tests.py                # Auth API tests
│
├── events/                     # Event Management App
│   ├── models.py               # Event model with category & ticket tracking
│   ├── serializers.py          # List & Detail serializers
│   ├── views.py                # Event ViewSet (Filtering & Search)
│   ├── permissions.py          # IsAdminOrReadOnly permission
│   ├── urls.py                 # /api/events/ routes
│   └── tests.py                # Event API tests
│
├── bookings/                   # Ticket Booking App
│   ├── models.py               # Booking model & reference generator
│   ├── serializers.py          # Booking serializers & validation
│   ├── views.py                # Atomic Booking creation & cancellation
│   ├── urls.py                 # /api/bookings/ routes
│   └── tests.py                # Concurrency & Booking unit tests
│
├── core/                       # Admin Metrics & Seed Utilities
│   ├── views.py                # Admin dashboard statistics API
│   ├── urls.py                 # /api/stats/ route
│   └── management/
│       └── commands/
│           └── seed_data.py    # Database seeder command
│
└── frontend/                   # Web Interface (Served by Django)
    ├── templates/              # HTML Pages
    │   ├── index.html          # Home & Event Discovery
    │   ├── event.html          # Event Details & Booking
    │   ├── login.html          # Auth Login
    │   ├── register.html       # Auth Register
    │   ├── dashboard.html      # User Tickets Dashboard
    │   └── admin_dashboard.html# Admin Management Dashboard
    └── static/
        ├── css/
        │   └── style.css       # Complete Design System
        └── js/
            ├── api.js          # Fetch API wrapper & Token Manager
            ├── home.js         # Event Discovery Script
            ├── event.js        # Ticket Selection & Booking Script
            ├── login.js        # Auth Login Handler
            ├── register.js     # Auth Registration Handler
            ├── dashboard.js    # User Tickets Script
            └── admin.js        # Admin Dashboard Script
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** installed on your system.

### 2. Installation
Clone or open the repository folder:

```bash
cd ticket
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Database Setup & Seeding

Apply database migrations:

```bash
python manage.py migrate
```

Populate the database with realistic demo events and pre-configured accounts:

```bash
python manage.py seed_data
```

### 4. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Credentials

| Role | Email | Password | Access Level |
| :--- | :--- | :--- | :--- |
| **Admin / Staff** | `admin@example.com` | `Admin123!` | Full CRUD, Admin Dashboard, All Bookings |
| **Regular User** | `user@example.com` | `User123!` | Browse, Book Tickets, Cancel Own Tickets |

*Note: The login page includes quick-fill buttons for fast testing.*

---

## 🎓 School Presentation Demonstration Walkthrough

When presenting to your instructor or class, follow this 10-step demonstration flow:

1. **Browse Events** (`http://127.0.0.1:8000/`): Filter events by category (e.g., Technology, Concerts) or use the search bar.
2. **Log In**: Click "Log In" and select the quick-fill **User** button (`user@example.com`).
3. **Open Event**: Click "View Event" on *Lagos Tech Conference 2026*. Note the available ticket count (e.g. `500`).
4. **Select & Book**: Increase ticket quantity to `3` and click **Book Tickets**.
5. **Receive Reference**: Instant modal pops up displaying the unique reference code (e.g. `EVT-8F4K29`).
6. **Verify Inventory Deduction**: Close modal or refresh page to observe `available_tickets` decreased to `497`.
7. **View User Dashboard**: Click **My Tickets**. See the newly booked ticket listed under *Upcoming*.
8. **Test Overbooking Guard**: Try booking more tickets than available for a low-quantity event — the API will block the transaction with a `400 Bad Request`.
9. **Cancel Booking**: In **My Tickets**, click **Cancel**. Confirm cancellation.
10. **Verify Inventory Restoration**: Return to the event page — available tickets incremented back by `3`.

---

## 🔌 REST API Endpoints & Reference

### 🔐 Authentication (`/api/auth/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/auth/register/` | Register a new user | ❌ No |
| `POST` | `/api/auth/login/` | Obtain access & refresh JWT tokens | ❌ No |
| `POST` | `/api/auth/token/refresh/` | Renew access token using refresh token | ❌ No |
| `GET` | `/api/auth/profile/` | View current authenticated user profile | ✅ Yes |
| `PATCH` | `/api/auth/profile/` | Update profile details | ✅ Yes |

#### Sample Registration Request:
```json
POST /api/auth/register/
{
  "email": "student@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "password": "Password123!",
  "password2": "Password123!"
}
```

#### Sample Registration Response (`201 Created`):
```json
{
  "message": "Account created successfully.",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6...",
  "user": {
    "id": 3,
    "email": "student@example.com",
    "full_name": "Jane Doe",
    "is_staff": false
  }
}
```

---

### 🎪 Events (`/api/events/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/events/` | List events (supports `?category=`, `?search=`, `?upcoming=true`, `?location=`) | ❌ No |
| `POST` | `/api/events/` | Create a new event | 👮 Admin Only |
| `GET` | `/api/events/<id>/` | Retrieve event details | ❌ No |
| `PATCH` | `/api/events/<id>/` | Update event details | 👮 Admin Only |
| `DELETE` | `/api/events/<id>/` | Delete an event | 👮 Admin Only |
| `GET` | `/api/events/categories/` | List all event categories | ❌ No |

---

### 🎫 Bookings (`/api/bookings/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/bookings/` | List user bookings (Admins see all bookings) | ✅ Yes |
| `POST` | `/api/bookings/` | Create a new ticket booking | ✅ Yes |
| `GET` | `/api/bookings/<id>/` | Retrieve booking details | ✅ Yes |
| `DELETE`| `/api/bookings/<id>/` | Cancel booking (restores tickets) | ✅ Yes |

#### Sample Booking Request:
```json
POST /api/bookings/
Header: Authorization: Bearer <access_token>
{
  "event": 1,
  "quantity": 2
}
```

#### Sample Booking Response (`201 Created`):
```json
{
  "id": 1,
  "booking_reference": "EVT-8F4K29",
  "event": 1,
  "event_title": "Lagos Tech Conference 2026",
  "event_date": "2026-09-15",
  "event_location": "Eko Convention Centre, Lagos",
  "event_category": "technology",
  "quantity": 2,
  "total_price": 10000.0,
  "status": "confirmed",
  "status_display": "Confirmed",
  "booking_date": "2026-08-31T10:30:00Z"
}
```

---

### 📊 Admin Analytics (`/api/stats/`)

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/stats/` | Retrieve system analytics (Total events, bookings, users, tickets sold, revenue) | 👮 Admin Only |

---

## 🧪 Automated Testing

To run the automated unit and integration tests:

```bash
python manage.py test
```

### Test Suite Covers:
1. User registration & JWT token generation
2. User login authentication
3. Public event list & detail retrieval
4. Admin-only event creation permissions
5. Ticket availability decrementing upon successful booking
6. Overbooking protection (rejection of requests exceeding remaining tickets)
7. Ticket restoration to event pool upon cancellation
8. Authorization boundaries (preventing users from modifying others' bookings)

---

## 📄 License
This project is open-source and intended for academic and learning purposes.
"# ticket_proj" 
