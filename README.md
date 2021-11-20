# Lampy

Clone branch: <br />
git clone -b <branch_name> <git_repo>  <br />

After clone exec following commands on main on main project folder  <br />
sudo chown www-data:root -R ./Lampy  <br />
sudo chmod 777 -R ./Lampy  <br />
(If you don't have dos2unix, please install - 'sudo apt-get install dos2unix') <br />
find . -type f -print0 | xargs -0 -n 1 -P 4 dos2unix  <br />
