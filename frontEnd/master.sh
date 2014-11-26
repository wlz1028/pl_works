#!/bin/bash

basedir="$(dirname $0)"
cd $basedir
echo "Deploy first bottle on port 8081"
`nohup python frontEnd.py 8081 &> server_8081.log &`
echo "Deploy first bottle on port 8082"
`nohup python frontEnd.py 8082 &> server_8082.log &`
