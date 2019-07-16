#! /bin/bash
set -u

# service-register
docker run -id --rm --name main --net=host -p 9999:9999 -t main --spring.profiles.active=dev



