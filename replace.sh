#! /bin/sh

cd /home/ubuntu/alumnus-django/
git pull --rebase origin master
sudo docker build -t alumnus .
sudo docker rm -f $(sudo docker ps -a -q)
sudo docker run -d -p 127.0.0.1:8000:8000 alumnus
