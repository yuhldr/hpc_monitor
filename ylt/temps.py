'''master温度监控'''
import os
import time
from datetime import datetime, timedelta

import psutil

from ylt import CACHE_DIR
from ylt.utils import read_json_file, write_json_file
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails

TEMP_PATH = f'{CACHE_DIR}/temp.json'
DATA_FORMAT = "%Y-%m-%d %H:%M:%S"
K_DATE = "date"
K_CPU = "cpu_rate"
K_TEMP = "temp"


def get_temp():
    """获取当前温度

    Returns:
        _type_: 每个核心平均温度
    """
    coretemps = psutil.sensors_temperatures()["coretemp"]
    temps = []
    for coretemp in coretemps:
        temps.append(coretemp.current)

    return sum(temps) / len(temps)


def get_cpu():
    """获取cpu信息，负载大时，温度高正常

    Returns:
        _type_: _description_
    """
    cpus = psutil.cpu_percent(interval=1, percpu=True)
    return sum(cpus) / len(cpus)


def get_temp_json(temp, cpu_rate, max_elements=43200):
    """获取温度、cpu相关json数据。温度保存30天，文件预计5M大小

    Args:
        temp (_type_): _description_
        cpu_rate (_type_): _description_
        max_elements (int, optional): _description_. Defaults to 100.

    Returns:
        _type_: _description_
    """
    data = read_json_file(TEMP_PATH, [])

    if len(data) > max_elements:
        data = data[-max_elements:]
    current_time = time.strftime(DATA_FORMAT, time.localtime())
    data.append({K_DATE: current_time, K_CPU: cpu_rate, K_TEMP: temp})
    write_json_file(TEMP_PATH, data)
    return data


def cpu_exceeded_threshold(data, threshold=15, time_period=20):
    """最近20分钟内，是否有cpu利用率超过15%

    Args:
        data (_type_): _description_
        threshold (int, optional): _description_. Defaults to 30.
        time_period (int, optional): _description_. Defaults to 10.

    Returns:
        _type_: _description_
    """
    current_time = datetime.now()
    # 遍历数据，仅考虑最近 time_period 内的数据
    # 逆序，最近时间在前
    for entry in reversed(data):
        entry_time = datetime.strptime(entry[K_DATE], DATA_FORMAT)
        if current_time - entry_time > timedelta(minutes=time_period):
            # 如果超过指定时间范围，不再继续遍历
            break

        # 判断CPU使用率是否超过阈值
        if entry[K_CPU] > threshold:
            print(entry)
            return True

    return False


def main(to_mail_users,
         title="服务器master温度过高提醒",
         log_file="temp.log"):
    """监控master的cpu核心温度。60s 内不重复发邮件

    Args:
        to_mail_users (list): 发给谁
        title (str, optional): 标题. Defaults to "服务器master温度过高提醒".
        log_file (str, optional): 日志文件名. Defaults to "temp.log".
    """
    max_temp = 40
    limits_sec_mail_temp = 60
    temp = get_temp()
    cpu = get_cpu()
    flag = "********"

    save_log2(f"cpu温度：{temp} 利用率：{cpu}", log_file)

    data = get_temp_json(temp, cpu)

    if (temp > max_temp and not cpu_exceeded_threshold(data)) or temp > limits_sec_mail_temp:
        d = "时间"
        t = "温度"
        c = "CPU使用率"
        content = f"当前服务器master {t} {temp} {c}{cpu} ℃"
        content += f"\n\n超过阈值温度 {max_temp} ℃，请尽快处理"

        content += f"\n\n\n{flag}  最近几分钟温度  {flag}\n\n{d:<21}{t:<6}{c:<8}\n"
        for e in data[0:20]:
            content += f'{e[K_DATE]:<23}{e[K_TEMP]:<8.2f}{e[K_CPU]:<8.2f}\n'
        content += f"\n\n{flag}  当前top  {flag}\n\n"
        content += os.popen('top -bi -n 1 -d 0.02').read()

        send_mails(title, content, to_mail_users, limits_sec_mail_temp)
