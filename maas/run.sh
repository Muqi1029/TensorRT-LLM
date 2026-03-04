#!/bin/bash
set -e

echo 'START ARSENAL SERVER'
python3 ./starter/cmd_generator_openai.py
chmod +x starter/start_cmd.sh
nohup ./starter/start_cmd.sh > /dev/stdout 2>&1 &
SERVER_PID=$!

trap 'handle_signal' SIGTERM SIGINT

handle_signal() {
  echo "$(date +'%Y-%m-%d %H:%M:%S') - Received termination signal. Sending SIGTERM"
  # 向 start_cmd.sh 进程发送 SIGTERM 信号
  kill -TERM $SERVER_PID
  # 等待 start_cmd.sh 进程结束
  echo "Waiting server to be killed"
  wait $SERVER_PID
  exit 0
}

echo "Waiting for port 8000 to be ready..."
while ! curl -s 0.0.0.0:8000 > /dev/null; do
  sleep 1
done

# do register
if [ -n "$CERES_CONFIG" ]; then
  python3 register.py --mode register
  if [ $? -ne 0 ]; then
    echo "Failed to register. Exiting..."
    exit 1
  fi
  nohup python3 register.py --mode heartbeat > /dev/stdout 2>&1 &
fi

wait $SERVER_PID
