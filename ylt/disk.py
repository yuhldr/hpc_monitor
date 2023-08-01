'''master硬盘占有监控'''
import os
import socket
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails

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
    """磁盘监控主入口

    Args:
        to_mail_users (list): 发给谁
        title (str, optional): _description_. Defaults to "集群磁盘占用提醒".
        log_file (str, optional): _description_. Defaults to "disk_home.log".
        disk_part (str, optional): _description_. Defaults to "/home".
    """
    home_user_dir = "/home/data/disk_home/home_today.txt"

    # 80, 90, 95, 98
    disk_s = str(os.popen(f'df -h | grep -w "{disk_part}"').readline())

    # disk_data_home = disk_s.replace("25%", "96%").split()
    disk_data_home = disk_s.split()

    print(disk_s)

    rate_now = int(disk_data_home[4].replace("%", ""))

    ni_rate = get_rate_i(rate_now, warning_disk_home_rates)

    print(ni_rate)

    if ni_rate < 0:
        return
    limits_sec = warning_disk_home_times[ni_rate]

    hostname = socket.gethostname()

    mail_title = hostname + "：" + title

    content = warning_disk_home_msgs[ni_rate] + \
        f"\n\n当前磁盘{disk_part}占用 {rate_now}：\n{disk_s}"

    if os.path.exists(home_user_dir):
        content += "\n以下是每个用户详细使用情况：\n\n"
        with open(home_user_dir, "r", encoding="utf-8") as file:
            s_home = file.read()
            content += s_home
    else:
        content += f"详细使用情况请查看 {home_user_dir}"

    send_mails(mail_title, content, to_mail_users, limits_sec)

    s_home = f"分区：{disk_part}，占用率：{rate_now}"

    save_log2(s_home, log_file)
