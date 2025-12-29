# gunicorn_config.py
workers = 4
timeout = 120
keepalive = 5
bind = '0.0.0.0:8000'
