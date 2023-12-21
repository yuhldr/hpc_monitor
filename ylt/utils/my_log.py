import os
import shutil
import time

from ylt import CACHE_DIR, THIS_PATH
from ylt.utils.my_file import check_dir

FILE_MAX_SIZE = 1  # Mb，日志文件多大保存一次
LOG_DIR = THIS_PATH + "/log/"


def save_log2(content_, log_file_name, test=False):
    split_str = "********************"
    content = "%s  %s      %s\n%s\n\n\n" % (split_str, getTime(), split_str,
                                            content_)
    if test:
        print(log_file_name + "\n" + content)
    else:
        save_log(content, log_file_name)


def save_log(content, log_file_name):
    check_dir(LOG_DIR)

    log_file = LOG_DIR + log_file_name

    with open(log_file, 'a', encoding="utf-8") as file:
        file.write(content)

    file_size(log_file)


# M
def file_size(log_file):
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
    return time2str(time.time(), p)


def time2str(time_long, p="%Y_%m_%d-%H_%M_%S"):
    return time.strftime(p, time.localtime(time_long))


def get_time_span(t1, t2=time.time(), unit=UNIT_HOUR):
    return (t2 - t1) / unit


def get_time_friend_span(t1, t2=time.time()):
    span_sec = get_time_span(t1, t2, UNIT_SEC)
    print(span_sec)
    if span_sec < UNIT_MIN:
        return f"{span_sec:.3f} s"
    elif span_sec < UNIT_HOUR:
        return f"{(span_sec / UNIT_MIN):.3f} min"
    elif span_sec < UNIT_DAY:
        return f"{(span_sec / UNIT_HOUR):.3f} h"
    elif span_sec < UNIT_DAY * 30:
        return f"{(span_sec / UNIT_DAY):.3f} d"
    else:
        return time2str(t2)
