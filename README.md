# Lampy

Clone branch:
git clone -b <branch_name> <git_repo>

After clone exec following commands on main on main project folder
sudo chown www-data:root -R ./Lampy
sudo chmod 777 -R ./Lampy
(If you don`t have dos2unix, please install - 'sudo apt-get install dos2unix')
find . -type f -print0 | xargs -0 -n 1 -P 4 dos2unix 
