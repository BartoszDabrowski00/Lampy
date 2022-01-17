FROM prestashop/prestashop
RUN rm -rf *
COPY src/ ./
RUN chown -R www-data:root -R ./
COPY scripts/ssl /etc/apache2/sites-available
COPY ./php.ini /usr/local/etc/php/php.ini
RUN a2enmod ssl
EXPOSE 80
EXPOSE 443
