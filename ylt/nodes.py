import os
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails


code_sinfo_s = "/usr/local/bin/sinfo-s"
code_sinfo = '/usr/local/slurm/bin/sinfo -N  -O "nodelist:.6,available:.6,statelong:.12,cpusstate:.16"'


def nodeOk(lines):
    ss = lines[7].split("/")
    cpus = int(ss[0]) + int(ss[1])
    return cpus == 144


def nsOk(lines):
    return lines[3] != 0


def getNodes():
    split_ = " "
    error_str = ""
    error_title = ""
    str_res = os.popen(code_sinfo_s).read()
    n = 0
    for line in str_res.strip().split("\n"):
        lines = line.split()
        print(lines)
        if len(lines) == 0:
            continue

        if "node" in lines[0] and not nodeOk(lines):
            error_str += (line + "\n")
            error_title += lines[0] + split_
            continue

        if "ns" in lines[0] and not nsOk(lines):
            error_str += (line + "\n")
            error_title += lines[0] + split_
            continue

        n += 1
    error_str = error_str.strip()
    error_title = error_title.strip().replace(split_, "_")
    return error_title, error_str


def main(title="计算节点[%s]出问题",
         log_file="nodes.log",
         to_mail_users=["***REMOVED***"]):
    error_title, error_str = getNodes()

    # 8小时不重复
    limits_sec_mail_node = 1 * 60 * 60

    if (len(error_str) > 0):
        title = title % error_title
        s = "%s\n\n其他\n%s" % (error_str, os.popen(code_sinfo_s).read())
        save_log2("%s\n%s" % (title, s), log_file)
        send_mails(title, s, to_mail_users, limits_sec_mail_node)
