#!/usr/bin/env bash

xhost +local:aocutils
docker start aocutils
docker exec -it aocutils /bin/bash