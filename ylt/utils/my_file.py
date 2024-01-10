'文件处理'
import os
import time


def del_old_data(path, date_max=31536000):
    """删除超过一定时间的文件

    Args:
        path (str): 路径
        date_max (int, optional): 超过多久就删除. Defaults to 31536000.
    """
    # 获取当前时间戳
    now = time.time()

    # 遍历文件夹中的所有文件
    for filename in os.listdir(path):
        filepath = os.path.join(path, filename)

        # 如果文件是文件夹，跳过
        if os.path.isdir(filepath):
            continue

        # 获取文件创建时间戳
        file_created_time = os.path.getctime(filepath)

        # 如果文件创建时间在一年之前，删除该文件
        if now - file_created_time > date_max:
            os.remove(filepath)


def check_dirs(paths):
    """创建多个文件夹，但是上一级文件夹必须存在

    Args:
        paths (_type_): _description_
    """
    for path in paths:
        check_dir(path)


def check_dir(path):
    """创建多个文件夹，但是上一级文件夹必须存在

    Args:
        paths (list): _description_
    """
    if not os.path.exists(path):
        os.mkdir(path)
