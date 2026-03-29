from astrbot.api.all import *
import aiohttp
import random


class EmojiUtils:
    self_text = [
        "那种事情不可以😣",
        "灰唁要被玩坏了😖",
        "发生什么了😪",
        "嗯？😴",
        "ta想做坏事，群友们超市ta！😡"
    ]

    SWITCH_DICT = {
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

    @staticmethod
    async def fetch_image(qq_number, flag):
        print(f"[DEBUG] 请求参数: QQ={qq_number}, Flag={flag}")
        url = EmojiUtils.SWITCH_DICT.get(flag, '')
        params = {'QQ': qq_number}
        result = MessageChain()
        result.chain = []
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        with open("./data/plugins/astrbot_plugin_emoji/petemoji.gif", "wb") as file:
                            file.write(image_data)
                        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_emoji/petemoji.gif")]
                        return result
                    else:
                        result.chain = [Plain(f"表情包制作失败，状态码: {response.status}")]
                        return result
        except aiohttp.ClientError as e:
            result.chain = [Plain(f"请求异常: {e}")]
            return result

    @staticmethod
    async def parse_target(event):
        for comp in event.message_obj.message:
            if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
                return str(comp.qq)
        return None
