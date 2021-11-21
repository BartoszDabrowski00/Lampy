FROM prestashop/prestashop
RUN a2enmod ssl
EXPOSE 80
EXPOSE 443
