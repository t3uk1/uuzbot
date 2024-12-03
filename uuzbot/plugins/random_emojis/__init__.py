from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_notice, get_bot, on_command
from nonebot.adapters.onebot.v12 import Bot, Event, NoticeEvent, Message, MessageSegment
from nonebot.params import ArgPlainText, CommandArg
import os
import random
import json
import shutil

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="random_emojis",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# emoji type list
send_bang_emoji = on_command("/bang")
send_uma_emoji = on_command("/随机赛马娘")
send_miku_emoji = on_command("/miku")
send_gbc_emoji = on_command("/gbc")
send_moye_emoji = on_command("/moye")
send_doro_emoji = on_command("/doro")

# update emoji
update_emoji = on_command("/表情库添加")

global emoji_database
@update_emoji.handle()
async def handle_add_emoji(event: Event, args: Message = CommandArg()):
    args_texts = args.extract_plain_text().split(' ')
    if args_texts[0] == '':
        await update_emoji.finish("未知的表情包库参数")
    elif len(args_texts) == 1:
        global emoji_database
        emoji_database = args_texts[0]
        print(emoji_database)

@update_emoji.got("emoji_id", prompt="开始上传表情包")
async def got_add_emoji(bot: Bot, event: Event):
    emoji_id = ''
    message = str(event.get_message())
    emoji_id = message.split("file_id=")[1]
    emoji_id = emoji_id.strip("[]")
    # print(emoji_id)  

    # 将临时表情文件另存为
    temp_file_info = await bot.get_file(type='url', file_id=emoji_id)
    temp_file_url = temp_file_info["url"]
    temp_file_path = temp_file_url.split('/')[-1].replace('\\', '/')
    poke_emoji_new_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/random_emojis/emojis/' + emoji_database + "/" + emoji_id + '.gif'
    with open(temp_file_path, 'rb') as fsrc:
        with open(poke_emoji_new_path, 'wb') as fdst:
            shutil.copyfileobj(fsrc, fdst)

    emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/random_emojis/emojis.json' 
    with open(emoji_ids_path, 'r') as file:
        data = json.load(file)
    data[emoji_database].append(emoji_id)
    with open(emoji_ids_path, 'w') as file:
        json.dump(data, file, indent=4)
    await update_emoji.finish(f"添加成功, file_id为{emoji_id}")


# send emoji
@send_bang_emoji.handle()
async def handle_send_bang(bot: Bot, event: Event, args: Message = CommandArg()):
    random_bang_emoji_id = await get_emoji_file_id("bang")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_bang_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))


@send_uma_emoji.handle()
async def handle_send_uma(bot: Bot, event: Event):
    random_uma_emoji_id = await get_emoji_file_id("uma")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_uma_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))


@send_miku_emoji.handle()
async def handle_send_miku(bot: Bot, event: Event):
    random_miku_emoji_id = await get_emoji_file_id("miku")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_miku_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))

@send_gbc_emoji.handle()
async def handle_send_gbc(bot: Bot, event: Event):
    random_gbc_emoji_id = await get_emoji_file_id("gbc")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_gbc_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))

@send_moye_emoji.handle()
async def handle_moye(bot: Bot, event: Event):
    random_moye_emoji_id = await get_emoji_file_id("moye")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_moye_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))

@send_doro_emoji.handle()
async def handle_doro(bot: Bot, event: Event):
    random_moye_emoji_id = await get_emoji_file_id("doro")
    emoji_apply = MessageSegment("wx.emoji",{"file_id":random_moye_emoji_id})
    await send_bang_emoji.finish(Message(emoji_apply))

async def get_emoji_file_id(branch_name):
    emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/random_emojis/emojis.json' 
    with open(emoji_ids_path, 'r') as file:
        data = json.load(file)
    emoji_ids = data[branch_name]
    random_emoji_id = random.choice(emoji_ids)
    return random_emoji_id