#!/bin/bash

if [ -x "$(command -v docker-compose)" ]; then
    docker-compose exec pgsql  pg_dump -U bottle bottle_exchange  | gzip -9 > dump.sql.gz
else
    docker compose exec pgsql  pg_dump -U bottle bottle_exchange  | gzip -9 > dump.sql.gz
fi