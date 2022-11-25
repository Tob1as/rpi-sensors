FROM tobi312/php:8.1-fpm-nginx-alpine-slim

RUN install-php-extensions pdo_mysql mysqli

COPY html/ /var/www/html/
