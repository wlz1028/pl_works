#!/bin/bash

#install required packages
basedir="$(dirname $0)"

#mongodb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
sleep 1
echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
sleep 1
apt-get update
sleep 1
apt-get install -y mongodb-org
sleep 1
#start deamon
service mongod stop
sleep 1
service mongod start
sleep 1

#python modules
apt-get install -y python-pip
sleep 1
pip install oauth2client
sleep 1
pip install --upgrade google-api-python-client
sleep 1
pip install beaker
sleep 1
pip install pymongo
sleep 1
apt-get install -y python-numpy
sleep 1
pip install bottle
sleep 1
pip install BeautifulSoup
sleep 1
pip install tornado
sleep 1


#packages
apt-get install -y pound
sleep 1

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
sleep 1

echo "startup=1" > /etc/default/pound

/etc/init.d/pound stop
sleep 1
/etc/init.d/pound start
sleep 1

ps -a | grep mongo | grep -v mongo

#backEnd autorun(indexing web and save to db)
cd backEnd
python master.py
cd -
sleep 1

#frontEnd online
chmod +x $basedir/frontEnd/master.sh
$basedir/frontEnd/master.sh
exit 1
