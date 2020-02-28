#!/bin/bash

docker-compose run -d --name idp_admin admin
docker-compose run -d --name idp_service service
