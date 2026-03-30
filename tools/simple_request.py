from pprint import pprint

import requests


def main():
    base_url = "http://maas-gr-query-rec-gray-sgl-beam-default.kanzhun-inc.com"
    api_key = "JustKeepMe"
    payload = {
        "model": "qwen-0.5b",
        "max_tokens": 12,
        "stop": "<|im_end|>",
        "messages": [
            {"role": "user", "content": "Who are you"},
        ],
        "temperature": 1.0,
        "n": 5,
        "use_beam_search": True,
        "num_beam_samples": 4,
        "repetition_penalty": 1.0,
        "length_penalty": 1.0,
    }

    try:
        response = requests.post(
            url=f"{base_url}/v1/chat/completions",
            headers={"Authorization": api_key, "Content-Type": "application/json"},
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        pprint(response.json())
    except requests.RequestException as e:
        print("❌ Request failed:", e)
        if response := getattr(e, "response", None):
            print("Response text:", response.text)


if __name__ == "__main__":
    main()
