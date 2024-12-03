from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
import json

import os
import random
from PIL import Image
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
# import aiohttp

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="randomUUZ",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

random_uuz_image = on_command("/随个uuz")

@random_uuz_image.handle()
# async def handle_random_uuz_image():
#     await random_uuz_image.send(message=MessageSegment.text("uuz"))
async def handle_random_uuz_image(bot: Bot, event: Event):
    # 图片目录路径
    image_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/randomuuz/image_file_ids.json'
    with open(image_ids_path, 'r') as file:
        image_ids = json.load(file)

    random_image_id = random.choice(image_ids)
    print(random_image_id)
    
    try:
        await random_uuz_image.send(Message(MessageSegment.image(random_image_id)))
    except Exception as e:
        # 如果发生异常，发送错误消息
        await random_uuz_image.finish(f"发生错误：{e}")


add_image = on_command("随个uuz 更新")

@add_image.handle()
async def handle_add_image(bot: Bot, event: Event):
    images_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/randomuuz/images/'
    file_names = os.listdir(images_path)
    new_json = []
    for filename in file_names:
        file_path = images_path + filename
        upload_response = await bot.upload_file(type='path',name=filename, path=file_path)
        file_id = upload_response['file_id']
        new_json.append(file_id)
    image_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/randomuuz/image_file_ids.json'
    with open(image_ids_path, 'w') as file:
        json.dump(new_json, file, indent=4)   
    await add_image.finish("图片更新完成")


# @add_image.got("image_id", prompt="请发送图片")
# async def got_add_image(bot: Bot, event: Event):
#     image_id = ""
#     found_image = False
#     while not found_image:
#         message = event.get_message()
#         for segment in message:
#             if(segment.type == "image"): 
#                 print(segment.data)
#                 image_id = segment.data["file_id"]
#                 found_image = True
#                 break
   
#     image_ids_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/randomuuz/image_file_ids.txt'
#     with open(image_ids_path, 'a') as file:
#         file.write('\n' + image_id)
#     await add_image.finish(f"添加成功, 图片id为{image_id}")
    