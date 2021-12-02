import os
import shutil
import time
from dateutil.parser import parse
import requests
import hashlib

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import sys

file_max_size = 1  # Mb，日志文件多大保存一次
# 可以保证在任何路径运行，都获取到正确的路径
os.chdir(sys.path[0])
cache_dir = os.path.abspath(".") + "/cache"
log_dir = os.path.abspath(".") + "/log"

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

# ============ time ========

# ============ log =========


def get_day_of_month():
    """
    获取指定的某天是某个月的第几周
    周一为一周的开始
    实现思路：就是计算当天在本年的第y周，本月一1号在本年的第x周，然后求差即可。
    因为查阅python的系统库可以得知：

    """

    end = int(time.strftime("%d"))

    return end


# 生成MD5


def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()

    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))

    md5 = hl.hexdigest()

    print('MD5加密前为 ：' + str)
    print('MD5加密后为 ：' + md5)

    return md5


def save_log2(content_, log_file_name, test=False):
    content = "********************  " + getTime(
    ) + "  ********************" + "\n" + str(content_) + "\n\n\n"
    if test:
        print(log_file_name + "\n" + content)
    else:
        save_log(content, log_file_name)


def save_log(content, log_file_name):
    make_dir(log_dir)

    log_file = log_dir + "/" + log_file_name

    # 每次获取现在的ip，都把文件中的上次ip更新一下
    with open(log_file, 'a') as file:
        file.write(content)

    file_size(log_file)


# M
def file_size(log_file):
    log_name = os.path.split(log_file)[1].replace(".log", "")
    ip_cache_dir_ = cache_dir + "/" + log_name
    make_dir(ip_cache_dir_)

    fsize = os.path.getsize(log_file) / float(1024 * 1024)

    if fsize > file_max_size:
        shutil.move(log_file, ip_cache_dir_ + "/" + getTime() + ".log")
    return fsize


def getTime(p="%Y_%m_%d-%H_%M_%S"):
    return time2str(time.time(), p)


def time2str(time_long, p="%Y_%m_%d-%H_%M_%S"):
    return time.strftime(p, time.localtime(time_long))


unit_sec = 1
unit_min = 60
unit_hour = unit_min * 60
unit_day = 24 * unit_hour


def get_time_span(t1, t2=time.time(), unit=unit_hour):
    return (t2 - t1) / unit


def get_time_friend_span(t1, t2=time.time()):
    span_sec = get_time_span(t1, t2, unit_sec)
    print(span_sec)
    if (span_sec < unit_min):
        return "%.3f s" % span_sec
    elif (span_sec < unit_hour):
        return "%.3f min" % (span_sec / unit_min)
    elif (span_sec < unit_day):
        return "%.3f h" % (span_sec / unit_hour)
    elif (span_sec < unit_day * 30):
        return "%.3f d" % (span_sec / unit_day)
    else:
        return time2str(t2)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


# 邮件主题，邮件内容，发信人账号（兰大邮箱），发信人密码（兰大邮箱），收信人（建议QQ邮箱）


def lzu_send_mails(subject, content, mail_from_usr, mail_from_usr_pw,
                   mail_to_usrs):
    send_mails(subject, content, mail_from_usr, mail_from_usr_pw, mail_to_usrs,
               "smtp.lzu.edu.cn")


def send_mails(subject,
               content,
               mail_from_usr,
               mail_from_usr_pw,
               mail_to_usrs,
               smtp_server="smtp.qq.com",
               smtp_port=465):
    mail_to_usrs_text = ""
    for mail_to_usr in mail_to_usrs:
        msg_from = mail_from_usr  # 发送方邮箱
        passwd = mail_from_usr_pw  # 填入发送方邮箱的授权码(填入自己的授权码，相当于邮箱密码)
        # msg_to = ['****@qq.com','**@163.com','*****@163.com']  # 收件人邮箱
        msg_to = mail_to_usr  # 收件人邮箱

        # 生成一个MIMEText对象（还有一些其它参数）
        msg = MIMEText(content)
        # 放入邮件主题
        msg['Subject'] = subject
        # 也可以这样传参
        # msg['Subject'] = Header(subject, 'utf-8')
        # 放入发件人
        msg['From'] = msg_from
        # 放入收件人
        # msg['To'] = '***REMOVED***'
        # msg['To'] = '发给你的邮件啊'
        print("发送中……")
        try:
            # 通过ssl方式发送，服务器地址，端口
            s = smtplib.SMTP_SSL(smtp_server, smtp_port)
            # 登录到邮箱
            s.login(msg_from, passwd)
            # 发送邮件：发送方，收件方，要发送的消息
            s.sendmail(msg_from, msg_to, msg.as_string())
            s.quit()
            print('成功')
            mail_to_usrs_text += mail_to_usr + "、"
        except Exception as e:
            save_log2("邮件发送%s失败：%s\n%s\n" + (mail_to_usr, subject, content),
                      "mail.log", False)
            print(e)

    save_log2(
        "成功发送邮件：\n%s\n%s\n发信人：%s  收信人：%s" %
        (subject, content, mail_from_usr, mail_to_usrs_text), "mail.log",
        False)
