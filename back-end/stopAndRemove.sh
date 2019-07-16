#! /bin/bash
# set -e
set -u

docker container stop main
docker rmi main

