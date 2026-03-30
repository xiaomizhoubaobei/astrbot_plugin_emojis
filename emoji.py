from astrbot.api.all import *
import random
import aiohttp
import os

self_text = [
    "那种事情不可以😣",
    "灰唁要被玩坏了😖",
    "发生什么了😪",
    "嗯？😴",
    "ta想做坏事，群友们超市ta！😡"
]

async def fetch_image(qq_number, flag):
    # 定义字典映射
    print(f"[DEBUG] 请求参数: QQ={qq_number}, Flag={flag}")
    switch_dict = {
        "摸头": "https://api.lolimi.cn/API/face_petpet/api.php",
        "感动哭了": "https://api.lolimi.cn/API/face_touch/api.php",
        "膜拜": "https://api.lolimi.cn/API/face_worship/api.php",
        "咬": "https://api.lolimi.cn/API/face_suck/api.php",
        "可莉吃": "https://api.lolimi.cn/API/chi/api.php",
        "捣": "https://api.lolimi.cn/API/face_pound/api.php",
        "咸鱼": "https://api.lolimi.cn/API/face_yu/api.php",
        "玩": "https://api.lolimi.cn/API/face_play/api.php",
        "拍": "https://api.lolimi.cn/API/face_pat/api.php",
        "丢": "https://api.lolimi.cn/API/diu/api.php",
        "撕": "https://api.lolimi.cn/API/si/api.php",
        "求婚": "https://api.lolimi.cn/API/face_propose/api.php",
        "爬": "https://api.lolimi.cn/API/pa/api.php",
        "你可能需要他": "https://api.lolimi.cn/API/face_need/api.php",
        "想看": "https://api.lolimi.cn/API/face_thsee/api.php",
        "点赞": "https://api.lolimi.cn/API/zan/api.php",
    }
    # 获取对应的URL
    url = switch_dict.get(flag)
    if not url:
        supported_flags = "，".join(switch_dict.keys())
        result = MessageChain()
        result.chain = [Plain(f"不支持的表情类型，支持的表情类型有：{supported_flags}")]
        return result
    params = {
        'QQ': qq_number
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 构造返回结果（直接使用网络图片数据）
                    result.chain = [Image.fromBytes(image_data)]
                    return result
                else:
                    # 获取服务端返回的错误信息
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
            if str(comp.qq) == str(event.get_self_id()):
                selected_text = random.choice(self_text)
                yield event.plain_result(selected_text)
                return
            return str(comp.qq)
    return None