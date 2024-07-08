#!/bin/bash

# Frontend setup
cd /home/ec2-user/frontend
npm install

# Backend setup
cd /home/ec2-user/backend
poetry install
