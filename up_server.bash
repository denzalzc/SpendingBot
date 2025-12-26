# remove old nginx sets
rm /etc/nginx/sites-availabl/spendignBot
rm /etc/nginx/sites-enabled/spendignBot

# stop old services
systemctl stop spendweb
systemctl stop spendbot

#remove old services
rm /etc/systemd/system/spendbot.service
rm /etc/systemd/system/spendweb.service

# create services
cp spendbot.service /etc/systemd/system/spendbot.service
cp spendweb.service /etc/systemd/system/spendweb.service

# copy apikey for TG bot
cp /home/apikey.txt /home/spendingBot/Bot/apikey.txt

# create nginx set for site
cp nginx.art /etc/nginx/sites-available/spendingBot

# create link for as enabled site
sudo ln -s /etc/nginx/sites-available/spendingBot /etc/nginx/sites-enabled/

# reload nginx
nginx -t
systemctl reload nginx
service nginx reload

# prepare to deploy
venv/bin/python3 WebApp/SpendWeb/manage.py collectstatic
DJANGO_DEBUG=False

# start-deploy
systemctl start spendbot
systemctl enable spendbot

systemctl start spendweb
systemctl enable spendweb

# checks
systemctl status spendweb
systemctl status spendbot