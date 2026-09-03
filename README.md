# EventHub — Event Ticketing REST API

EventHub is a full-stack event ticketing platform built with Django and Django REST Framework. It provides JWT-based authentication, event management, ticket booking, cancellation, availability protection, and separate user and administrative dashboards.

## Demo

[▶ Watch the EventHub Demo](https://youtu.be/skWITgug3Kk)

## Features

### Authentication

- User registration and login
- JWT access and refresh tokens
- Authenticated profile management
- Protected API endpoints

### Event Management

- Create, view, update, and delete events
- Filter events by category and location
- Search events by text
- Filter upcoming events
- Featured event support

### Ticket Booking

- Book multiple tickets for an event
- Automatic booking total calculation
- Unique booking reference generation
- Booking status tracking
- Cancel bookings and automatically restore ticket availability

### Concurrency-Safe Reservations

Ticket reservations use database transactions and `select_for_update()` to protect ticket inventory and prevent overbooking when multiple booking requests occur simultaneously.

### User Dashboard

- View upcoming and past bookings
- Track booking status
- View booking details
- Cancel bookings

### Admin Dashboard

- Manage events
- Manage bookings
- Monitor users
- View total events and bookings
- Track tickets sold
- Monitor revenue

### Responsive Frontend

- Responsive design for desktop and mobile
- CSS Grid and Flexbox layouts
- Modern UI components
- Vanilla JavaScript with the Fetch API
- No frontend framework required

---

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | Python, Django |
| API | Django REST Framework |
| Authentication | Simple JWT |
| Database | SQLite |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Image Processing | Pillow |

---

## Project Structure

```text
ticket/
├── manage.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── eventhub/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── events/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── tests.py
│
├── bookings/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
│
├── core/
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed_data.py
│
└── frontend/
    ├── templates/
    │   ├── index.html
    │   ├── event.html
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   └── admin_dashboard.html
    │
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            ├── api.js
            ├── home.js
            ├── event.js
            ├── login.js
            ├── register.js
            ├── dashboard.js
            └── admin.js
