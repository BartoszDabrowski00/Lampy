#!/bin/bash

docker cp ./BE_179962_abba.sql admin-mysql_db:/tmp/BE_179962_abba.sql

docker cp ./db_script.sh admin-mysql_db:/tmp/BE_179962_db_script.sh

docker exec admin-mysql_db chmod +x /tmp/BE_179962_db_script.sh

docker exec admin-mysql_db /tmp/BE_179962_db_script.sh

docker exec admin-mysql_db rm /tmp/BE_179962_abba.sql

docker exec admin-mysql_db rm /tmp/BE_179962_db_script.sh
