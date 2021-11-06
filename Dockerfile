FROM prestashop/prestashop

WORKDIR /var/www/html

RUN mv admin admin1
RUN rm -r install
COPY app ./app
COPY config ./config
COPY translations ./translations
COPY modules ./modules

