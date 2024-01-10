'保存日志'
import os
import shutil
import time

from ylt import CACHE_DIR, THIS_PATH
from ylt.utils.my_file import check_dir

FILE_MAX_SIZE = 1  # Mb，日志文件多大保存一次
LOG_DIR = THIS_PATH + "/log/"


def save_log2(content_, log_file_name, test=False):
    """保存日志，可以测试

    Args:
        content_ (_type_): _description_
        log_file_name (_type_): _description_
        test (bool, optional): _description_. Defaults to False.
    """
    split_str = "********************"
    content = f'{split_str:22}{getTime()}{"":5}{split_str}\n{content_}\n\n\n'
    if test:
        print(log_file_name + "\n" + content)
    else:
        save_log(content, log_file_name)


def save_log(content, log_file_name):
    """保存日志

    Args:
        content (_type_): _description_
        log_file_name (_type_): _description_
    """
    check_dir(LOG_DIR)

    log_file = LOG_DIR + log_file_name

    with open(log_file, 'a', encoding="utf-8") as file:
        file.write(content)

    file_size(log_file)


# M
def file_size(log_file):
    """文件大小

    Args:
        log_file (_type_): _description_

    Returns:
        _type_: _description_
    """
    log_name = os.path.split(log_file)[1].replace(".log", "")
    ip_cache_dir_ = f"{CACHE_DIR}/{log_name}/"
    check_dir(ip_cache_dir_)

    fsize = os.path.getsize(log_file) / float(1024 * 1024)

    if fsize > FILE_MAX_SIZE:
        shutil.move(log_file, f"{ip_cache_dir_}/{getTime()}.log")
    return fsize


UNIT_SEC = 1
UNIT_MIN = 60
UNIT_HOUR = UNIT_MIN * 60
UNIT_DAY = 24 * UNIT_HOUR


def getTime(p="%Y_%m_%d-%H_%M_%S"):
    """当前时间

    Args:
        p (str, optional): _description_. Defaults to "%Y_%m_%d-%H_%M_%S".

    Returns:
        _type_: _description_
    """
    return time2str(time.time(), p)


def time2str(time_long, p="%Y_%m_%d-%H_%M_%S"):
    """时间转字符串

    Args:
        time_long (_type_): _description_
        p (str, optional): _description_. Defaults to "%Y_%m_%d-%H_%M_%S".

    Returns:
        _type_: _description_
    """
    return time.strftime(p, time.localtime(time_long))


def get_time_span(t1, t2=time.time(), unit=UNIT_HOUR):
    """时间间隔

    Args:
        t1 (_type_): _description_
        t2 (_type_, optional): _description_. Defaults to time.time().
        unit (_type_, optional): _description_. Defaults to UNIT_HOUR.

    Returns:
        _type_: _description_
    """
    return (t2 - t1) / unit


def get_time_friend_span(t1, t2=time.time()):
    """友好的时间间隔说明

    Args:
        t1 (_type_): _description_
        t2 (_type_, optional): _description_. Defaults to time.time().

    Returns:
        _type_: _description_
    """
    span_sec = get_time_span(t1, t2, UNIT_SEC)
    if span_sec < UNIT_MIN:
        return f"{span_sec:.3f} s"
    if span_sec < UNIT_HOUR:
        return f"{(span_sec / UNIT_MIN):.3f} min"
    if span_sec < UNIT_DAY:
        return f"{(span_sec / UNIT_HOUR):.3f} h"
    if span_sec < UNIT_DAY * 30:
        return f"{(span_sec / UNIT_DAY):.3f} d"

    return time2str(t2)
