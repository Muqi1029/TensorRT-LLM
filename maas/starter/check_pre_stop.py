"""ENV IMPLEMENTATION.

MAAS_TERMINATION_GRACE_SECONDS: 30
PRE_STOP_INTERVAL_TIME: 6
"""

import logging
import os
import sys
import time

import requests
from starter.utils import get_dist_init_addr, get_node_nums

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

MAAS_TERMINATION_GRACE_SECONDS_DEFAULT = 30
PRE_STOP_INTERVAL_TIME_DEFAULT = 6


def get_pre_stop_timeout() -> int:
    return int(os.getenv("MAAS_TERMINATION_GRACE_SECONDS", MAAS_TERMINATION_GRACE_SECONDS_DEFAULT))


def get_pre_interval_time() -> int:
    return int(os.getenv("PRE_STOP_INTERVAL_TIME", PRE_STOP_INTERVAL_TIME_DEFAULT))


def run():
    node_nums = get_node_nums()
    if node_nums > 1:
        master_addr = get_dist_init_addr()
    else:
        master_addr = os.getenv("POD_IP", "0.0.0.0")
    port = os.getenv("PORT", "8000")
    url = f"http://{master_addr}:{port}/metrics"
    headers = {"Authorization": os.environ["API_KEY"]} if os.getenv("API_KEY") else None

    pre_stop_timeout = get_pre_stop_timeout()
    pre_stop_interval_time = get_pre_interval_time()
    start_time = time.time()

    try:
        # while loop: waiting for the current engine processing all inflight requests
        while True:
            # 1. set timeout
            elapsed_time = time.time() - start_time
            if elapsed_time > pre_stop_timeout:
                logger.info(f"Timeout: Exceeded maximum waiting time of {pre_stop_timeout} seconds")
                break

            # 2. send a request to the metrics interface of the master node
            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {str(e)}.")
                break

            # 3. process metrics
            metrics_arr = response.json()
            logger.debug(metrics_arr)
            if metrics_arr:
                logger.info(
                    f"Found some inflight requests. Retrying after {pre_stop_interval_time} second..."
                )
                time.sleep(pre_stop_interval_time)
            else:
                logger.info("All requests completed (running and waiting counts are zero)")
                break

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    run()
