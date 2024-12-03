from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot import on_notice
from nonebot.rule import to_me
from nonebot.adapters.onebot.v12 import Bot, Event, NoticeEvent, Message, MessageSegment
import json
import os
import re



from .config import Config

__plugin_meta__ = PluginMetadata(
    name="autoreply",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# keywords和valid_commands存在当前目录json里
def load_config():
    config_json_path =  os.getcwd().replace('\\', '/') + '/uuzbot/plugins/autoreply/config.json'
    with open(config_json_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    return config_data
config_data = load_config()
keywords = config_data['keywords']
valid_commands = config_data['valid_commands']
white_list = config_data['white_list']

auto_reply = on_message()
@auto_reply.handle()
async def handle_autoreply(bot: Bot, event: Event):
    if event.get_user_id() == "wxid_czeabjvsc9a729":
        return
    # print(keywords, valid_commands)
    message = event.get_message()
    message_text = str(message)
    reply_text = keywords.get(message_text)

    # handle maimai auto reply
    maip_user_ids = ['wxid_xxx']
    check_keys = ["pc","😉", "出勤", "推分", "hp", "wx", "lh", "yk", "米", "买币", "买点币", "有币吗", "堵门", "几卡", "底力", "mai", "没带手套", "舞萌", "一粉", "鸟了", "绝赞"]
    event_user_id = event.get_user_id()
    # 去掉@用户部分
    cleaned_text = re.sub(r'\[mention:.*?\]', '', message_text)
    # 去掉表情
    cleaned_text = re.sub(r'\[wx.emoji:.*?\]', '', cleaned_text)
    print(event_user_id)
    is_maip_message_send = False
    for maip_user_id in maip_user_ids:
        if is_maip_message_send:
            break
        if maip_user_id == event_user_id:
            for key in check_keys:
                if key in cleaned_text:
                    print(key, cleaned_text)
                    await auto_reply.send("唉,maip")
                    is_maip_message_send = True
                    break

    
    # 识别命令
    if message_text.startswith('/'):
        # 命令存在带参数的情况，只检测前缀
        command = message_text.split(' ')[0].lstrip('/')
        exist = False
        print(valid_commands)
        for valid_command in valid_commands:
            if command == valid_command:
                exist = True 

        # 其它bot的命令
        for white_command in white_list:
            if command == white_command:
                exist = True
                
        invalid_command_text = '命令被我吃掉了!'
        print_help = '发送/help查看命令捏'
        if exist == False:
            await auto_reply.send(invalid_command_text)
            await auto_reply.send(print_help)

    print(reply_text)
    # 检测文本匹配
    for keyword, reply_text in keywords.items():
       if keyword in message_text:
           if keyword == '复读': reply_text = message_text
           await auto_reply.send(reply_text)  
           return
    

# handle @
# notice = on_notice(rule=to_me())
# @notice.handle()
# async def handle_group_at(bot: Bot, event: NoticeEvent):
#     await notice.send("艾特我干啥?")