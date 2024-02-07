#! /usr/bin/env python

"""
查看其他节点 top 信息
"""

from jinja2 import Environment, FileSystemLoader

from ylt import path_templates
from ylt.nodes import re_sinfo
from ylt.ns_state import NS_STATE_PATH
from ylt.utils.my_log import getTime


def sinfo2html(text_node="", text_ns="", path="./index.html"):
    """slurm信息
    """
    now_node = getTime(p="%Y/%m/%d %H:%M:%S")
    node_list = []
    for i, line in enumerate(text_node.split("\n")):
        if len(line) == 0:
            continue
        if i == 0:
            print(line)
            continue
        lines = line.split()
        nd = {
            "name": lines[0],
            "partition": lines[1],
            "status": lines[2],
            "memory": lines[3],
            "cpu": lines[4]
        }
        if len(lines) > 5:
            nd["other"] = lines[5]
        node_list.append(nd)

    ns_list = []
    for i, line in enumerate(text_ns.split("\n")):
        if len(line) == 0:
            continue
        if i == 0:
            now_ns = line
            continue
        if i == 1:
            continue
        print(line)
        lines = line.split()
        print(lines)
        ns_list.append({
            "name": lines[0],
            "status": lines[1],
            "memory": lines[2],
            "cpu": lines[3]})

    env = Environment(loader=FileSystemLoader(path_templates))
    template = env.get_template("sinfo_s.html")

    html_output = template.render(
        node_list=node_list, now_node=now_node, ns_list=ns_list, now_ns=now_ns)
    with open(path, 'w', encoding="utf-8") as f:
        f.write(html_output)


def ref_sinfo_s(path="/home/data/www/other/test/sinfo-s/index.html"):
    """直接在网页查看

    Args:
        path (str, optional): _description_. Defaults to "index.html".
    """
    with open(NS_STATE_PATH, "r", encoding="utf-8") as file:
        sinfo2html(re_sinfo(), file.read(), path)
