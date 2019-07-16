#! /bin/bash
# set -e
set -u

# remove container and images
./stopAndRemove.sh

mvn clean install

mvn package docker:build -Dmaven.test.skip=true




