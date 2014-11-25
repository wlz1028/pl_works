#!/bin/bash

#install required packages
#python modules
apt-get install python-pip
pip install oauth2client
pip install --upgrade google-api-python-client
pip install beaker
pip install pymongo
sudo apt-get install python-numpy
pip install bottle
pip install BeautifulSoup
pip install tornado

#mongodb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sudo apt-get update
sudo apt-get install -y mongodb-org
#start deamon
sudo service mongod start

#packages
sudo apt-get install pound

#backEnd autorun(indexing web and save to db)
python ./backEnd/master.py

#frontEnd online

