#!/bin/bash

set -e
# start envoy
if [ "$APP_PROTOCOL" == "TCP" ]
then
  nohup /opt/binary/envoy --config-path /opt/conf/envoy_config_grpc.yaml --concurrency 2 --disable-hot-restart --log-path /opt/envoy.log &
else
  nohup /opt/binary/envoy --config-path /opt/conf/envoy_config.yaml --concurrency 2 --disable-hot-restart --log-path /opt/envoy.log &
fi

# run app
exec bash ./run.sh
