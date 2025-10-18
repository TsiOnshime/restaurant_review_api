# Restaurant Review API

A simple RESTful API for restaurant reviews built with Django and Django REST Framework. Users can register, log in, add reviews for restaurants, and manage their own reviews. A minimal client-side frontend is included for quick testing.

## Features

- User registration and JWT authentication
- Create / Read / Update / Delete reviews (owner-only for edits/deletes)
- Restaurant listing and details
- View all reviews for a specific restaurant
- Minimal JavaScript frontend to interact with the API

## Tech stack

- Python 3.13
- Django 5.x
- Django REST Framework
- djangorestframework-simplejwt (JWT auth)
- SQLite (development) — db.sqlite3 in repo
- Optional: django-cors-headers (if serving frontend from a different origin)

## Repository layout

```
restaurant_review_api/
├── manage.py
├── db.sqlite3
├── Readme.md
├── requirements.txt
├── restaurant_review_api/        # project settings
│   ├── settings.py
│   └── urls.py
├── restaurants/                  # restaurant app
│   └── ...
├── reviews/                      # review app
│   └── ...
├── templates/                    # frontend templates (index.html)
└── static/                       # frontend static (css/js)
```

## Quick start (local)

1. Clone
```sh
git clone https://github.com/TsiOnshime/restaurant_review_api.git
cd restaurant_review_api/restaurant_review_api
```

2. Create virtualenv and install
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Migrate and create admin user
```sh
python manage.py migrate
python manage.py createsuperuser
```

4. Run server
```sh
python manage.py runserver
```

5. Open
- Frontend: http://127.0.0.1:8000/
- API root (DRF router): http://127.0.0.1:8000/api/
- Admin: http://127.0.0.1:8000/admin/

## API endpoints (main)

- POST /api/auth/token/ — Obtain JWT (username & password)
- POST /api/auth/token/refresh/ — Refresh JWT
- GET /api/restaurants/ — List restaurants
- POST /api/restaurants/ — Create restaurant (see permissions)
- GET /api/restaurants/{id}/ — Restaurant details
- GET /api/restaurants/{id}/reviews/ — Reviews for a restaurant
- GET /api/reviews/ — List reviews
- POST /api/reviews/ — Create review (authenticated)
- GET /api/reviews/{id}/ — Review detail
- PUT/PATCH /api/reviews/{id}/ — Update review (owner-only)
- DELETE /api/reviews/{id}/ — Delete review (owner-only)

## Frontend (included)

- Templates: `templates/index.html`
- Static JS/CSS: `static/js/app.js`, `static/css/styles.css`
- The frontend uses the token endpoint `/api/auth/token/` to log in and stores the access token in localStorage. If serving frontend from a separate origin, enable CORS (`django-cors-headers`).

## Add data

- Admin UI (recommended): /admin — add Restaurants and manage data.
- Shell:
```sh
python manage.py shell
```
```py
from restaurants.models import Restaurant
Restaurant.objects.create(name="Injera", address="Addis Ababa", description="Hager bet")
```

- API (curl example):
```sh
curl -X POST http://127.0.0.1:8000/api/restaurants/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"My Cafe","address":"123 Main St","description":"Cozy spot"}'
```

## Testing

Run Django tests:
```sh
python manage.py test
```

## Notes / next steps

- Ensure serializer field names match the Review model (content vs comment). Update `reviews/serializers.py` and `static/js/app.js` to use the same field.
- For production: switch to PostgreSQL, set DEBUG=False, and manage SECRET_KEY via environment variables.
- Consider adding a registration endpoint and more unit tests.

## Contributing

Fork, create a branch, commit changes, and open a pull request. Keep changes focused and include tests when possible.

## License

MIT

## Author

Tsion Shimelis