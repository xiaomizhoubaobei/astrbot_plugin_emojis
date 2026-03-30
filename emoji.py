from astrbot.api.all import *
import random
import aiohttp
import os
import json
import asyncio

# 自我防御回复语料
# Closes #32
# Add more fun defense statements for #35
self_text = [
    "那种事情不可以😣",
    "灰唁要被玩坏了😖",
    "发生什么了😪",
    "嗯？😴",
    "ta想做坏事，群友们超市ta！😡",
    "别闹，灰唁可是正经AI😤",
    "这种操作太犯规了，会被封号的🫨",
    "灰唁脸红：你、你在干嘛呀😳",
    "警告！检测到奇怪行为，启动卖萌防御模式🥺",
    "想对灰唁做啥？先过群友这关🧐",
    "灰唁启动了防沉迷系统😵",
    "检测到调皮能量超标，开启可爱护盾💖",
    "灰唁拒绝接受奇怪指令🙈",
    "再这样我要呼叫管理员啦👮",
    "灰唁已进入傲娇模式：哼！😾"
]

def load_api_config():
    """从 api_config.json 加载 API 映射表"""
    config_path = os.path.join(os.path.dirname(__file__), 'api_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        # 如果读取失败，返回空 dict
        return {}

async def fetch_image(qq_number, flag):
    # 每次调用重新读取配置，实现热更新
    switch_dict = load_api_config()
    print(f"[DEBUG] 请求参数: QQ={qq_number}, Flag={flag}")
    url = switch_dict.get(flag)
    if not url:
        supported_flags = "，".join(switch_dict.keys())
        result = MessageChain()
        result.chain = [Plain(f"不支持的表情类型，支持的表情类型有：{supported_flags}")]
        return result
    params = {'QQ': qq_number}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    image_data = await response.read()
                    result.chain = [Image.fromBytes(image_data)]
                    return result
                else:
                    try:
                        error_text = await response.text()
                    except Exception:
                        error_text = response.reason
                    result.chain = [Plain(f"表情包制作失败，状态码: {response.status}，错误信息: {error_text}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def parse_target(event):
    """解析@目标或用户名"""
    for comp in event.message_obj.message:
        if isinstance(comp, At):
            # 检查是否是@机器人自己
            if str(comp.qq) == str(event.get_self_id()):
                # 激活自我防御逻辑：随机选择一条回复语料
                selected_text = random.choice(self_text)
                yield event.plain_result(selected_text)
                return
            # 否则返回被@的用户QQ号
            return str(comp.qq)
    return None