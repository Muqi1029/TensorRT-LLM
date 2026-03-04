import argparse
import os
import signal
import socket
import sys

from ceres.polaris import CeresClient, RegisterInstance


# get local ip
def get_all_ips():
    hostname = socket.gethostname()
    ips = socket.gethostbyname_ex(hostname)[2]
    # 过滤掉回环地址（127.x.x.x）
    valid_ips = [ip for ip in ips if not ip.startswith("127.")]
    return valid_ips


# ceres_config
# domain;namespace
ceres_config = os.environ.get("CERES_CONFIG", "").split(";")
if len(ceres_config) != 2:
    sys.exit(1)
ceres_host = ceres_config[0]
ceres_namespace = ceres_config[1]
ceres_token = os.environ.get("CERES_TOKEN", "")

# service info
service_ip = get_all_ips()[0]
service_port = 9000
service_default_name = f"{os.environ.get('TWL_LABEL_app')}.{os.environ.get('TWL_LABEL_group')}.{os.environ.get('TWL_LABEL_env')}"
service_name = os.environ.get("CERES_SERVICE_NAME", service_default_name)
meta_data = {
    "framework": "SGLang:v0.0.1",  # framework:version
    "source": os.environ.get("CERES_SERVICE_SOURCE", ""),
    "device": os.environ.get("CERES_SERVICE_DEVICE", ""),
}


# register
def register():
    try:
        cc = CeresClient(_host=ceres_host, _token=ceres_token)
        # 注册实例信息
        instance = RegisterInstance(
            namespace=ceres_namespace,
            service=service_name,
            host=service_ip,
            port=service_port,
            metadata=meta_data,
        )
        response = cc.register_instance(instance)
        print(response.__dict__ if instance is not None else None)
    except Exception as e:
        print("request error:", e)
        sys.exit(1)


# deregister
def deregister():
    try:
        cc = CeresClient(_host=ceres_host, _token=ceres_token)
        instance = RegisterInstance(
            namespace=ceres_namespace,
            service=service_name,
            host=service_ip,
            port=service_port,
            metadata=meta_data,
        )
        cc.deregister_instance(instance)
        print("Deregistered successfully.")
    except Exception as e:
        print("request error:", e)
        sys.exit(1)


# Signal handler for graceful shutdown
def signal_handler(sig, frame):
    print(f"Received signal {sig}. Deregistering and exiting...")
    deregister()
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Service registration script")
    parser.add_argument(
        "--mode",
        choices=["register", "heartbeat"],
        required=True,
        help="Choose 'register' for one-time registration or 'heartbeat' for continuous heartbeat",
    )
    args = parser.parse_args()
    if args.mode == "register":
        register()
    elif args.mode == "heartbeat":
        register()
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        print("Service registered. Waiting for signals...")
        # Keep the process running
        signal.pause()
