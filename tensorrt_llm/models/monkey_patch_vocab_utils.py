import json
import os
from pathlib import Path

vocab_map_filename = "new2old.json"
vocab_map_filepath = Path(os.path.dirname(__file__)).parent.parent / vocab_map_filename

with open(vocab_map_filepath, "r", encoding="utf-8") as f:
    vocab_map_list = json.load(f)

new_vocab_len = len(vocab_map_list)


def patch_tensors(tensor):
    tensor = tensor[:]
    tensor = tensor[vocab_map_list]
    return tensor


# def patch_input(input_ids, sampling_params):
#     # input_ids = [old2new_dict[str(input_id)] for input_id in input_ids]
#     input_ids = [i + 1 for i in range(len(input_ids))]
#
#     sampling_params.end_id = 125  # old2new_dict[str(sampling_params.end_id)]
#     sampling_params.pad_id = 123  # old2new_dict[str(sampling_params.pad_id)]
#     sampling_params._stop_word_ids = [
#         # [old2new_dict[str(token_id[0])]] for token_id in sampling_params._stop_word_ids
#         [125]
#         for token_id in sampling_params._stop_word_ids
#     ]
#
#     return input_ids, sampling_params
#
#
# def patch_output(output_ids) -> List[int]:
#     return [new_vocab_list[id] for id in output_ids]
