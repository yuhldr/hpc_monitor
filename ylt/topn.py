import os
from ylt import cache_dir


TOPS_PATH = f"{cache_dir}/tops/"

if not os.path.exists(TOPS_PATH):
    os.makedirs(TOPS_PATH)


def main(ns=range(14)):
    """获取每个节点的top信息

    Args:
        n (int, optional): _description_. Defaults to 14.
    """
    for i in ns:
        os.popen(f'ssh node{i} "top -b -n 1" > {TOPS_PATH}/topnode{i}')
