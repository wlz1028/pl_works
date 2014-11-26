#!/bin/bash

#install required packages
basedir="$(dirname $0)"
#python modules
apt-get update
apt-get install python-pip
pip install oauth2client
pip install --upgrade google-api-python-client
pip install beaker
pip install pymongo
apt-get install python-numpy
pip install bottle
pip install BeautifulSoup
pip install tornado

#mongodb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
apt-get update
apt-get install -y mongodb-org
#start deamon
service mongod stop
service mongod start

#packages
apt-get install pound

cat > /etc/pound/pound.cfg << '_EOF'
User        "www-data"
Group        "www-data"
LogLevel    1

Alive        30

Control "/var/run/pound/poundctl.socket"

ListenHTTP
    Address 0.0.0.0
    Port    80

    Service
        BackEnd
            Address 127.0.0.1
            Port    8081
        End
        BackEnd
            Address 127.0.0.1
            Port    8082
        End
    End
End
_EOF

echo "startup=1" > /etc/default/pound

/etc/init.d/pound stop
/etc/init.d/pound start

#backEnd autorun(indexing web and save to db)
cd backEnd
python master.py
cd -

#frontEnd online
chmod +x $basedir/frontEnd/master.sh
$basedir/frontEnd/master.sh
exit 1
