# Microservices Project Make File
# author: dor-amar

.PHONY: install test run clean

install:
	python3 -m pip install --upgrade pip
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest tests/

run-movies:
	python3 -m services.movies

# Additional movies instance on port 5005
run-movies-secondary:
	PORT=5005 python3 -m services.movies

run-showtimes:
	python3 -m services.showtimes

# Additional showtimes instance on port 5006
run-showtimes-secondary:
	PORT=5006 python3 -m services.showtimes

run-bookings:
	python3 -m services.bookings

run-user:
	python3 -m services.user

run-ui:
	python3 -m services.ui

# New command for running all services including secondary instances
run-all:
	python3 -m services.movies & \
	PORT=5005 python3 -m services.movies & \
	python3 -m services.showtimes & \
	PORT=5006 python3 -m services.showtimes & \
	python3 -m services.bookings & \
	python3 -m services.user & \
	python3 -m services.ui

stop-all:
	pkill -f "python3 -m services"

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

format:
	black services/ tests/

lint:
	flake8 services/ tests/

