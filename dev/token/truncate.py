import json
import os
from enum import Enum
from typing import List

from judge import judge_token
from transformers import AutoTokenizer


def pretty_print(content: str):
    print()
    print(f" {content} ".center(80, "="))


model_path = os.environ["GR_F1_QWEN_05B"]


class TOKENTYPE(Enum):
    CHINESE = 0
    ASCII = 1
    COMMA = 2


def truncate(vocab: dict):
    i = 0
    new_token_ids = []
    truncated_vocab = {}
    for token, token_id in vocab.items():
        real_text = tokenizer.convert_tokens_to_string([token])
        if is_valid := judge_token(real_text):
            truncated_vocab[token] = token_id
            new_token_ids.append(token_id)
        if i < 20:
            print(f"{real_text:<30} {is_valid=}")
            i += 1

    pretty_print(f"Truncated Vocab Size: {len(truncated_vocab)}")

    with open("new_vocab.json", mode="w", encoding="utf-8") as f:
        json.dump(truncated_vocab, f, indent=2, ensure_ascii=False)

    new_token_ids.sort()
    with open("new_token_ids.json", mode="w", encoding="utf-8") as f:
        json.dump(new_token_ids, f, indent=2, ensure_ascii=False)

    old2new = {}
    for new_token_id, old_token_id in enumerate(new_token_ids):
        old2new[old_token_id] = new_token_id
    with open("old2new.json", mode="w", encoding="utf-8") as f:
        json.dump(old2new, f, indent=2, ensure_ascii=False)


def test_token(token: str):
    print(f"Processing {token=}: {judge_token(token)}")


def find_key(target_id: int):
    for key, token_id in vocab.items():
        if token_id == target_id:
            found_key = key
            break
    print(f"{found_key=}")


def convert_back(token_ids: List[int], tokenizer) -> str:
    with open("new_token_ids.json", "r", encoding="utf-8") as f:
        new_ids = json.load(f)
    original_ids = [new_ids[token_id] for token_id in token_ids]
    text = tokenizer.decode(original_ids)
    print(f"{text=}")


def show_semantic_ids(vocab):
    start_id = 151646
    ids = []
    for token, token_id in vocab.items():
        if token_id >= start_id:
            ids.append(token_id)
    ids.sort()
    with open("new2old.json", "w", encoding="utf-8") as f:
        json.dump(ids, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # get_vocab() returns a dictionary of {token: id}
    vocab = tokenizer.get_vocab()

    pretty_print(f"Original Vocab Size: {len(vocab)}")
    # test_token(" ")

    # truncate(vocab)
    show_semantic_ids(vocab)
    # find_key(108386)

    # token_ids = [28542, 43141, 96773, 15960, 111229, 39238]
    # convert_back(token_ids, tokenizer)
