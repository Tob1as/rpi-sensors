FROM tobi312/php:8.4-fpm-nginx-alpine-slim

RUN install-php-extensions pdo_mysql mysqli

COPY html/ /var/www/html/
