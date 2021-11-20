FROM prestashop/prestashop

#COPY ./rmscript.sh . 
#RUN chmod 777 rmscript.sh
#RUN ./rmscript.sh

#RUN mkdir /var/www/html
#COPY ./html /var/www/html

#ARG DB_SERVER=some-mysql
#ARG PWD=/var/www/html
#ARG DB_USER=root
#ARG DB_PASSWD=admin
#ARG DB_NAME=prestashop
#ARG DATABASE_PREFIX=ps_
#ARG PS_INSTALL_AUTO=0
#ARG PS_FOLDER_ADMIN=admin1
#ARG PS_DEV_MODE=1
#ARG ADMIN_MAIL=bizneselektronicznylampy@gmail.com
#ARG ADMIN_PASSWD=bizneselektroniczny

#WORKDIR /var/www/html
EXPOSE 80
EXPOSE 443
