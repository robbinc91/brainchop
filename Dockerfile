FROM nginx
COPY . /usr/share/nginx/html

FROM apache
COPY . /var/www/html