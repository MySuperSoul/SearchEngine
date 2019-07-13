#! /bin/bash
set -u

# service-register
docker run -id --rm --name main --net=host -p 7000:7000 -t main --spring.profiles.active=dev



