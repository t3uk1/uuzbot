from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
from nonebot.params import ArgPlainText, CommandArg
from nonebot import on_command
import os
import random
import json

from PIL import Image

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="chouka",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# TODO 
# 其他更多抽卡功能有空再说

star_rail = on_command("/星铁抽卡")

# 控制用户查询状态
star_rail_run_list = []
async def add_star_rail_user(user_id):
    star_rail_run_list.append(user_id)

async def remove_star_rail_user(user_id):
    star_rail_run_list.remove(user_id)

async def find_image(dir_path, image_name):
    images = os.listdir(dir_path)
    for image in images:
        if image_name in image:
            return os.path.join(dir_path, image)
        

async def make_ten_times(image_path_list,user_id,times):
    sample_image = Image.open(image_path_list[0])
    height = sample_image.height * 2 + 20
    width = sample_image.width * 5 + 50

    new_image = Image.new('RGBA', (width, height), (18, 25, 45, 1))
    for i in range(5):
        image = Image.open(image_path_list[i])
        new_image.paste(image, ((image.width + 10) * i, 0))
    for i in range(5):
        image = Image.open(image_path_list[i+5])
        new_image.paste(image, ((image.width + 10) * i, image.height + 20))
    tmp_path = os.getcwd().replace('\\', '/') + f'/uuzbot/plugins/chouka/images/starrail/十连/{user_id}-{times}-十连.png'
    new_image.save(tmp_path)
    return tmp_path

@star_rail.handle()
async def handle_star_rail(bot: Bot, event: Event,args: Message = CommandArg()):
    rank = ["3", "4", "5"]
    # 载入角色数据
    star_rail_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/chouka/starrail.json'
    with open(star_rail_path, 'r', encoding='utf-8') as file:
        star_rail_data = json.load(file)
    data = {
        "3": [],
        "4": [],
        "5": []
    }
    for rare in star_rail_data['chara']:
        for chara in star_rail_data['chara'][rare]:
            data[rare].append(chara)
    for rare in star_rail_data['weapon']:
        for weapon in star_rail_data['weapon'][rare]:
            data[rare].append(weapon)
    weights = [93.3, 5.1, 0.6]

    user_id = event.get_user_id()
    # 添加用户查询状态
    for user in star_rail_run_list:
        if user_id == user:
            await star_rail.finish("当前已经有正在生成的十连, 等等再抽捏")
    await add_star_rail_user(user_id)
    # 抽卡计数
    times = total_times = gold_counts = 0
    star_rail_log_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/chouka/starrail.log'
    images_path =  os.getcwd().replace('\\', '/') + '/uuzbot/plugins/chouka/images'
    with open(star_rail_log_path, 'r', encoding='utf-8') as f:
        log_data = f.readlines()
    for log in log_data:
        if user_id in log:
            total_times = int(log.split(' ')[1])
            times = int(log.split(' ')[2])
            gold_counts = int(log.split(' ')[3])

    args_texts = args.extract_plain_text().split(' ')
    # 单抽
    if args_texts[0] == '单抽' or args_texts[0] == '':
        times += 1
        total_times += 1
        rank_result = random.choices(rank, weights)[0]
        # 保底设置，但没加清空保底状态
        if times % 90 == 0:
            rank_result = '5'
        elif times % 10 == 0:
            rank_result = '4'
        if rank_result == '5':
            # 出金要改回原来的概率
            weights[2] = 0.6
            has_rare = True
            # 开启新的一轮保底计数
            gold_counts += 1
            times = 0
        item = random.choice(data[rank_result])          
        # 查找图片
        image_dir = images_path + '/starrail/' + rank_result + '星/'
        image_path = await find_image(image_dir, item)
        # print(image_path)
        upload_response = await bot.upload_file(type='path',name='1', path=image_path)
        reply_file_id = upload_response['file_id']
        # 记录和更新抽卡次数(总抽数/当前轮次抽数)
        # 单抽直接更新total_times即可，出金开启新的轮次times也是0不影响结果
        now_log = f"{user_id} {str(total_times)} {str(times)} {str(gold_counts)}\n"
        # print(user_id + ': '+ item)
        with open(star_rail_log_path, 'w', encoding='utf-8') as f:
            # 前面read的log_data
            for log in log_data:
                if user_id in log:
                    log = now_log
                f.write(log)
            if total_times == 1:
                f.write(now_log)
    # 十连
    elif args_texts[0] == '十连':
        # 是否有5星
        has_rare = False
        image_path_list = []
        for i in range(10):
            # times和total_times每次同步+1
            times += 1
            total_times += 1
            # 软保底
            if (times % 90) > 70 and has_rare == False:
                up_rate = (times-70) * 6
                weights[2] = 0.6 + up_rate
            rank_result = random.choices(rank, weights)[0]
            # 硬保底设置
            if times % 90 == 0:
                rank_result = '5'
            elif times % 10 == 0:
                rank_result = '4'
            if rank_result == '5':
                # 出金要改回原来的概率
                weights[2] = 0.6
                has_rare = True
                # 开启新的一轮保底计数
                gold_counts += 1
                times = 0
                
            item = random.choice(data[rank_result])
            # 查找图片
            image_dir = images_path + '/starrail/' + rank_result + '星/'
            image_path = await find_image(image_dir, item)
            image_path_list.append(image_path)
        ten_image_path = await make_ten_times(image_path_list,user_id,times)
        upload_response = await bot.upload_file(type='path',name='1', path=ten_image_path)
        reply_file_id = upload_response['file_id']

        # 记录和更新抽卡次数
        now_log = f"{user_id} {str(total_times)} {str(times)} {str(gold_counts)}\n"
        # print(now_log)
        with open(star_rail_log_path, 'w', encoding='utf-8') as f:
            # 前面read的log_data
            for log in log_data:
                if user_id in log:
                    log = now_log
                f.write(log)
            if total_times == 10:
                f.write(now_log)
    elif  args_texts[0] == 'howmany':
        reply_message = Message()
        reply_message.append(MessageSegment.mention(user_id=user_id))
        if times == 0:
            reply_text = MessageSegment.text("你还没有抽过卡哦")
        else:
            reply_text = MessageSegment.text(f"你已经抽了{total_times}发了捏, 共出了{gold_counts}个金!距离下次保底约有{90-times}抽.")
        reply_message.append(reply_text)
        await remove_star_rail_user(user_id)
        await star_rail.finish(reply_message)
    else:
        await remove_star_rail_user(user_id) 
        await star_rail.finish("参数错误")
    result_message = Message()
    mention_message = MessageSegment.mention(user_id=user_id)
    image_message = MessageSegment.image(reply_file_id)
    result_message.append(mention_message)
    result_message.append(image_message)
    # 移除占用状态
    await remove_star_rail_user(user_id)
    await star_rail.send(result_message)


# 碧蓝航线抽卡
azure_lane = on_command("/碧蓝航线抽卡")

@azure_lane.handle()
async def handle_azure_lane(bot: Bot, event: Event,args: Message = CommandArg()):
    rank = ["ur", "ssr", "sr", "r", "n"]
    rank_dict = {
        "ur": "**UR**",
        "ssr": "SSR",
        "sr": "SR",
        "r": "R",
        "n": "N"
    }
    weights = [1.2, 7, 12, 51, 28.8]
    result = '你的抽卡结果如下:\n'

    azure_lane_chara_path = os.getcwd().replace('\\', '/') + '/uuzbot/plugins/chouka/azure_lane.json'
    with open(azure_lane_chara_path, 'r', encoding='utf-8') as file:
        chara_data = json.load(file)

    args_texts = args.extract_plain_text().split(' ')
    if args_texts[0] == '单抽' or args_texts[0] == '':
        rank_result = random.choices(rank, weights)[0]
        chara_rank = rank_dict[rank_result]
        chara_name = random.choice(chara_data[rank_result])
        left_len = len(chara_rank)
        right_len = len(chara_name)
        result += f"{chara_rank:<{left_len}}    {chara_name:<{right_len}}"
    elif args_texts[0] == '十连':
        result_data = []
        max_left_len = 0
        max_right_len = 0
        assign_text = "这把手气不是很好啊, 再抽一次试试?"
        has_ur = False
        for i in range(10):
            rank_result = random.choices(rank, weights)[0]
            if rank_result == 'ur':
                assign_text = "666, 这个入抽到彩船了."
                has_ur = True
            elif rank_result == 'ssr' and has_ur == False:
                assign_text = "手气还行, 再接再励."
            chara_rank = rank_dict[rank_result]
            chara_name = random.choice(chara_data[rank_result])
            left_len = len(chara_rank)
            right_len = len(chara_name)
            max_left_len = max(max_left_len, left_len)
            max_right_len = max(max_right_len, right_len)
            result_data.append(chara_rank + ' ' + chara_name)
        print(max_left_len)
        for simple_result in result_data:
            simple_result = simple_result.split(' ')
            chara_rank, chara_name = simple_result[0], simple_result[1]
            result += f"{chara_rank:<{max_left_len+8}}{chara_name:<{max_right_len}}\n"
        result += assign_text
    else:
        await azure_lane.finish("参数错误")
        
    user_id = event.get_user_id()
    result_message = Message()
    mention_message = MessageSegment.mention(user_id=user_id)
    reply_message = MessageSegment.text(result)
    result_message.append(mention_message)
    result_message.append(reply_message)
    await azure_lane.send(result_message)


# wtf_is_this = on_command("/???抽卡")

# @wtf_is_this.handle()
# async def handle_wtf(bot: Bot, event: Event,args: Message = CommandArg()):
#     rank = []
