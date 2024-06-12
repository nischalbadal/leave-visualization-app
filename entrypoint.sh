#!/bin/bash
set -e

# Apply database migrations
alembic upgrade head

# Execute the command specified as CMD in Dockerfile
exec "$@"
