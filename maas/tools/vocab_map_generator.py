import json
from argparse import ArgumentParser

FILENAME = "new2old.json"


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--start-token-id", type=int, required=True, help="")
    parser.add_argument("--end-token-id", type=int, required=True, help="")
    return parser.parse_args()


def main(args):
    new2old_list = list(range(args.start_token_id, args.end_token_id + 1))
    with open(FILENAME, mode="w", encoding="utf-8") as f:
        json.dump(new2old_list, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    args = parse_args()
    main(args)
