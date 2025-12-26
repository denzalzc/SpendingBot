cp nginx.art /etc/nginx/sites-available/spendingBot
nginx -t
systemctl reload nginx
service nginx reload
sudo ln -s /etc/nginx/sites-available/spendingBot /etc/nginx/sites-enabled/
.././venv/bin/python3 manage.py collectstatic
DJANGO_DEBUG=False

systemctl start spendbot
systemctl enable spendbot

systemctl start spendweb
systemctl enable spendweb