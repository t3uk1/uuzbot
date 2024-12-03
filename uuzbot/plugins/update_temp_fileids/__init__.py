from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
import os
import json
from datetime import datetime

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="update_temp_fileids",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

update = on_command("/更新临时表情")

async def update_file_id(emoji_path, emoji_name, bot: Bot, event: Event):
    # temp_file_info = await bot.get_file(type='url', file_id=temp_file_id)
    # temp_file_url = temp_file_info["url"]
    # temp_file_name = temp_file_info['name']
    # print(temp_file_url)
    # temp_file_path = temp_file_url.split('/')[-1].replace('\\', '/')
    # print(temp_file_path)

    upload_response = await bot.upload_file(type='path',name=emoji_name, path=emoji_path)
    new_file_id = upload_response['file_id']
    print(new_file_id)
    update_log_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/update_temp_fileids/update.log'
    nowtime = datetime.now()
    with open(update_log_path, 'a') as file:
        file.write(f'{nowtime} | success update file_id: {new_file_id} from {emoji_path}\n')
    #await update.send(Message(MessageSegment("wx.emoji",{"file_id":new_file_id})))
    return new_file_id


@update.handle()
async def handle_update(bot: Bot, event: Event):
    emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/random_emojis/emojis.json' 
    with open(emoji_ids_path, 'r') as file:
        data = json.load(file)
    new_json = {}
    for key in data:
        new_json[key] = []
        emojis_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/random_emojis/emojis/' + key + '/'
        emoji_names = os.listdir(emojis_path)
        for emoji_name in emoji_names:
            emoji_path = emojis_path + emoji_name
            new_json[key].append(await update_file_id(emoji_path, emoji_name, bot, event))
        # for emoji_file_id in data[key]:
            # new_json[key].append(await update_file_id(emoji_file_id, bot, event))
            
    print(new_json)
    with open(emoji_ids_path, 'w') as file:
        json.dump(new_json, file, indent=4)

    
    # poke_emojis
    poke_emoji_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/wechatpokereply/poke_emojis.json'
    with open(poke_emoji_ids_path, 'r') as file:
        data = json.load(file)
        new_poke_emojis_file_ids = []
        emojis_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/wechatpokereply/poke_emojis/'
        emoji_names = os.listdir(emojis_path)
        for emoji_name in emoji_names:
            emoji_path = emojis_path + emoji_name
            new_poke_emojis_file_ids.append(await update_file_id(emoji_path, emoji_name, bot, event))
        # for poke_emoji_file_id in data:
        #     new_poke_emojis_file_ids.append(await update_file_id(poke_emoji_file_id, bot, event))
    # print(new_poke_emojis_file_ids)
    with open(poke_emoji_ids_path, 'w') as file:
        json.dump(new_poke_emojis_file_ids, file, indent=4)
    
    await update.finish("所有表情file_id更新完成.")

