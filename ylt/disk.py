import os
import socket
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails


# 磁盘使用率到达多少时体系
warning_disk_home_rates = [80, 90, 95, 98]
# 每隔多少小时提醒
warning_disk_home_times = [30*24*60*60, 7*24*60*60, 6*60*60, 1*60*60]
# 提醒内容
warning_disk_home_msgs = [
    "磁盘占用已经到达警戒值，请提醒清理各自空间",
    "磁盘占用过高！影响服务器性能！，请提醒用户清理各自空间", "磁盘占用极高！严重影响服务器性能！，请提醒占用过多的同学，立刻清理、转移数据",
    "磁盘占用危险！有崩盘风险！，请管理员立刻清理空间"
]


def get_rate_i(rate_now, rates):
    ns = len(rates)
    for n in range(ns):
        ni = ns - 1 - n
        if (rate_now >= rates[ni]):
            return ni
    return -1


def main(title="集群磁盘占用提醒",
         log_file="disk_home.log",
         to_mail_users=["***REMOVED***", "***REMOVED***", "***REMOVED***"],
         disk_part="/home"):
    home_user_dir = "/home/data/disk_home/home_today.txt"

    # 80, 90, 95, 98
    disk_s = str(os.popen('df -h | grep -w "%s"' % disk_part).readline())

    # disk_data_home = disk_s.replace("25%", "96%").split()
    disk_data_home = disk_s.split()

    print(disk_s)

    rate_now = int(disk_data_home[4].replace("%", ""))

    ni = get_rate_i(rate_now, warning_disk_home_rates)

    print(ni)

    if ni < 0:
        return
    limits_sec = warning_disk_home_times[ni]

    hostname = socket.gethostname()

    mail_title = hostname + "：" + title

    content = warning_disk_home_msgs[ni] + \
        "\n\n当前磁盘%s占用 %d：\n%s" % (disk_part, rate_now, disk_s)

    if (os.path.exists(home_user_dir)):
        content += "\n以下是每个用户详细使用情况：\n\n"
        with open(home_user_dir, "r") as file:
            s = file.read()
            content += s
    else:
        content += "详细使用情况请查看 %s" % home_user_dir

    send_mails(mail_title, content, to_mail_users, limits_sec)

    s = "分区：%s，占用率：%d" % (disk_part, rate_now)

    save_log2(s, log_file)
