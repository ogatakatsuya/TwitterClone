#!/bin/bash

# Frontend build and start
cd /home/ec2-user/frontend
sudo npm run build
sudo systemctl restart nextjs

# Backend start
cd /home/ec2-user/backend
/home/ec2-user/.local/bin/poetry run python -m api.migrate_db
sudo systemctl restart fastapi
