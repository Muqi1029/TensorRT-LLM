"""Convert yaml data to env setting to adapt to ARSENAL MAAS."""

from typing import Dict

import yaml


def yaml_to_env(data: Dict, prefix: str = "TRTLLM", sep: str = "__"):
    env_vars = []

    def recurse(item, current_key):
        if isinstance(item, dict):
            for key, value in item.items():
                new_key = f"{current_key}{sep}{key.upper()}" if current_key else key.upper()
                recurse(value, new_key)
        else:
            # handle bool env
            if isinstance(item, bool):
                value = str(item).lower()
            else:
                value = item
            env_vars.append(f"{current_key}={value}")

    recurse(data, prefix.upper())
    return "\n".join(env_vars)


yaml_content = """
build_config:
  max_batch_size: 16
  max_beam_width: 128
  max_seq_len: 2048
  plugin_config:
    gpt_attention_plugin: auto
    remove_input_padding: true
    context_fmha: true
    use_paged_context_fmha: true
    paged_kv_cache: true
    multiple_profiles: true

extended_runtime_perf_knob_config:
  cuda_graph_mode: true
  cuda_graph_cache_size: 32
"""


if __name__ == "__main__":
    data = yaml.safe_load(yaml_content)
    result = yaml_to_env(data)

    print(result)
