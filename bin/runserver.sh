export $(grep -v '^#' ../.env | tr -d ' ' | xargs)
export LD_LIBRARY_PATH="/usr/local/lib/"
poetry run python manage.py runserver 127.0.0.1:8000
