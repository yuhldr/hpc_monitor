'邮件'
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import ylt.utils.ratelimit_json as rj
from ylt.utils.my_log import save_log2


# pylint: disable=R0913
def send_163mail(subject, content, mail_from_usr,
                 mail_from_usr_pw, mail_to_usr):
    """使用163邮箱发邮件

    Args:
        subject (_type_): _description_
        content (_type_): _description_
        mail_from_usr (_type_): _description_
        mail_from_usr_pw (_type_): _description_
        mail_to_usr (_type_): _description_
    """
    send_mail(subject, content, mail_from_usr, mail_from_usr_pw,
              mail_to_usr, smtp_server="smtp.163.com")


def send_mails_by_yuh163(subject, content, mail_to_usrs: list, limit_sec=60):
    """使用163邮箱发邮件，内置账号

    Args:
        subject (_type_): _description_
        content (_type_): _description_
        mail_to_usrs (_type_): _description_
        limit_sec (int, optional): _description_. Defaults to 60.
    """
    user = "***REMOVED***"
    pw = "***REMOVED***"

    send_mail(subject,
              content,
              user,
              pw,
              mail_to_usrs[0:1],
              mail_to_usrs[1:],
              "smtp.163.com",
              limit_sec=limit_sec)


def mail_limit(all_recipients, subject, limit_sec=60):
    """同一个人，60s内不同发送同一主题的邮件


    Args:
        all_recipients (list): 所有收件人
        subject (_type_): _description_
        limit_sec (int, optional): _description_. Defaults to 60.

    Returns:
        _type_: _description_
    """
    # 同一组人，60s内不同发送同一主题的邮件
    rj_key = f'{subject}_{"_".join(all_recipients)}'

    over_limit, span_sec = rj.over_limit(rj_key, limit_sec)
    if not over_limit:
        log_str = f"邮件发生太频繁[{span_sec}:.2f/{limit_sec}]s，本次暂停：\n\n{subject}\n\n{all_recipients}"
        save_log2(log_str, "mail_limit.log")
        return None

    return rj_key


def send_mail(subject,
              content,
              mail_from_usr,
              mail_from_usr_pw,
              receivers: list,
              cc_recipients=None,
              smtp_server="smtp.qq.com",
              smtp_port=465,
              limit_sec=60,
              sender_name="集群管理员"):
    """发邮件

    Args:
        subject (_type_): _description_
        content (_type_): _description_
        mail_from_usr (_type_): 发件人
        mail_from_usr_pw (_type_): _description_
        receivers (list): 接收人
        cc_recipients (list, optional): 抄送给谁. Defaults to None.
        smtp_server (str, optional): _description_. Defaults to "smtp.qq.com".
        smtp_port (int, optional): _description_. Defaults to 465.
        limit_sec (int, optional): _description_. Defaults to 60.
        sender_name (str, optional): 发件人名字. Defaults to "集群管理员".

    Returns:
        _type_: _description_
    """
    if cc_recipients is None:
        cc_recipients = []

    all_recipients = receivers + cc_recipients

    rj_key = mail_limit(all_recipients, subject, limit_sec)
    if rj_key is None:
        return True

    # 生成一个MIMEText对象（还有一些其它参数）
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = formataddr((sender_name, mail_from_usr))
    msg["To"] = ", ".join(receivers)
    msg["Cc"] = ", ".join(cc_recipients)

    try:
        # 通过ssl方式发送，服务器地址，端口
        s = smtplib.SMTP_SSL(smtp_server, smtp_port)
        # 登录到邮箱
        s.login(mail_from_usr, mail_from_usr_pw)
        # 发送邮件：发送方，收件方，要发送的消息
        s.sendmail(mail_from_usr, all_recipients, msg.as_string())
        s.quit()

        rj.save_record(rj_key)

        save_log2(
            f"成功发送邮件：\n\n{subject}\n\n{all_recipients}\n\n{content}", "mail.log")

        return True
    except Exception as e:  # pylint: disable=w0718
        save_log2(f"邮件发送失败：\n{subject}\n{content}\n{e}", "mail.log")
    return False
