#!/bin/bash
# Filename: build.sh

. .env
docker build -t $SERVICE_IMAGE_TAG .