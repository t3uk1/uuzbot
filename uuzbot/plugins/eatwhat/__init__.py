from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
import os
import random
import json

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="eatWhat",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

eatWhat = on_command("/吃什么")
@eatWhat.handle()
async def handle_eatWhat():
    # 改成相对路径
    food_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/eatwhat/food.json'
    # print(food_path)
    # food_path = "C:/Users/y1027/Desktop/bot/uuzbot/uuzbot/plugins/eatwhat/food.txt"
    with open(food_path, 'r', encoding='utf-8') as file:
        food_items = json.load(file)["food"]
    # food_items = [id.strip() for id in food_items]
    random_food = random.choice(food_items)
    # print(random_food)
    await eatWhat.finish(random_food)


drinkwhat = on_command("喝什么")
@drinkwhat.handle()
async def handle_drinkwhat():
    drink_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/eatwhat/food.json'
    with open(drink_path, 'r', encoding='utf-8') as file:
        drink_items = json.load(file)["drink"]
    random_drink = random.choice(drink_items)
    await drinkwhat.finish(random_drink)
