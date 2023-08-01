'''master温度监控'''
import os
import psutil
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails


def get_temp():
    """获取当前温度

    Returns:
        _type_: 每个核心平均温度
    """
    coretemps = psutil.sensors_temperatures()["coretemp"]
    temps = []
    for coretemp in coretemps:
        temps.append(coretemp.current)
    print(temps)

    return sum(temps) / len(temps)


def get_cpu():
    """获取cpu信息，负载大时，温度高正常

    Returns:
        _type_: _description_
    """
    cpus = psutil.cpu_percent(interval=1, percpu=True)
    return sum(cpus) / len(cpus)


def main(to_mail_users,
         title="服务器master温度过高提醒",
         log_file="temp.log"):
    """60s 内不重复发邮件，其实定时任务5分种才一次。。。。

    Args:
        to_mail_users (list): 发给谁
        title (str, optional): 标题. Defaults to "服务器master温度过高提醒".
        log_file (str, optional): 日志文件名. Defaults to "temp.log".
    """
    max_temp = 40
    limits_sec_mail_temp = 60
    temp = get_temp()
    cpu = get_cpu()

    save_log2(f"cpu温度：{temp} 利用率：{cpu}", log_file)

    if ((temp > max_temp and cpu < 10) or temp > 60):
        content = f"当前服务器master CPU利用率{cpu} 温度 {temp} ℃\n\n超过阈值温度 {max_temp} ℃，请尽快处理"
        content += "\n\n当前top：\n" + os.popen('top -bi -n 1 -d 0.02').read()

        send_mails(title, content, to_mail_users, limits_sec_mail_temp)
