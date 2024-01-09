'''获取独立服务器信息'''
import os
from ylt import CACHE_DIR
from ylt.utils.my_log import getTime
from multiprocessing import Pool

NS_STATE_PATH = f'{CACHE_DIR}/ns_state.txt'


def get_cpu(ns_name, cpu_ok_rate=20):
    """_summary_

    Args:
        ns (_type_): _description_
        cpu_ok_rate (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    start = False
    cpu_ok = 0
    cpu_no = 0
    ssh_code = f'ssh {ns_name} "sar -P ALL 1 2"'
    cpu_msg = os.popen(ssh_code).readlines()
    for line in cpu_msg:
        lines = line.strip().split()
        if len(lines) == 0 or lines[0] != "Average:":
            continue
        if lines[1] == "all":
            start = True
            continue

        if start:
            if float(lines[2]) > cpu_ok_rate or float(lines[3]) > cpu_ok_rate:
                cpu_no += 1
            else:
                cpu_ok += 1
    return cpu_ok, cpu_no


def get_mem(ns_name):
    """_summary_

    Args:
        ns (_type_): _description_

    Returns:
        _type_: _description_
    """
    mem_ok = 0
    mem_no = 0
    ssh_code = f'ssh {ns_name} "sar -r 3 2"'
    mem_msg = os.popen(ssh_code).readlines()
    for line in mem_msg:
        lines = line.strip().split()

        if len(lines) != 0 and lines[0] == "Average:":
            mem_ok = float(lines[2])/(1024*1024)
            mem_no = float(lines[3])/(1024*1024)

    return mem_ok, mem_no


def cm2s(param):
    cal_type, sn = param
    if cal_type == "cpu":
        cpu_ok, cpu_no = get_cpu(sn)
        return f"{cpu_ok:3d} /{cpu_ok+cpu_no:3d} {'':8s}"
    else:
        mem_ok, mem_no = get_mem(sn)
        return f"{mem_ok:3.2f} / {mem_no+mem_ok:3.2f}"


def ref_ns_state():
    server_names = ["ns1", "ns2", "ns3", "ns4"]
    ps = []
    for sn in server_names:
        for ct in ["cpu", "mem"]:
            ps.append((ct, sn))

    with Pool(len(server_names)*2) as p:
        dd = p.map(cm2s, ps)

        msg = f'{getTime(p="%Y/%m/%d %H:%M:%S")}\n小服务器     cpu核心数(空闲/总)  内存(可用/总|G)'
        for i, sn in enumerate(server_names):
            msg += f"\n  {sn} {'':8s}"
            msg += dd[i*2]
            msg += dd[i*2+1]

        with open(NS_STATE_PATH, "w", encoding="utf-8") as file:
            file.write(msg+"\n")

