# Lampy

Clone branch: <br />
git clone -b <branch_name> <git_repo>  <br />

After clone exec following commands on main on main project folder  <br />
sudo chown www-data:root -R ./Lampy  <br />
sudo chmod 777 -R ./Lampy  <br />
(If you don't have dos2unix, please install - 'sudo apt-get install dos2unix') <br />
find . -type f -print0 | xargs -0 -n 1 -P 4 dos2unix  <br />

Databse dump might take a while to load, if you want to inspect it you can do following: <br />
docker exec -it <db_container_name> bash <br />
mysql -u root -padmin <br />
use prestashop; <br />
show tables; <br />
At ~283 tables mysql will restart and then presta will be working <br />
