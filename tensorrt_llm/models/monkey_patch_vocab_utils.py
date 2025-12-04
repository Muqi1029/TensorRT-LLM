import json
import os
from typing import List

script_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(script_dir, "qwen/new_token_ids.json")

with open(filepath, "r", encoding="utf-8") as f:
    new_vocab_list = json.load(f)

old2new_filepath = os.path.join(script_dir, "qwen/old2new.json")
with open(old2new_filepath, "r", encoding="utf-8") as f:
    old2new_dict = json.load(f)


def patch_config(config):
    config.vocab_size = len(new_vocab_list)


def patch_embed_tokens(tensor):
    tensor = tensor[:]
    tensor = tensor[new_vocab_list]
    return tensor


def patch_input(input_ids, sampling_params):
    input_ids = [old2new_dict[str(input_id)] for input_id in input_ids]

    sampling_params.end_id = old2new_dict[str(sampling_params.end_id)]
    sampling_params.pad_id = old2new_dict[str(sampling_params.pad_id)]
    sampling_params._stop_word_ids = [
        [old2new_dict[str(token_id[0])]] for token_id in sampling_params._stop_word_ids
    ]

    return input_ids, sampling_params


def patch_output(output_ids) -> List[int]:
    return [new_vocab_list[id] for id in output_ids]


class FakeSlice:
    def __init__(self, original_slice, key):
        self.original_slice = slice

    def get_shape(self):
        pass
