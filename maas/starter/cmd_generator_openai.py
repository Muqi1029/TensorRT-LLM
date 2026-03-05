import os

import torch

SHELL_FILE_PATH = "/app/starter/start_cmd.sh"

# hardcode here since trtllm uses click command parser
serve_options = [
    "tokenizer",
    "host",
    "port",
    "backend",
    "log_level",
    "max_beam_width",
    "max_batch_size",
    "max_num_tokens",
    "max_seq_len",
    "tp_size",
    "pp_size",
    "ep_size",
    "cluster_size",
    "gpus_per_node",
    "kv_cache_free_gpu_memory_fraction",
    "num_postprocess_workers",
    "trust_remote_code",
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
]


def get_device_count():
    if not torch.cuda.is_available():
        raise Exception("No GPU Found!")
    return torch.cuda.device_count()


def title_print(title: str):
    print("\n\n" + f" {title} ".center(80, "=") + "\n")


def get_model_path():
    model_repo_dir = os.environ["MODEL_REPO_DIR"]
    dirs = os.listdir(model_repo_dir)
    if len(dirs) == 0:
        raise Exception("No any model directory found!")
    return str(os.path.join(model_repo_dir, dirs[0]))


arsenal_default_args = {
    "host": "0.0.0.0",
    "port": 8000,
    "tp_size": get_device_count(),
    "log_level": "verbose",
}


def get_from_env(field_name: str):
    # env_name: MODEL_PATH TP_SIZE
    env_name = field_name.upper()
    if value := os.getenv(env_name):
        return value
    return arsenal_default_args.get(field_name, None)


def run():
    with open(SHELL_FILE_PATH, mode="w", encoding="utf-8") as f:
        f.write(f"trtllm-serve {os.getenv('COMMAND', '')} {get_model_path()} ")
        for option in serve_options:
            if (value := get_from_env(option)) is not None:
                f.write(f"--{option} {value} ")
                print(f"FROM ENV:  {option:<30} {value:<20}")  # log

    with open(SHELL_FILE_PATH, mode="r", encoding="utf-8") as f:
        title_print(SHELL_FILE_PATH)
        print(f.read())
        print()
        print("=" * 80)


if __name__ == "__main__":
    run()
