#!/bin/bash

PROJECT_DIR="$(dirname "$0")"

COMMAND="cd $PROJECT_DIR && make etl-api"

(crontab -l 2>/dev/null; echo "*/2 * * * * $COMMAND") | crontab -
