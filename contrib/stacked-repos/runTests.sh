#!/bin/bash

set -e
set -x

cd testRepo
../git-stack-resolve
git co master
touch master2.txt && git add master2.txt && git commit -m "master2"
../git-stack-resolve
git co master

cd ..
