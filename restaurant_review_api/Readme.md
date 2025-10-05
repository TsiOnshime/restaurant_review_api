# Restaurant Review API

A RESTful API for a restaurant review system built with Django and Django REST Framework. Users can register, log in, add reviews for restaurants, and manage their own reviews.

## Features

- **User Management:** Registration, authentication, and profile management.
- **Review Management:** Create, read, update, and delete reviews. Each review is linked to a user and a restaurant.
- **Restaurant Data:** View all restaurants and all reviews for a specific restaurant.
- **Data Validation:** Ensures submitted data is valid and correctly formatted.
- **Security:** Secure password hashing and token-based authentication.

## Technologies

- Django 5.x
- Django REST Framework
- PostgreSQL (for production)
- SQLite (for development)
- Python 3.13

## Project Structure

```
restaurant_review_api/
├── manage.py
├── db.sqlite3
├── restaurant_review_api/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
├── restaurants/
│   ├── models.py
│   ├── views.py
│   └── ...
├── reviews/
│   ├── models.py
│   ├── views.py
│   └── ...
```

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/restaurant_review_api.git
   cd restaurant_review_api
   ```

2. **Install dependencies:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

4. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

### User Endpoints
- `POST /api/users/register/` — Register a new user
- `POST /api/users/login/` — Authenticate and get a token
- `GET /api/users/me/` — Get current user profile
- `PUT/PATCH /api/users/me/` — Update user profile

### Review Endpoints
- `GET /api/reviews/` — List all reviews
- `POST /api/reviews/` — Create a review
- `GET /api/reviews/<id>/` — Retrieve a review
- `PUT/PATCH /api/reviews/<id>/` — Update a review
- `DELETE /api/reviews/<id>/` — Delete a review

### Restaurant Endpoints
- `GET /api/restaurants/` — List all restaurants
- `POST /api/restaurants/` — Create a restaurant (admin only)
- `GET /api/restaurants/<id>/` — Retrieve a restaurant
- `GET /api/restaurants/<id>/reviews/` — List reviews for a restaurant

## Contributing

Pull requests are welcome! Please open an issue first to discuss changes.

## License

This project is licensed under the MIT License.

## Author

Tsion Shimelis 