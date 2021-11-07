# Lampy
To build the needed docker image run in console:
```
docker build -t my_prestashop $PATH_TO_DOCKERFILE
```
In case the dockerfile is in the current working directory, simply run:
```
docker build -t my_prestashop .
```

To run docker-compose:
- install docker for windows
- navigate console to your project directory (docker-compose.yml has to be in that directory)
- type "docker-compose up -d"

Prestashop port: 8080
MySQL port: 3307


To import data from an archive to a database, run this command inside the container with mysql:
```
gunzip < $ARCHIVE_LOCATION | mysql -u root -padmin mysql
```
