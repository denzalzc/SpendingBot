cp nginx.art /etc/nginx/sites-available/codesworld
nginx -t
systemctl reload nginx
service nginx reload
sudo ln -s /etc/nginx/sites-available/codesworld /etc/nginx/sites-enabled/
.././venv/bin/python3 manage.py collectstatic
DJANGO_DEBUG=False
.././venv/bin/python3 .././venv/bin/gunicorn --bind 127.0.0.1 codesworld.wsgi:application