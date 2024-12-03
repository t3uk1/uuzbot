from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
import random as rand

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="random",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

random = on_command("/随个数字")

@random.handle()
async def handle_generate_random():
    random_number = rand.randint(0,100)
    await random.finish(f"{random_number}")
