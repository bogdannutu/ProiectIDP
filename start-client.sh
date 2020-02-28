#!/bin/bash

ip_admin=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' idp_admin)
ip_service=$(docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' idp_service)

docker-compose run -T -e ip_admin=$ip_admin -e ip_service=$ip_service client
