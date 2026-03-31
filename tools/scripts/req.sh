#!/bin/bash

MODEL_NAME="checkpoint-109368-test-sug-model"
MODEL_PATH="/models/arsenal-inf/${MODEL_NAME}"
# URL="${A30_URL}"
# URL="127.0.0.1:8888"
URL="maas-b-sug-gr-prod-queryrec-sug-gr-v2-default.kanzhun.tech"
max_tokens=10
best_of=32
n=32

presence_penalty=0.0
frequency_penalty=0.0
#presence_penalty=1.9
#frequency_penalty=1.9

CONTENT='性别：女，年龄：33岁，工作：11年，状态：职场，学历：本科，期望职业：带货主播。<工作经历>：上海能良电子科技有限公司_广东梵大集团有限公司_喜彩屋（广州）网络科技有限公司。<专业>：土木工程。<求职期望>：带货主播_总助/ceo助理/董事长助理_直播运营。<搜索历史>：上海能良_起跑线_贝苗传媒_上海能良电子科技有限公司_深圳青旅_青旅_九猫。<喜欢的工作>：带货主播_人事/招聘专员/底薪+提成_电商带货主播_电商带货主播_电商带货主播_（双休）中层事业管理岗_高薪主播销售（小白可做）_主播(旅行社）_【电商带货主播】_姐妹！！微信运营。<浏览的工作>：带货主播_男女主播_食品带货主播（抖音）_双休缺个搭子零零后老板创业急需人才！审核_急招抖音旅游主播_新媒体销售_双休新公司很差人 来就要不加班到点走审核_招两个徒弟亲自带_抖音直播_电商带货主播'

curl -X POST \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg model "$MODEL_PATH" \
    --arg content "$CONTENT" \
    --argjson max_tokens "$max_tokens" \
    --argjson best_of "$best_of" \
    --argjson n "$n" \
    --argjson presence_penalty "$presence_penalty" \
    --argjson frequency_penalty "$frequency_penalty" \
    '{
      model: $model,
      stream: false,
      messages: [
        {
          role: "user",
          content: $content
        }
      ],
      stop: ["<|im_end|>"],
      max_tokens: $max_tokens,
      best_of: $best_of,
      n: $n,
      use_beam_search: true,
      presence_penalty: $presence_penalty,
      frequency_penalty: $frequency_penalty,
      early_stopping: true
    }')" \
  "http://${URL}/v1/chat/completions" | jq
