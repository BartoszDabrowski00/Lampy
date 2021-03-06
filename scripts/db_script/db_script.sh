#!/bin/bash

DATABASE_NAME="BE_179962_abba"
DATABASE_USER="abba"
DATABASE_PASSWORD="abba"
DATABASE_ROOT_PASSWORD="student"
SHOP_URL="localhost:8090"
SHOP_SSL_URL="localhost:79962"

mysql -p$DATABASE_ROOT_PASSWORD -e "CREATE DATABASE IF NOT EXISTS ${DATABASE_NAME};"
mysql -p$DATABASE_ROOT_PASSWORD -e "CREATE USER IF NOT EXISTS ${DATABASE_USER}@'%' IDENTIFIED BY '${DATABASE_PASSWORD}';"
mysql -p$DATABASE_ROOT_PASSWORD -e "GRANT ALL PRIVILEGES ON ${DATABASE_NAME}.* TO '${DATABASE_USER}'@'%';"
mysql -p$DATABASE_ROOT_PASSWORD -e "FLUSH PRIVILEGES;"
mysql -u $DATABASE_USER -p$DATABASE_PASSWORD $DATABASE_NAME < /tmp/BE_179962_abba.sql

mysql -u $DATABASE_USER -p$DATABASE_PASSWORD $DATABASE_NAME -e "UPDATE ps_shop_url SET domain='${SHOP_URL}', domain_ssl='${SHOP_SSL_URL}' WHERE id_shop_url=1;"
mysql -u $DATABASE_USER -p$DATABASE_PASSWORD $DATABASE_NAME -e "UPDATE ps_homeslider_slides_lang SET url=REPLACE(url, 'localhost', '${SHOP_SSL_URL}');"
mysql -u $DATABASE_USER -p$DATABASE_PASSWORD $DATABASE_NAME -e "UPDATE ps_configuration_lang SET value=REPLACE(value, 'localhost', '${SHOP_SSL_URL}') WHERE id_configuration=434;"

