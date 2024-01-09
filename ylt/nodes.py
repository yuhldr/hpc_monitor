'''
node是否在线，top情况
'''
import os

from ylt import CACHE_DIR
from ylt.utils.my_file import check_dir
from ylt.utils.my_log import save_log2, getTime
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails

CODE_SINFO_S = "/usr/bin/sinfo-s"
# 系统进程不显示
TOP_NO_USER = "root|rpc|ntp|dbus|polkitd|postfix|libstor"
CODE_TOP = f"top -b -n 1 -w 512 | grep -vE {TOP_NO_USER}"


TOPS_PATH = f"{CACHE_DIR}/tops/"
check_dir(TOPS_PATH)


def ref_node_top(ns=range(14)):
    """获取每个节点的top信息

    Args:
        n (int, optional): _description_. Defaults to 14.
    """
    s = getTime(p="%Y_%m_%d-%H_%M_%S")
    for i in ns:
        os.popen(f'echo {s} > {TOPS_PATH}/topnode{i+1}')
        os.popen(f'ssh node{i+1} "{CODE_TOP}" >> {TOPS_PATH}/topnode{i+1}')


def node_ok(lines):
    """接入slurm的这些node1-14是否正常

    Args:
        lines (str): sinfo-s以后每一条信息

    Returns:
        _type_: _description_
    """
    sinfo_s = lines[5].split("/")
    cpus = int(sinfo_s[0]) + int(sinfo_s[1])
    return cpus == int(sinfo_s[3])


def ns_ok(lines):
    """未接入slurm的这些ns1-4是否正常

    Args:
        lines (_type_): _description_

    Returns:
        _type_: _description_
    """
    return lines[3] != 0


def get_nodes():
    """_summary_

    Returns:
        _type_: _description_
    """
    split_ = " "
    error_str = ""
    error_title = ""
    str_res = os.popen(CODE_SINFO_S).read()
    for line in str_res.strip().split("\n"):
        lines = line.split()
        print(lines)
        if len(lines) == 0:
            continue

        if "node" in lines[0] and not node_ok(lines):
            error_str += (line + "\n")
            error_title += lines[0] + split_
            continue

        if "ns" in lines[0] and not ns_ok(lines):
            error_str += (line + "\n")
            error_title += lines[0] + split_
            continue

    error_str = error_str.strip()
    error_title = error_title.strip().replace(split_, "_")
    return error_title, error_str


def main(to_mail_users,
         title="计算节点[%s]出问题",
         log_file="nodes.log"):
    """显示node节点是否出现问题，比如掉线

    Args:
        to_mail_users (_type_): _description_
        title (str, optional): _description_. Defaults to "计算节点[%s]出问题".
        log_file (str, optional): _description_. Defaults to "nodes.log".
    """
    error_title, error_str = get_nodes()

    # 8小时不重复
    limits_sec_mail_node = 8 * 60 * 60

    if len(error_str) > 0:
        title = title % error_title
        notice_msg = f"{error_str}\n\n其他\n{os.popen(CODE_SINFO_S).read()}"
        save_log2(f"{title}\n{notice_msg}", log_file)
        send_mails(title, notice_msg, to_mail_users, limits_sec_mail_node)
