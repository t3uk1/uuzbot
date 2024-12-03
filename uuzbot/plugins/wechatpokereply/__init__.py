from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_notice, get_bot, on_command
from nonebot.adapters.onebot.v12 import Bot, Event, NoticeEvent, Message, MessageSegment
from nonebot.rule import to_me
import random
import os
import json
import shutil

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="wechatPokeReply",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

poke = on_notice()

@poke.handle()
async def handle_poke(bot: Bot, event: Event):
    # 检查事件是否为拍一拍事件
    event_type = event.detail_type
    # print(event.user_id)
    if "poke" in event_type and event.user_id == 'wxid_5r5feen7ekgp12':
        # reply = MessageSegment.text("你拍我干啥？")
        emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/wechatpokereply/poke_emojis.json' 
        # emoji_ids_path= 'C:/Users/y1027/Desktop/bot/uuzbot/uuzbot/plugins/wechatpokereply/poke_emojis.txt'
        with open(emoji_ids_path, 'r') as file:
            emoji_ids = json.load(file)
    
        # emoji_ids = [id.strip() for id in emoji_ids]
        random_emoji_id = random.choice(emoji_ids)
        reply = MessageSegment("wx.emoji",{"file_id":random_emoji_id})

        print(event_type, reply)
        # 发送回复消息并结束事件处理
        bot = get_bot()
        if event_type == 'wx.get_private_poke':
            print(event.from_user_id)
            await bot.send_message(detail_type='private', user_id=event.from_user_id ,messagge=reply)
            # 私聊寄了不写了（
        else:
            await bot.send_message(detail_type='group', group_id=event.group_id,message=reply)


add_emoji = on_command("拍一拍添加")
@add_emoji.got("emoji_id", prompt="开始上传表情包")
async def got_add_emoji(bot: Bot, event: Event):
    emoji_id = ""
    message = str(event.get_message())
    emoji_id = message.split("file_id=")[1]
    emoji_id = emoji_id.strip("[]")
    print(emoji_id)  

    temp_file_info = await bot.get_file(type='url', file_id=emoji_id)
    temp_file_url = temp_file_info["url"]
    temp_file_path = temp_file_url.split('/')[-1].replace('\\', '/')
    poke_emoji_new_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/wechatpokereply/poke_emojis/' + emoji_id + '.gif'
    with open(temp_file_path, 'rb') as fsrc:
        with open(poke_emoji_new_path, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)
    
    emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/wechatpokereply/poke_emojis.json' 
    with open(emoji_ids_path, 'r') as file:
        # file.write(emoji_id + '\n')
        data = json.load(file)
    data.append(emoji_id)
    with open(emoji_ids_path, 'w') as file:
        json.dump(data, file, indent=4)
    await add_emoji.finish(f"添加成功, file_id为{emoji_id}")
    