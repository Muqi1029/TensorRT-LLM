import json
import os
from pathlib import Path

vocab_map_list = None


def maybe_read_file():
    vocab_map_filename = "new2old.json"
    vocab_map_filepath = Path(os.path.dirname(__file__)).parent.parent / vocab_map_filename

    print(f"Load map file: {vocab_map_filepath=}")
    with open(vocab_map_filepath, "r", encoding="utf-8") as f:
        vocab_map_list = json.load(f)
    return vocab_map_list


def get_vocab_len():
    global vocab_map_list
    if vocab_map_list is None:
        vocab_map_list = maybe_read_file()
    new_vocab_len = len(vocab_map_list)
    return new_vocab_len


def patch_tensors(tensor):
    global vocab_map_list
    if vocab_map_list is None:
        vocab_map_list = maybe_read_file()
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
