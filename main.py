import json
import os

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.all import *
from data.plugins.astrbot_plugin_emoji import emoji


def _load_emoji_commands() -> list:
    """从 api_config.json 动态加载所有支持的表情包命令列表"""
    config_path = os.path.join(os.path.dirname(__file__), 'api_config.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return list(json.load(f).keys())
    except Exception:
        return []


EMOJI_COMMANDS = _load_emoji_commands()


@register("astrbot_plugin_emojis", "祁筱欣",
          "一个表情包创建插件",
          "v0.0.1", "https://github.com/xiaomizhoubaobei/astrbot_plugin_emojis.git")
class Emojis(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.command("表情包")
    async def list_commands(self, event: AstrMessageEvent):
        cmds = " ".join(EMOJI_COMMANDS)
        yield event.plain_result(
            "指令格式：@本机器人 指令@xx
"
            f"支持的指令：{cmds}        "
        )

    async def _handle_emoji(self, event: AstrMessageEvent, command_name: str):
        """通用表情包处理方法，所有表情包命令共用此逻辑"""
        ids = await emoji.parse_target(event)
        if not ids:
            msg = MessageChain()
            msg.chain = [Plain("请@一个用户来制作表情包哦～")]
            await event.send(msg)
            return
        data = await emoji.fetch_image(ids, command_name)
        await event.send(data)


def _create_emoji_handler(cmd_name: str):
    """为指定表情包命令创建处理函数并注册为命令处理器"""
    @filter.command(cmd_name)
    async def handler(self, event: AstrMessageEvent):
        await self._handle_emoji(event, cmd_name)
    handler.__name__ = f"emoji_{cmd_name}"
    handler.__qualname__ = f"Emojis.emoji_{cmd_name}"
    return handler


# 动态注册所有表情包命令处理方法
for _cmd in EMOJI_COMMANDS:
    setattr(Emojis, f"emoji_{_cmd}", _create_emoji_handler(_cmd))
