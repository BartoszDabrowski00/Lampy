FROM prestashop/prestashop

RUN mkdir ssl
COPY scripts/ssl/ssl_config.txt ./ssl
COPY scripts/ssl/apache-key.key /etc/ssl/private/
COPY scripts/ssl/apache-cert.crt /etc/ssl/certs/
RUN cat ./ssl/ssl_config.txt > /etc/apache2/sites-available/000-default.conf
RUN a2enmod ssl

WORKDIR /var/www/html

RUN mv admin admin1
RUN rm -r install

COPY app ./app
COPY config ./config
COPY translations ./translations
COPY modules ./modules

EXPOSE 80
EXPOSE 443

