"""Usage: python one_request.py"""

import argparse
import time
from pprint import pprint

import numpy as np
import requests

f1_content = """根据工作描述的内容，介绍客户给用户。
职位：<|j0:0003|><|j1:0224|><|j2:0761|><|j3:0060|>
用户满意的客户：<|e0:0899|><|e1:0937|><|e2:0101|><|e3:0194|><|e0:0068|><|e1:0860|><|e2:0653|><|e3:0417|><|e0:0951|><|e1:0694|><|e2:0346|><|e3:0181|><|e0:0404|><|e1:0359|><|e2:0449|><|e3:0576|><|e0:0665|><|e1:0806|><|e2:0976|><|e3:0695|><|e0:0076|><|e1:0884|><|e2:0483|><|e3:0423|><|e0:0528|><|e1:0488|><|e2:0116|><|e3:0048|><|e0:0250|><|e1:0804|><|e2:0755|><|e3:0277|><|e0:0951|><|e1:0700|><|e2:0571|><|e3:0878|><|e0:1022|><|e1:0667|><|e2:0724|><|e3:0144|><|e0:0610|><|e1:0833|><|e2:0069|><|e3:0992|><|e0:0012|><|e1:1015|><|e2:0165|><|e3:0195|><|e0:0528|><|e1:0795|><|e2:0256|><|e3:0066|><|e0:0404|><|e1:0510|><|e2:0291|><|e3:0001|><|e0:0250|><|e1:0368|><|e2:0364|><|e3:0457|><|e0:0176|><|e1:0908|><|e2:0668|><|e3:0305|><|e0:0708|><|e1:0205|><|e2:0097|><|e3:0422|><|e0:0250|><|e1:0469|><|e2:0028|><|e3:0564|><|e0:0528|><|e1:0837|><|e2:0069|><|e3:0242|><|e0:0250|><|e1:0466|><|e2:0551|><|e3:0368|><|e0:0404|><|e1:0263|><|e2:0480|><|e3:0623|><|e0:0068|><|e1:0493|><|e2:1016|><|e3:0611|><|e0:0528|><|e1:0353|><|e2:1011|><|e3:0056|><|e0:0653|><|e1:0609|><|e2:0759|><|e3:0590|><|e0:0250|><|e1:0226|><|e2:0069|><|e3:0916|><|e0:0250|><|e1:0320|><|e2:0455|><|e3:0093|><|e0:0206|><|e1:0471|><|e2:0954|><|e3:0437|><|e0:0528|><|e1:0930|><|e2:0069|><|e3:0342|><|e0:0528|><|e1:0265|><|e2:0391|><|e3:0992|><|e0:0404|><|e1:0675|><|e2:0291|><|e3:0001|>
双方满意的客户：

职位信息：
- 职位：月入7000+配车包住+0元入职外卖骑手
- 岗位：送餐员
- 公司：成都泰便利电子商务有限公司
- 品牌：泰便利
- 城市：成都
- 学历要求：不限
- 薪资要求：5k-8k
- 技能要求：餐饮外卖#&#自带电动车/摩托车#&#会用导航#&#生鲜蔬果#&#日结工资#&#全职兼职均可#&#酒水饮料#&#月结工资#&#公司提供电动车/摩托车#&#无犯罪记录#&#周结工资#&#配车无押金，0元入职
请根据以上信息，为用户推荐合适的客户。
"""
query_content = "who are you"


def main(args):
    if args.mode == "query":
        content = query_content
        max_tokens = 12
    elif args.mode == "f1":
        content = f1_content
        max_tokens = 2
    else:
        raise ValueError(f"{args.mode} is not supported")

    payload = {
        "model": "",
        "max_tokens": max_tokens,
        # "stop": "<|im_end|>",
        "messages": [
            {"role": "user", "content": content},
        ],
        # "beam_width_array": [1, 2]
        # "num_beam_samples": 4,
        # "early_stopping": False,
        # "repetition_penalty": 0.1,
        # "length_penalty": 0.0,
        # "frequency_penalty": 0.0,
        # "presence_penalty": 0.0,
    }
    if not args.disable_beam_search:
        payload.update({"n": args.beam, "best_of": args.beam, "use_beam_search": True})

    latency_ms_list = []
    for _ in range(args.n):
        try:
            start_tic = time.perf_counter()
            response = requests.post(
                url=f"{args.base_url}/v1/chat/completions",
                headers={
                    "Authorization": args.api_key,
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            latency_ms_list.append((time.perf_counter() - start_tic) * 1000)

            pprint(response.json())
        except requests.HTTPError:
            print(response.text)
        time.sleep(0.5)

    # remove slowest 3
    latency_ms_list.sort()
    if len(latency_ms_list) > 3:
        latency_ms_list = latency_ms_list[3:]
        print(f"\033[42m {np.mean(latency_ms_list)=} in {len(latency_ms_list)} rounds \033[0m")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8888")
    parser.add_argument("--api-key", default="JustKeepMe")
    parser.add_argument("--beam", type=int, default=32, help="Beam width")
    parser.add_argument("--n", type=int, default=13, help="Repeat times")
    parser.add_argument("--mode", type=str, choices=["query", "f1"], default="f1")
    parser.add_argument(
        "--disable-beam-search",
        action="store_true",
        help="Disable Beam Search for compatibility for other llm inference engine",
    )

    args = parser.parse_args()
    main(args)
