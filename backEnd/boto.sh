#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR
git clone git://github.com/boto/boto.git
cd boto

python setup.py install --user

exit 1
