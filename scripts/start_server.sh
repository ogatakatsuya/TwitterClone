#!/bin/bash

# Frontend build and start
cd /home/ec2-user/frontend
npm run build

# Backend start
cd /home/ec2-user/backend
poetry run python -m api.migrate_db
