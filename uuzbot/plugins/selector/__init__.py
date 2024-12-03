from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot.adapters.onebot.v12 import Bot, Event
import random
import re

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="selector",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

selector = on_message()
@selector.handle()
async def handle_select(bot: Bot, event: Event):
    if event.get_user_id() == "wxid_czeabjvsc9a729":
        return
    message_text = str(event.get_message())
    # 纯文本消息记得过滤命令头
    if '还是' in message_text and message_text.startswith('/') == False and message_text.startswith("还是") == False:
        # 去掉@用户部分
        message_text = re.sub(r'\[mention:.*?\]', '', message_text)
        choices = message_text.split('还是')
        for choice in choices:
            if choice == ' ':
                return
        choice = random.choice(choices)
        await selector.finish(choice)


