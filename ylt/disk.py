'''master硬盘占有监控'''
import os
import socket
import subprocess

from ylt import CACHE_DIR
from ylt.utils.my_file import check_dir
from ylt.utils.my_log import getTime, save_log2
from ylt.utils.run_code import run
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails

DISK_PATH = f"{CACHE_DIR}/disk/"
check_dir(DISK_PATH)
DISK_HOME_DODAY_PATH = f'{DISK_PATH}/home_{getTime("%Y_%m_%d")}.txt'
DISK_HOME_TODAY = f"{DISK_PATH}/home_today.txt"

# 磁盘使用率到达多少时体系
warning_disk_home_rates = [80, 90, 95, 98]
# 每隔多少小时提醒
warning_disk_home_times = [
    30 * 24 * 60 * 60, 7 * 24 * 60 * 60, 6 * 60 * 60, 1 * 60 * 60
]
# 提醒内容
warning_disk_home_msgs = [
    "磁盘占用已经到达警戒值，请提醒清理各自空间", "磁盘占用过高！影响服务器性能！，请提醒用户清理各自空间",
    "磁盘占用极高！严重影响服务器性能！，请提醒占用过多的同学，立刻清理、转移数据", "磁盘占用危险！有崩盘风险！，请管理员立刻清理空间"
]


def ref_data():
    """获取用户使用详细信息
    """
    code = f'du -h --max-depth=1  /home |sort -hr > {DISK_HOME_DODAY_PATH}'
    subprocess.call(code, shell=True)
    code_cp = f"rm -f {DISK_HOME_TODAY} && cp {DISK_HOME_DODAY_PATH} {DISK_HOME_TODAY}"
    subprocess.call(code_cp, shell=True)


def get_rate_i(rate_now, rates):
    """_summary_

    Args:
        rate_now (_type_): _description_
        rates (_type_): _description_

    Returns:
        _type_: _description_
    """
    ns_rate = len(rates)
    for n_rate in range(ns_rate):
        n_i = ns_rate - 1 - n_rate
        if rate_now >= rates[n_i]:
            return n_i
    return -1


def main(to_mail_users,
         title="集群磁盘占用提醒",
         log_file="disk_home.log",
         disk_part="/home"):
    """监控master磁盘情况，主要是home

    Args:
        to_mail_users (list): 发给谁
        title (str, optional): _description_. Defaults to "集群磁盘占用提醒".
        log_file (str, optional): _description_. Defaults to "disk_home.log".
        disk_part (str, optional): _description_. Defaults to "/home".
    """

    # 80, 90, 95, 98
    disk_s = run(f'df -h | grep -w "{disk_part}"')

    # disk_data_home = disk_s.replace("25%", "96%").split()
    disk_data_home = disk_s.split()
    rate_now = int(disk_data_home[4].replace("%", ""))
    save_log2(f"分区：{disk_part}，占用率：{rate_now}", log_file)

    ni_rate = get_rate_i(rate_now, warning_disk_home_rates)
    if ni_rate < 0:
        return

    limits_sec = warning_disk_home_times[ni_rate]

    hostname = socket.gethostname()

    mail_title = hostname + "：" + title

    content = warning_disk_home_msgs[ni_rate] + \
        f"\n\n当前磁盘{disk_part}占用 {rate_now}：\n{disk_s}"

    if os.path.exists(DISK_HOME_TODAY):
        content += "\n以下是每个用户详细使用情况：\n\n"
        with open(DISK_HOME_TODAY, "r", encoding="utf-8") as file:
            s_home = file.read()
            content += s_home
    else:
        content += f"详细使用情况请查看 {DISK_HOME_TODAY}"

    send_mails(mail_title, content, to_mail_users, limits_sec)
