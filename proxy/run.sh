#!/bin/sh

set -e
#把變數替換成環境變數的值, 並輸出檔案
envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf
# start the nginx server
# daemon off: don't run it like a background daemon
# run it in the foreground of the docker container,
# it helps that all of the logs that are output to the application
# get sent straight to the docker logs(helps debugging)
nginx -g 'daemon off;'