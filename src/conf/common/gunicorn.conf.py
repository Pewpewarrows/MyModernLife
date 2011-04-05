bind = '127.0.0.1:8000'
logfile = '/var/www/mymodernlife/logs/gunicorn.log'
workers = 4
worker_connections = 30
timeout = 60
keepalive = 2