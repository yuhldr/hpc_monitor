import os
from ylt.utils.my_log import save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails


def getNodes():
    error_str = ""
    code_str = '/usr/local/slurm/bin/sinfo -N  -O "nodelist:.6,available:.6,statelong:.12,cpusstate:.16"'
    str_res = os.popen(code_str).read()
    n = 0
    for line in str_res.strip().split("\n"):
        if (n > 0):
            lines = line.split()
            ss = lines[3].split("/")
            cpus = int(ss[0]) + int(ss[1])
            if (cpus != 144):
                error_str += (line + "\n")

        n += 1
    error_str = error_str.strip()
    return error_str


def main(title="计算节点出问题",
         log_file="nodes.log",
         to_mail_users=["***REMOVED***"]):
    error_str = getNodes()

    # 8小时不重复
    limits_sec_mail_node = 8 * 60 * 60

    if (len(error_str) > 0):
        s = "%s\n\n其他\n%s" % (error_str, os.popen("sinfo-s").read())
        save_log2("%s\n%s" % (title, s), log_file)
        send_mails(title, s, to_mail_users, limits_sec_mail_node)


main()
