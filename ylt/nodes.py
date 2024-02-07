'''
node是否在线，top情况
'''
import os
import re
from multiprocessing import Pool

from ylt import CACHE_DIR
from ylt.utils.my_file import check_dir
from ylt.utils.my_log import getTime, save_log2
from ylt.utils.send_mail import send_mails_by_yuh163 as send_mails

CODE_SINFO_S = "/usr/bin/sinfo-s"
CODE_SINFO = "/usr/local/slurm/bin/sinfo"
CODE_SINFO_OK = f"{CODE_SINFO} -N -O cpusstate"
ARG_SINFO = "nodelist,partition,available,statelong,memory,allocmem,freemem,cpusstate,Reason:.100"
# 系统进程不显示
TOP_NO_USER = "root|rpc|ntp|dbus|polkitd|postfix|libstor|systemd|syslog|munge"
CODE_TOP = f"top -b -n 1 -w 512 | grep -vE '{TOP_NO_USER}'"


TOPS_PATH = f"{CACHE_DIR}/tops/"
check_dir(TOPS_PATH)


TRS = {
    "up": "在线",
    "down": "掉线",
    "allocated": "繁忙",
    "draining": "暂停",
    "drained": "暂停",
    "mixed": "有空闲",
    "idle": "空闲",
    "none": "",
    "*": "",
}


def t(s):
    """汉化

    Args:
        s (_type_): _description_

    Returns:
        _type_: _description_
    """
    for k, v in TRS.items():
        s = s.replace(k, v)
    return s


def re_sinfo():
    """获取所有节点的slurm状态

    Returns:
        _type_: _description_
    """

    po = os.popen(f'{CODE_SINFO} -N -O "{ARG_SINFO}"')
    ss = po.buffer.read().decode('utf-8', errors='ignore').strip()

    sts = f' {"节点":5}{"分区":5}{"说明":7}{"内存:空/总":8}{"CPU:空/总":9}其他'
    for line in ss.strip().split("\n")[1:]:
        if len(line) == 0:
            continue
        ws = re.split(r'\s{2,}', line)

        sts += f"\n{ws[0]:8}{ws[1]:7}"

        w_state = t(ws[3])
        width = 14
        padding = (
            width - len(w_state.encode('utf-8').decode('unicode_escape'))) // 2
        if w_state == "暂停提交":
            padding -= 1
        sts += f'{w_state}{padding*" "}'

        sts += f'{f"{(int(ws[4])-int(ws[5]))/1024:>4.1f}/{int(ws[4])/1024:<4.0f}":^11}'

        cs = ws[7].split("/")
        sts += f'{f"{cs[1]:>4}/{cs[3]:<5}":^12}'

        sts += t(ws[8])

    return sts


def get_top(node_n: int):
    """获取某个节点top信息

    Args:
        node_n (int): _description_
    """
    n = f"node{node_n+1}"
    s = os.popen(f'ssh {n} "{CODE_TOP}"').read()
    st = f'××××× 节点 {n} 刷新时间: {getTime(p="%Y_%m_%d-%H_%M_%S")} ×××××'
    os.popen(f'echo "{st}\n\n{s}\n{st}" > {TOPS_PATH}/top{n}')


def ref_node_top(ns=range(14)):
    """获取每个节点的top信息

    Args:
        n (int, optional): _description_. Defaults to 14.
    """
    with Pool(len(ns)) as p:
        p.map(get_top, ns)


def node_ok(lines):
    """接入slurm的这些node1-14是否正常

    Args:
        lines (str): sinfo-s以后每一条信息

    Returns:
        _type_: _description_
    """
    return lines[2] != "掉线"


def ns_ok(lines):
    """未接入slurm的这些ns1-4是否正常

    Args:
        lines (_type_): _description_

    Returns:
        _type_: _description_
    """
    return lines[1] != "掉线"


def get_nodes():
    """_summary_

    Returns:
        _type_: _description_
    """
    split_ = " "
    error_str = ""
    error_title = ""
    for line in re_sinfo().strip().split("\n"):
        lines = line.split()
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
        notice_msg = f"{error_str}\n\n其他\n{re_sinfo()}"
        save_log2(f"{title}\n{notice_msg}", log_file)
        send_mails(title, notice_msg, to_mail_users, limits_sec_mail_node)
