from astrbot.api.all import *
import aiohttp

PETEMOJI_PATH = "./data/plugins/astrbot_plugin_emoji/petemoji.gif"


class EmojiUtils:

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
        """
        根据 QQ 号和表情标志获取表情包图片并发送。

        Args:
            qq_number (str): 目标 QQ 号，不能为空。
            flag (str): 表情类型标志，对应 SWITCH_DICT 中的键。

        Returns:
            MessageChain: 包含图片或错误信息的消息链。
        """
        if not qq_number:
            return MessageChain([Plain("缺少有效的 QQ 号参数")])
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
                        with open(PETEMOJI_PATH, "wb") as file:
                            file.write(image_data)
                        result.chain = [Image.fromFileSystem(PETEMOJI_PATH)]
                        return result
                    else:
                        result.chain = [Plain(f"表情包制作失败，状态码: {response.status}")]
                        return result
        except aiohttp.ClientError as e:
            result.chain = [Plain(f"请求异常: {e}")]
            return result

    @staticmethod
    async def parse_target(event):
        """
        从事件消息中解析出被 At 的目标 QQ 号（排除自己）。

        Args:
            event: 消息事件对象。

        Returns:
            str | None: 目标 QQ 号，若未找到则返回 None。
        """
        for comp in event.message_obj.message:
            if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
                return str(comp.qq)
        return None
