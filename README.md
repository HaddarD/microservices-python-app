# Cinema 3: A Movie Theater Microservices Project 🎬

Welcome to the **Cinema 3** project!
Here, we bring movie magic to life with microservices powered by Python and Flask. 🍿✨
This project demonstrates how to set up multiple Flask services, load balance with NGINX, and much more!

---

## 🎯 What is Cinema 3?

Cinema 3 is a fictional movie theater system that uses Flask-based microservices
to manage and display movie info, showtimes, bookings, and user recommendations.
It’s a **production-ready** example of how you might deploy a movie-related web application in the real world. 🌍

---

## 🚀 Features

Here’s what this setup does:

- **Movie Service**: Provides movie data (titles, ratings, etc.). 🍿
- **Showtimes Service**: Displays showtimes for each movie. 🎥
- **Booking Service**: Provides bookings and reservation details. 📅
- **Users Service**: Recommends movies to users. 🎬
- **UI Service**: Displays a neat simple dashboard to users with all the movie and booking info. 🖥️

---

## ⚙️ Setup Instructions

To get Cinema 3 up and running, you need to set up your Flask services and NGINX configuration.
Here's how to do it!

1. Clone the Repository

Start by cloning the Cinema 3 project repo:

```bash
git clone git@github.com:HaddarD/microservices-python-app.git
cd microservices-python-app
```

2. Install dependencies:
```bash
make install
```

3. Nginx Configuration\
I highly recommend that you create a backup for your original `nginx.conf` file
```bash
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginxOrg.conf
```
Replace the content of your  `nginx.conf` file with the content of `NginxConfSampleCode.txt` from this repo\
**Make sure you change the location of your `server.crt` and `server.key` in `nginx.conf`**
```bash
sudo nano /etc/nginx/nginx.conf
```

4. Custom HTML
```bash
sudo nano /usr/share/nginx/html/403.html
```
Paste the content of the `403.html` file from this repo:


5. Create an SSL
```bash
openssl genpkey -algorithm RSA -out server.key
openssl req -new -key server.key -out server.csr
openssl x509 -req -in server.csr -signkey server.key -out server.crt
```

6. Running the Services

You have two options to run the services:

Option 1: Run All Services at Once
```bash
make run-all
```

Option 2: Run Services Individually
```bash
make run-movies     # Movies service on port 5001
make run-movies-secondary # Movies service on port 5005 (backend for least connection)
make run-showtimes  # Showtimes service on port 5002
make run-showtimes-secondary # Showtimes service on port 5006 (backup)
make run-bookings   # Bookings service on port 5003
make run-users      # Users service on port 5000
```

To stop all services:
```bash
make stop-all
```

7. NGINX

verify nginx is running smoothly:
```bash
sudo nginx -t
```
Start nginx
```bash
sudo systemctl start nginx
```
Or
```bash
sudo nginx -s reload
```

## Troubleshooting

1. If services fail to start, check if the ports are already in use:
```bash
sudo lsof -i :5000-5006 -i :80 -i :8080 -i :8443
```
* If any port is accupied clear it with:
```bash
sudo fuser -k 5000/tcp 5001/tcp 5002/tcp 5003/tcp 5004/tcp 5005/tcp 5006/tcp 80/tcp 8080/tcp 8443/tcp
```

2. If you can't access the services, verify they're running:
```bash
ps aux | grep "python3 -m services"
```

3. To view service logs, check the terminal where you started the services

## Development Commands

Format code:
```bash
make format
```

Run linter:
```bash
make lint
```

Clean up cache files:
```bash
make clean
```

## Testing the Services

For all the testing commands and browser links follow the instructions in: the [Testing Guide](testing-guide.md)

#### Endpoints:
- `GET /` - Dashboard showing all services status
- `GET /movies` - Browse movie catalog
- `GET /showtimes` - View movie schedules
- `GET /users` - User management
- `GET /bookings/<username>` - View user bookings

### Movie Service
- `GET /movies`: Returns a list of all movies
- `GET /movies/<movieid>`: Returns details for a specific movie

Example response:
```json
{
    "id": "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
    "title": "Creed",
    "director": "Ryan Coogler",
    "rating": 8.8
}
```

### Showtimes Service
- `GET /showtimes`: Returns all showtimes by date
- `GET /showtimes/<date>`: Returns movies playing on a specific date

Example response:
```json
{
    "20151130": [
        "267eedb8-0f5d-42d5-8f43-72426b9fb3e6",
        "7daf7208-be4d-4944-a3ae-c1c2f516f3e6"
    ]
}
```

### Bookings Service
- `GET /bookings`: Returns all bookings
- `GET /bookings/<username>`: Returns bookings for a specific user

Example response:
```json
{
    "chris_rivers": {
        "20151201": [
            "267eedb8-0f5d-42d5-8f43-72426b9fb3e6"
        ]
    }
}
```

### Users Service
- `GET /users`: Returns all users
- `GET /users/<username>`: Returns user details
- `GET /users/<username>/suggested`: Returns movie suggestions

Example response:
```json
{
    "id": "chris_rivers",
    "name": "Chris Rivers",
    "last_active": 1360031010
}
```


## 📁 Project Structure
```
.
├── 403.html
├── database
│   ├── bookings.json
│   ├── movies.json
│   ├── showtimes.json
│   └── users.json
├── diagram.mmd
├── diagram.png
├── docker-compose.yml
├── images
├── makefile
├── NginxConfSampleCode.txt
├── README.md
├── reflection.md
├── requirements.txt
├── screenshots
│   └── dashboard.png
├── server.crt
├── server.csr
├── server.key
├── services
│   ├── bookings.py
│   ├── __init__.py
│   ├── movies.py
│   ├── __pycache__
│   │   ├── bookings.cpython-313.pyc
│   │   ├── __init__.cpython-313.pyc
│   │   ├── movies.cpython-313.pyc
│   │   ├── showtimes.cpython-313.pyc
│   │   ├── ui.cpython-313.pyc
│   │   └── user.cpython-313.pyc
│   ├── showtimes.py
│   ├── static
│   │   └── style.css
│   ├── templates
│   │   ├── base.html
│   │   ├── bookings.html
│   │   ├── error.html
│   │   ├── index.html
│   │   ├── movies.html
│   │   ├── showtimes.html
│   │   └── users.html
│   ├── ui.py
│   └── user.py
├── setup.py
├── testing-guide.md
└── tests
    ├── __pycache__
    │   ├── test_bookings.cpython-313-pytest-8.3.5.pyc
    │   ├── test_movies.cpython-313-pytest-8.3.5.pyc
    │   ├── test_showtimes.cpython-313-pytest-8.3.5.pyc
    │   └── test_user.cpython-313-pytest-8.3.5.pyc
    ├── test_bookings.py
    ├── test_movies.py
    ├── test_showtimes.py
    └── test_user.py

```



## Reflections
[Work Process Reflections](reflection.md)
