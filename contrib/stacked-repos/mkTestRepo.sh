#!/bin/bash

set -e
set -x

rm -rf testRepo
mkdir testRepo
cd testRepo
git init .

# Create branches
touch master.txt && git add master.txt && git commit -m "master1"
echo 'foo' >>master.txt && git add master.txt && git commit -m "master2"
echo 'bar' >>master.txt && git add master.txt && git commit -m "master3"

git co master^^ && git co -b branch1
touch branch1.txt && git add branch1.txt && git commit -m "branch1"

git co -b branch2
touch branch2.txt && git add branch2.txt && git commit -m "branch2"

git co branch1 && git co -b branch3
touch branch3.txt && git add branch3.txt && git commit -m "branch3"

git co branch3 && git co -b branch4
touch branch4.txt && git add branch4.txt && git commit -m "branch4"

git co branch2 && git co -b branch5
touch branch5.txt && git add branch5.txt && git commit -m "branch5"

git co master^^ && git co -b branch6
touch branch6.txt && git add branch6.txt && git commit -m "branch6"

git co branch6 && git co -b branch7
touch branch7.txt && git add branch7.txt && git commit -m "branch7"

git co master


# Set up tags
../git-stack-follow-branch branch1 master
../git-stack-follow-branch branch2 branch1
../git-stack-follow-branch branch3 branch1
../git-stack-follow-branch branch4 branch3
../git-stack-follow-branch branch5 branch2
../git-stack-follow-branch branch6 master
../git-stack-follow-branch branch7 branch6


cd ..
