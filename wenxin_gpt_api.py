import requests
import json
from split_segments import split_string
import time
import logging

# API_KEY = "RgAq3xxxxxvXOoLy"
# SECRET_KEY = "zWSdXWxxxxxxmkRWi8YORj"


def get_access_token():
    token = r"24.e78893178f759a5331d4c7fa40f6a957.2592000.1695373564.282335-33925417"
    return token


def wenxin_correct(prompt, content):
    content_list = split_string(content, max_length=1000, split_symbol="。")
    curr_res = ""
    for content in content_list:
        start_time = time.time()
        curr_res += wenxin_call(prompt, content)
        logging.info("wenxin single piece costing time: " + str(time.time() - start_time) + "s")
    return curr_res


def wenxin_call(prompt, content):
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token=" \
          + get_access_token()
    # url = r"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" \
    #      + get_access_token()

    payload = json.dumps({
        "messages": [
            {"role": "user",
             "content": prompt},
            {"role": "assistant",
             "content": "好的，请提供需要处理的文本内容。"},
            {"role": "user",
             "content": content}
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    temp = response.text
    result = json.loads(temp).get("result", "")
    return result


