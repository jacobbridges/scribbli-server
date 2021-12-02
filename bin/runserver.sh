export $(grep -v '^#' ../.env | tr -d ' ' | xargs)
poetry run python manage.py runserver