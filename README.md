# Lampy
## Setting up containers
To run docker-compose:
- install docker for windows
- navigate console to your project directory (docker-compose.yml has to be in that directory)
- type "docker-compose up -d"

Prestashop port: 8080
MySQL port: 3307

## Importing settings
To import data from an archive to a database:
- set up containers
- copy the archive to the container:
```
docker cp mysqldump.sql.gz  lampy_mysql4prestashop_1:/
```
- run this command inside the container with mysql:
```
gunzip < /mysqldump.sql.gz | mysql -u root -padmin mysql
```
