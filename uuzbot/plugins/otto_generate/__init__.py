from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.adapters.onebot.v12 import Bot, Event, Message, MessageSegment
from nonebot.params import ArgPlainText, CommandArg

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="otto_generate",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from time import sleep

from selenium.webdriver.edge.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os

run_status = False

async def get_run_status():
    global run_status
    return run_status
    
async def change_run_status():
    global run_status
    if run_status == False:
        run_status = True
    else:
        run_status = False

# 调用爬虫下载音频
async def get_generated_voice(words_text, order):
    # 使用线程池执行Selenium操作
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, run_selenium, words_text, order)
        return result

def run_selenium(words_text, order):
    opt = Options()
    opt.add_experimental_option('detach', True)

    driver = webdriver.Edge(opt)
    wait = WebDriverWait(driver, 20)
    driver.get("https://otto-hzys.huazhiwan.xyz/")

    # 等待输入区域元素加载完成
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-textarea__inner')))
    input_area = driver.find_element(By.CLASS_NAME, 'el-textarea__inner')
    input_area.clear()
    input_area.send_keys(words_text)

    # 等待生成按钮加载完成
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="生成otto鬼叫"]')))
    generate_button = driver.find_element(By.XPATH, '//span[text()="生成otto鬼叫"]')
    generate_button.click()

    # 等待下载按钮加载完成
    sleep(3)
    if order == 0:
        download_button = driver.find_element(By.XPATH, '//span[text()="下载原音频"]')
    elif order == 1:
        download_button = driver.find_element(By.XPATH, '//span[text()="下载倒放音频"]')

    download_button.click()
    sleep(10)
    # 关闭浏览器
    driver.quit()


# 获取下载路径的最新文件
async def get_latest_file(directory):
    # 获取指定目录下的所有文件和目录名
    entries = os.listdir(directory)
    # 过滤出文件，排除目录
    files = [f for f in entries if os.path.isfile(os.path.join(directory, f))]
    # 如果目录为空或没有文件，则返回None
    if not files:
        return None
    # 初始化最新文件和最新时间戳
    latest_file = None
    latest_mtime = 0
    # 遍历文件，比较修改时间
    for file in files:
        file_path = os.path.join(directory, file)
        # 获取文件的修改时间
        mtime = os.path.getmtime(file_path)
        # 如果这个文件的修改时间更近，则更新最新文件和时间戳
        if mtime > latest_mtime:
            latest_mtime = mtime
            latest_file = file
    # 返回最新文件的完整路径
    return os.path.join(directory, latest_file)


# 获取上传到bot服务器的file_id
async def get_file_id(bot, words_text):
    download_path = os.path.join(os.environ['USERPROFILE'], 'Downloads')
    # download_path = 'C:/Users/y1027/Downloads'
    file_path = await get_latest_file(download_path)
    file_path = str(file_path).replace("\\","/")
    print(file_path)
    upload_response = await bot.upload_file(type='path',name=words_text, path=file_path)
    file_id = upload_response['file_id']
    print(file_id)
    return file_id


async def handle_send_generated_voice(bot, event, words_text, order):
    await otto_generate.send("开始生成电棍硅胶, 需要花费时间较长, 请耐心等待")
    await get_generated_voice(words_text, order)
    user_id = event.get_user_id()
    order_text = '' if order == 0 else '倒放'
    print(user_id)
    file_id = await get_file_id(bot, words_text)
    reply_message = Message()
    mention_message = MessageSegment.mention(user_id=user_id)
    voice_message = MessageSegment.file(file_id=file_id)
    text_message = MessageSegment.text(f'你的硅胶{words_text}{order_text}生成完辣!')
    reply_message.append(voice_message)
    reply_message.append(mention_message)
    reply_message.append(text_message)
    # run_status = False
    await change_run_status()
    await otto_generate.finish(reply_message)


otto_generate = on_command("/otto")
@otto_generate.handle()
async def handle_otto_generate(bot: Bot, event = Event, args: Message = CommandArg()):
    # global run_status
    if(await get_run_status() == False): 
        # run_status == True
        await change_run_status()
    else:
        await otto_generate.finish("你先别急, 当前还有其他用户在生成硅胶, 过一会再试吧.")
    args_texts = args.extract_plain_text().split(' ')
    if words_text := args_texts[0]:
        if len(args_texts) == 2 and args_texts[1] == '倒放':
            await handle_send_generated_voice(bot, event, words_text, 1)
            # await otto_generate.finish(f'生成{words_text}倒放.')
        elif len(args_texts) == 1:
            await handle_send_generated_voice(bot, event, words_text, 0)
            # await otto_generate.finish(f'生成{words_text}.')
    # run_status = False
    await change_run_status()

@otto_generate.got("words_text", prompt="请输入要转化的文本")
async def got_generate(bot: Bot, event: Event, words_text: str = ArgPlainText()):
    # global run_status
    # print(run_status)
    if(await get_run_status() == False): 
        # run_status = True
        await change_run_status()
    elif await get_run_status() == True:
        await otto_generate.finish("你先别急, 当前还有其他用户在生成硅胶, 过一会再试吧~")
    print(run_status)
    await handle_send_generated_voice(bot, event, words_text, 0)


