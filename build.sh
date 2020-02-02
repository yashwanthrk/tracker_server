#!/bin/sh
# Filename: build.sh

. .env
docker build -t $SERVICE_IMAGE_TAG .