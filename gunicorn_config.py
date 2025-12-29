# gunicorn_config.py
workers = 4
worker_class = 'uvicorn.workers.UvicornWorker'
timeout = 120
keepalive = 5
bind = '0.0.0.0:8000'
