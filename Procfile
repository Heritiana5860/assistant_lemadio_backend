# web: ./.venv/bin/gunicorn app:app --bind 0.0.0.0:$PORT
# web: python -m gunicorn app:app --bind 0.0.0.0:$PORT

# web:: gunicorn app_lc:app 

web: gunicorn app_lc:app --workers 1 --bind 0.0.0.0:$PORT