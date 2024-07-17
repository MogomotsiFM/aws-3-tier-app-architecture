#!/bin/bash
# Commands to build a golden AMI
dnf install python3.11 -y
dnf install python3.11-pip -y
python3.11 -m pip install fastapi
python3.11 -m pip install "uvicorn[standard]" gunicorn