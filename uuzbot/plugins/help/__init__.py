from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
import os
from PIL import ImageFont, Image, ImageDraw
from nonebot.adapters.onebot.v12 import Bot, Event, NoticeEvent, Message, MessageSegment

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="help",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

help = on_command("/help")

# 文本转图片
async def text_to_image(text):
    fontpath = 'C:/Windows/Fonts/simhei.ttf'
    font = ImageFont.truetype(fontpath, 24)
    padding = 20
    margin = 4
    text_list = text.split('\n')
    max_width = 0
    max_height = 0
    line_heights = []

    for line in text_list:
        w, h = font.getbbox(line)[2:]
        max_width = max(max_width, w)
        line_heights.append(h)  # 记录每一行的高度

    wa = max_width + padding * 2
    ha = sum(line_heights) + (len(text_list) - 1) * margin + padding * 2
    i = Image.new('RGB', (wa, ha), color=(255, 255, 255))
    draw = ImageDraw.Draw(i)

    y_offset = padding
    for j, line in enumerate(text_list):
        h = line_heights[j]
        draw.text((padding, y_offset), line, font=font, fill=(0, 0, 0))
        y_offset += h + margin  # 更新 y 偏移量

    return i

@help.handle()
async def handle_help(bot: Bot):
    help_dir_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/help'
    help_text_path = help_dir_path + '/help.txt'
    help_image_path = help_dir_path + '/help.png'
    # help_text_path = 'C:/Users/y1027/Desktop/bot/uuzbot/uuzbot/plugins/help/help.txt'
    with open(help_text_path, 'r', encoding='utf-8') as file:
        help_text = file.read()
        help_image = await text_to_image(help_text)
        help_image.save(help_image_path, "PNG")

        upload_response = await bot.upload_file(type='path',name="help_image", path=help_image_path)
        image_id = upload_response['file_id']
        print(image_id)
        await help.finish(Message(MessageSegment.image(image_id)))
