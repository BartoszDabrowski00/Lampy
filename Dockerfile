FROM prestashop/prestashop
COPY ./php.ini /usr/local/etc/php/php.ini
RUN a2enmod ssl
EXPOSE 80
EXPOSE 443
