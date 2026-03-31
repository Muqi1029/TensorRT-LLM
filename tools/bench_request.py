import argparse
import asyncio
import json
import sys
import time
import traceback
from dataclasses import asdict, dataclass, field

import aiohttp
import numpy as np
from tqdm import tqdm

content = """根据工作描述的内容，介绍客户给用户。
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


@dataclass
class RequestOutput:
    success: bool = False
    latency_ms: float = 0.0
    content_list: list = field(default_factory=list)


async def vllm_request_func(pbar: tqdm, sem: asyncio.Semaphore):
    # print(args.output_len)
    async with sem:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "",
                "max_completion_tokens": args.output_len,
                # "stop": "<|im_end|>",
                "messages": [
                    {"role": "user", "content": content},
                ],
                # "temperature": 0.0,
                "n": args.n,
                # "best_of": 8,
                "use_beam_search": not args.disable_beam_search,
                # "stream": True,
                "early_stopping": False,
                # "beam_width_array": [16, 16, 32, 32],
                # "repetition_penalty": 1.0,
                # "length_penalty": 1.0
            }
            st = time.perf_counter()
            output = RequestOutput()
            output.content_list = ["" for _ in range(args.n)]
            try:
                async with session.post(
                    url=args.base_url + "/v1/chat/completions",
                    json=payload,
                    headers={
                        "Authorization": args.api_key,
                        "Content-Type": "application/json",
                    },
                ) as response:
                    if response.status == 200:
                        response_json = await response.json()

                        for choice in response_json["choices"]:
                            output.content_list[choice["index"]] = choice["message"]["content"]
                            if choice["index"] == 0:
                                # use the first choice as latency metric
                                output.latency_ms = (time.perf_counter() - st) * 1000
                        output.success = True
                    else:
                        print(response.reason)
            except Exception:
                exc_info = sys.exc_info()
                print("".join(traceback.format_exception(*exc_info)))
            pbar.update(1)
            return output


async def sgl_request_func(pbar: tqdm, sem: asyncio.Semaphore):
    async with sem:
        async with aiohttp.ClientSession() as session:
            payload = {
                "max_completion_tokens": args.output_len,
                "stop": "<|im_end|>",
                "messages": [
                    {"role": "user", "content": "Who are you"},
                ],
                "n": 5,
                "use_beam_search": True,
                "num_beam_samples": 3,
                "stream": False,
            }
            st = time.perf_counter()
            output = RequestOutput()
            output.content_list = ["" for _ in range(15)]
            try:
                async with session.post(
                    url=args.base_url + "/v1/chat/completions",
                    json=payload,
                    headers={
                        "Authorization": args.api_key,
                        "Content-Type": "application/json",
                    },
                ) as response:
                    if response.status == 200:
                        response_json = await response.json()

                        for choice in response_json["choices"]:
                            output.content_list[choice["index"]] = choice["message"]["content"]
                            if choice["index"] == 0:
                                # use the first choice as latency metric
                                output.latency_ms = (time.perf_counter() - st) * 1000
                        output.success = True
                    else:
                        print(response.reason)
            except Exception:
                exc_info = sys.exc_info()
                print("".join(traceback.format_exception(*exc_info)))
            pbar.update(1)
            return output


dispatcher = {
    "vllm": vllm_request_func,
    "trtllm": vllm_request_func,
    "sgl": sgl_request_func,
}


def compute(values: list, name: str):
    mean_ms = np.mean(values or 0)
    median_ms = np.median(values or 0)
    std_ms = np.std(values or 0)
    p99_ms = np.percentile(values or 0, 99)
    print(f"{name=:<15} {mean_ms=:.2f} {median_ms=:.2f} {std_ms=:.2f} {p99_ms=:.2f}")


async def main(args):
    pbar = tqdm(total=args.num_prompts)

    request_func = dispatcher[args.backend]

    sem = asyncio.Semaphore(args.max_concurrency)
    outputs = await asyncio.gather(
        *[asyncio.create_task(request_func(pbar, sem)) for _ in range(args.num_prompts)]
    )

    with open(f"{args.backend}_output.json", "w", encoding="utf-8") as f:
        json.dump([asdict(item) for item in outputs], f, ensure_ascii=False, indent=2)

    # filter
    filtered_output = [item for item in outputs if item.success]
    if len(filtered_output) != len(outputs):
        print("WARNING: some requests are not finished")

    latencies = [item.latency_ms for item in outputs]
    compute(latencies, "latentcy")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", default="http://127.0.0.1:8888")
    parser.add_argument("--api-key", default="JustKeepMe")
    parser.add_argument("--backend", choices=dispatcher.keys(), required=True)
    parser.add_argument("--n", default=8, type=int)
    parser.add_argument("--max-concurrency", default=32, type=int)
    parser.add_argument("--num-prompts", default=1000, type=int)
    parser.add_argument("--output-len", default=12, type=int)
    parser.add_argument("--disable-beam-search", action="store_true", default=False)

    args = parser.parse_args()
    asyncio.run(main(args))
