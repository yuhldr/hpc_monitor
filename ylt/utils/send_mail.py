import smtplib
from email.mime.text import MIMEText
import ylt.utils.ratelimit_json as rj
from ylt.utils.my_log import save_log2


def send_163mail(subject, content, mail_from_usr, mail_from_usr_pw,
                 mail_to_usr):
    send_mail(subject, content, mail_from_usr, mail_from_usr_pw, mail_to_usr,
              "smtp.163.com")


def send_mails_by_yuh163(subject, content, mail_to_usrs, limit_sec=60):
    user = "***REMOVED***"
    pw = "***REMOVED***"

    for mail_to_usr in mail_to_usrs:
        send_mail(subject,
                  content,
                  user,
                  pw,
                  mail_to_usr,
                  "smtp.163.com",
                  limit_sec=limit_sec)


def send_mail(subject,
              content,
              mail_from_usr,
              mail_from_usr_pw,
              mail_to_usr,
              smtp_server="smtp.qq.com",
              smtp_port=465,
              limit_sec=60):

    # 同一个人，60s内不同发送同一主题的邮件
    rj_key = "%s_%s" % (subject, mail_to_usr)
    overLimit, span_sec = rj.overLimit(rj_key, limit_sec)
    if (not overLimit):
        log_str = "邮件发生太频繁[%.2f/%d]s，本次暂停：\n\n%s\n\n%s\n\n%s\n" % (
            span_sec, limit_sec, subject, mail_to_usr, content)
        save_log2(log_str, "mail.log")

        return

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
        # s = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # # 登录到邮箱
        # s.login(msg_from, passwd)
        # # 发送邮件：发送方，收件方，要发送的消息
        # s.sendmail(msg_from, msg_to, msg.as_string())
        # s.quit()

        rj.saveRecord(rj_key)

        log_str = "成功发送邮件：\n\n%s\n\n%s\n\n%s" % (subject, mail_to_usr, content)
        save_log2(log_str, "mail.log")

        return True
    except Exception as e:
        save_log2("邮件发送失败：\n" + subject + "\n" + content, "mail.log")
        print(e)
    return False
