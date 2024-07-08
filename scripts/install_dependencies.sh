#!/bin/bash

# Frontend setup
cd /home/ec2-user/frontend
sudo npm install

# Backend setup
cd /home/ec2-user/backend
poetry install
