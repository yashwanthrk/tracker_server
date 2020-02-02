#!/bin/sh
# Filename: start.sh

. .env

# removes the container when docker stop or crashes
# docker run --rm -it -p 5000:${port}  -v ${PWD}:/usr/src/app --name  operation-services-build ${image} 
if [[ $(docker ps -a | grep $SERVICE_NAME) != "" ]]; then
  docker rm -f $SERVICE_NAME
fi


docker run  -it -d -p $FLASK_EXPOSED_PORT:5000 \
  -v ${PWD}:/usr/src/app --restart $RESTART \
  --log-opt max-size=$LOG_FILE_MAX_SIZE --log-opt max-file=$LOG_FILE_MAX_FILE \
  --name $SERVICE_NAME $SERVICE_IMAGE_TAG python3 $FLASK_FILE_NAME