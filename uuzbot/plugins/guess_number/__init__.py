from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
from nonebot.params import ArgPlainText, CommandArg
from nonebot.matcher import Matcher
from nonebot.typing import T_State
import random

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="guess_number",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

random_number = 0

# TODO
# 要加锁
# 参数上限的限制判断
guessnum = on_command("/猜数字")

async def generate_random_number(state: T_State, range = 100):
    global random_number
    # print(range)
    random_number = random.randint(0, range)
    print(random_number)
    await guessnum.send(f"开始猜数字, 猜数范围为0-{range}.\n输入  /不玩了  退出游戏.")

@guessnum.handle()
async def handle_guessnum(event: Event, args: Message = CommandArg()):
    # args中的CommandArg为/命令后跟的参数
    args_texts = args.extract_plain_text().split(' ')
    print(len(args_texts))
    if args_texts[0] == '':
        await generate_random_number(T_State())
    elif len(args_texts) == 1:
        range = int(args_texts[0])
        await generate_random_number(T_State(), range)

        

@guessnum.got("msg", prompt="请输入数字")
async def got_guessnum(event: Event,state: T_State, msg: str = ArgPlainText()):
    global random_number
    print('111' + msg)
    if msg == '/不玩了':
        await guessnum.send("不是哥们，这都猜不中？")
        await guessnum.finish(f"答案是{random_number}.")

    num = msg
    guess = int(num)
    if guess == random_number:
        user_id = event.get_user_id()
        finish_message = Message()
        mention_message = MessageSegment.mention(user_id=user_id)
        finish_message.append(MessageSegment.text("666, "))
        finish_message.append(mention_message)
        finish_message.append(MessageSegment.text("这个入猜对辣!"))
        await guessnum.finish(finish_message)
    elif guess < random_number:
        await guessnum.reject("小了!")
    else:
        await guessnum.reject("大了!")
    





