import psutil
import os
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails


def getTemp():
    coretemps = psutil.sensors_temperatures()["coretemp"]
    temps = []
    for coretemp in coretemps:
        temps.append(coretemp.current)
    print(temps)

    return sum(temps) / len(temps)


def getCPU():
    cpus = psutil.cpu_percent(interval=1, percpu=True)
    return sum(cpus) / len(cpus)


# 60s 内不重复发邮件，其实定时任务5分种才一次。。。。
def main(title="服务器master温度过高提醒",
         log_file="temp.log",
         to_mail_users=["***REMOVED***", "***REMOVED***"]):
    max_temp = 40
    limits_sec_mail_temp = 60
    temp = getTemp()
    cpu = getCPU()

    save_log2("cpu温度：%.2f 利用率：%.2f" % (temp, cpu), log_file)

    if ((temp > max_temp and cpu < 10) or temp > 60):
        content = "当前服务器master CPU利用率%.2f 温度 %.2f ℃\n\n超过阈值温度 %.3f ℃，请尽快处理" % (
            cpu, temp, max_temp)
        content += "\n\n当前top：\n" + os.popen('top -bi -n 1 -d 0.02').read()

        send_mails(title, content, to_mail_users, limits_sec_mail_temp)
