from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from collections import defaultdict, deque
import json
from nonebot.adapters.onebot.v12 import Bot, Event,GroupMessageEvent, Message, MessageSegment

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="repeator",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 定义一个全局字典来存储每个群聊中的消息状态
message_count = defaultdict(lambda: [])

# 定义事件响应器
repeator = on_message()

# 目前只能支持连续三条的复读
# 剩下的日后再说()
@repeator.handle()
async def handle_repeator(bot: Bot, event: Event) -> None:
    # 检查是否为群聊消息
    if isinstance(event, GroupMessageEvent):
        # 获取群聊ID
        group_id = str(event.get_session_id())
        # 获取消息内容
        message = str(event.get_message()).strip()
        # 命令格式的消息忽略
        if message.startswith('/'):
            return
        
        # 更新对应群聊的消息状态
        message_count[group_id].append(message)
        
        # 如果同一个文本消息达到三次
        if len(message_count[group_id]) >= 3 and len(set(message_count[group_id][-3:])) == 1:
            # 重置对应群聊的状态
            message_count[group_id].clear()
            # 复读该文本
            await bot.send(event, message)

        # 如果消息列表长度超过3，移除最早的消息
        if len(message_count[group_id]) > 3:
            message_count[group_id].pop(0)
    
            


