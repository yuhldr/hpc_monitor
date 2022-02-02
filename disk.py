import os, json, time
import socket
import utils
import config

disk_part = "/home"
home_user_dir = "/home/data/disk_home"
home_user_path = "%s/home_%s.txt" % (home_user_dir, utils.getTime("%Y-%m-%d"))
log_file_name = "disk_home.log"
config_path = "data/disk_home.json"

utils.make_dir("data")

disk_s = str(os.popen('df -h | grep -w "%s"' % disk_part).readline())
# disk_data_root = str(os.system('df -h | grep /home'))

disk_data_home = disk_s.split()

print(disk_s)
print(home_user_path)

rate_now = int(disk_data_home[4].replace("%", ""))
# rate_now = 98
rates = config.warning_disk_home_rate

last_mail_date = -1
section_mail_date = disk_part + "_mail"
config_data = {section_mail_date: {}}

if os.path.exists(config_path):
    config_data = json.load(open(config_path, "r"))

print(config_data)

hostname = socket.gethostname()
print(hostname)

for n in range(len(rates)):
    i = len(rates) - 1 - n
    if (str(i) in config_data[section_mail_date]):
        last_mail_date = config_data[section_mail_date][str(i)]

    if (rate_now >= rates[i] and utils.get_time_span(last_mail_date) >
            config.warning_disk_home_time[i]):
        title = hostname + "：" + config.warning_disk_home_title[i]

        content = config.warning_disk_home_msg[
            i] + "\n\n当前磁盘%s占用 %d：\n%s\n以下是每个用户详细使用情况：\n\n" % (
                disk_part, rate_now, disk_s)

        if (os.path.exists(home_user_path)):
            with open(home_user_path, "r") as file:
                s = file.read()
                content += s
        else:
            content += "详细使用情况请查看 %s" % home_user_dir


        utils.lzu_send_mails(title, content, config.mail_from_usr,
                             config.mail_from_pw,
                             config.disk_home_warning_to_mails)

        break

with open(config_path, 'w') as file:
    config_data[section_mail_date][str(i)] = time.time()
    json.dump(config_data, file, ensure_ascii=False)

s = "分区：%s，占用率：%d，上次提醒时间：%s，间隔：%s" % (
    disk_part, rate_now, utils.time2str(last_mail_date),
    utils.get_time_friend_span(last_mail_date))
utils.save_log2(s, log_file_name)
