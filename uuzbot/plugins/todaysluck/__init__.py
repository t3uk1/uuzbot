from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
import os
import random
import json
from datetime import datetime

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="todaysluck",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

todaysluck = on_command("/今日运势")

# 每天清空记录
async def refresh():
    nowtime = datetime.now()
    nowdate = str(nowtime.date())
    log_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/todaysluck/reply.log'
    with open(log_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    for log in data:
        luck_info = log.split(' ')
        if nowdate != luck_info[0]:
            with open(log_path, 'r+') as file:
                file.truncate(0)


# 检测是否重复抽取
async def check_repeat(user_id):
    nowtime = datetime.now()
    nowdate = str(nowtime.date())
    log_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/todaysluck/reply.log'
    with open(log_path, 'r', encoding='utf-8') as file:
        data = file.readlines()
    for log in data:
        if user_id in log:
            log = log.replace('\n', '')
            luck_info = log.split(' ')
            if nowdate != luck_info[0]: return
            today_luck = luck_info[2]
            if today_luck == '寄':
                reply_text = (
                    "你的今日运势如下:\n"
                    f"今日运势: {today_luck}\n"
                    f"诸事不宜, 自求多福吧."
                )
            else:
                do_key = luck_info[3]
                do_text = luck_info[4]
                notdo_key = luck_info[5]
                notdo_text = luck_info[6]
                reply_text = (
                    "今天你已经抽过今日运势了!\n"
                    f"今日运势: {today_luck}\n"
                    f"宜{do_key}: {do_text}\n"
                    f"忌{notdo_key}: {notdo_text}"
                )
            text_message = MessageSegment.text(reply_text)
            mention_message = MessageSegment.mention(user_id=user_id)
            reply_message = Message()
            reply_message.append(mention_message)
            reply_message.append(text_message)
            await todaysluck.finish(reply_message)


@todaysluck.handle()
async def handle_todaysluck(bot: Bot, event: Event):
    await refresh()
    user_id = event.get_user_id()
    await check_repeat(user_id)
    
    luck_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/todaysluck/luck.json'
    with open(luck_path, 'r', encoding='utf-8') as file:
        luck_data = json.load(file)
    luck = luck_data["luck"]
    weights = [0.95, 0.05]
    # 是否为寄
    is_ji = random.choices([False, True], weights)[0]
    todo_data = luck_data["todo"]
    # 从字典中获取左值
    todo_keys = list(todo_data.keys())
    if is_ji:
        today_luck = '寄'
    else:
        today_luck = random.choices(luck)[0]
    # 随机选从key中选
    today_todo_key = random.sample(todo_keys, 2)
    do_key = today_todo_key[0]
    do_text = todo_data[do_key][0]
    notdo_key = today_todo_key[1]
    notdo_text = todo_data[notdo_key][1]

    # write log
    nowtime = datetime.now()
    nowdate = nowtime.date()
    log_text = str(nowdate) + ' ' + user_id
    log_text += ' ' + today_luck
    log_text += ' ' + do_key
    log_text += ' ' + do_text
    log_text += ' ' + notdo_key
    log_text += ' ' + notdo_text + '\n'
    log_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/todaysluck/reply.log'
    with open(log_path, 'a', encoding='utf-8') as file:
        file.write(log_text)

    luck_message = (
            "你的今日运势如下:\n"
            f"今日运势: {today_luck}\n"
            f"宜{do_key}: {do_text}\n"
            f"忌{notdo_key}: {notdo_text}"
        )
    if today_luck == '寄':
        luck_message = (
            "你的今日运势如下:\n"
            f"今日运势: {today_luck}\n"
            f"诸事不宜, 自求多福吧."
        )
    reply_text = MessageSegment.text(luck_message)
    mention_message = MessageSegment.mention(user_id=user_id)
    reply_message = Message()
    reply_message.append(mention_message)
    reply_message.append(reply_text)
    await todaysluck.finish(reply_message)
    


