FROM tobi312/php:8.0-fpm-nginx-alpine-slim-arm

RUN install-php-extensions pdo_mysql mysqli

COPY html/ /var/www/html/
