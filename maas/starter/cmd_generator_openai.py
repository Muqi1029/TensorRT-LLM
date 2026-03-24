import os
from pathlib import Path

import torch
import yaml

# constants
SHELL_FILE_DIR = Path("/app/starter")
os.makedirs(SHELL_FILE_DIR, exist_ok=True)
SHELL_FILE_PATH = os.path.join(SHELL_FILE_DIR, "start_cmd.sh")
EXTRA_YAML_PATH = os.path.join(SHELL_FILE_DIR, "trtllm.yaml")
PREFIX = "TRTLLM__"
# hardcode here since trtllm uses click command parser
extra_llm_api_options = {}
serve_options = [
    "tokenizer",
    "custom_tokenizer",
    "host",
    "port",
    "backend",
    "custom_module_dirs",
    "log_level",
    "max_beam_width",
    "max_batch_size",
    "max_num_tokens",
    "max_seq_len",
    "tp_size",
    "pp_size",
    "cp_size",
    "ep_size",
    "cluster_size",
    "gpus_per_node",
    "free_gpu_memory_fraction",
    "kv_cache_free_gpu_memory_fraction",
    "kv_cache_dtype",
    "num_postprocess_workers",
    "trust_remote_code",
    "revision",
    "extra_llm_api_options",
    "reasoning_parser",
    "tool_parser",
    "metadata_server_config_file",
    "server_role",
    "fail_fast_on_attention_window_too_large",
    "otlp_traces_endpoint",
    "disagg_cluster_uri",
    "enable_chunked_prefill",
    "media_io_kwargs",
    "video_pruning_rate",
    "chat_template",
    "grpc",
    "served_model_name",
]


def get_device_count():
    if not torch.cuda.is_available():
        raise Exception("No GPU Found!")
    return torch.cuda.device_count()


ARSENAL_DEFAULT_ARGS = {
    "host": "0.0.0.0",
    "port": 8000,
    "tp_size": get_device_count(),
    "log_level": "verbose",
}


def title_print(title: str):
    print("\n\n" + f" {title} ".center(80, "=") + "\n")


def get_from_env(field_name: str):
    # env_name: MODEL_PATH TP_SIZE
    env_name = field_name.upper()
    if value := os.getenv(env_name):
        return value
    # fallback to arsenal default args
    return ARSENAL_DEFAULT_ARGS.get(field_name)


def get_model_path():
    model_repo_dir = os.environ["MODEL_REPO_DIR"]
    dirs = os.listdir(model_repo_dir)
    if len(dirs) == 0:
        raise Exception("No any model directory found!")
    return str(os.path.join(model_repo_dir, dirs[0]))


def run():
    with open(SHELL_FILE_PATH, mode="w", encoding="utf-8") as f:
        f.write(f"trtllm-serve {os.getenv('COMMAND', '')} {get_model_path()} ")
        for option in serve_options:
            if (value := get_from_env(option)) is not None:
                f.write(f"--{option} {value} ")
                print(f"FROM ENV:  {option:<30} {value:<20}")  # log

        for env_name, env_value in os.environ.items():
            if env_name.startswith(PREFIX):
                env_name = env_name[len(PREFIX) :]
                parts = env_name.split("__")

                d = extra_llm_api_options
                for part in parts[:-1]:
                    d = d.setdefault(part.lower(), {})

                if env_value.lower() in ("true", "false"):
                    env_value = env_value.lower() == "true"
                elif env_value.isdigit():
                    env_value = int(env_value)

                d[parts[-1].lower()] = env_value

        if extra_llm_api_options:
            yaml_str = yaml.safe_dump(extra_llm_api_options, indent=2, default_flow_style=False)

            with open(EXTRA_YAML_PATH, "w", encoding="utf-8") as f_yaml:
                f_yaml.write(yaml_str)

            f.write(f"--extra_llm_api_options {EXTRA_YAML_PATH}")
            title_print("rebuild extra_llm_api_options")
            print(yaml_str)
            print()
            print("=" * 80)

    with open(SHELL_FILE_PATH, mode="r", encoding="utf-8") as f:
        title_print(SHELL_FILE_PATH)
        print(f.read())
        print()
        print("=" * 80)


if __name__ == "__main__":
    run()
