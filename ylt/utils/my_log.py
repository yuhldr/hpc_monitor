import os
import shutil
import time

cache_dir = os.path.abspath('.') + "/cache"

file_max_size = 1  # Mb，日志文件多大保存一次
log_dir = os.path.abspath('.') + "/log"


def save_log2(content_, log_file_name, test=False):
    split_str = "********************"
    content = "%s  %s      %s\n%s\n\n\n" % (split_str, getTime(), split_str,
                                            content_)
    if test:
        print(log_file_name + "\n" + content)
    else:
        save_log(content, log_file_name)


def save_log(content, log_file_name):
    make_dir(log_dir)

    log_file = log_dir + "/" + log_file_name

    with open(log_file, 'a') as file:
        file.write(content)

    file_size(log_file)


# M
def file_size(log_file):
    log_name = os.path.split(log_file)[1].replace(".log", "")
    ip_cache_dir_ = cache_dir + "/" + log_name
    make_dir(ip_cache_dir_)

    fsize = os.path.getsize(log_file) / float(1024 * 1024)

    if fsize > file_max_size:
        shutil.move(log_file, ip_cache_dir_ + "/" + getTime() + ".log")
    return fsize


unit_sec = 1
unit_min = 60
unit_hour = unit_min * 60
unit_day = 24 * unit_hour


def getTime(p="%Y_%m_%d-%H_%M_%S"):
    return time2str(time.time(), p)


def time2str(time_long, p="%Y_%m_%d-%H_%M_%S"):
    return time.strftime(p, time.localtime(time_long))


def get_time_span(t1, t2=time.time(), unit=unit_hour):
    return (t2 - t1) / unit


def get_time_friend_span(t1, t2=time.time()):
    span_sec = get_time_span(t1, t2, unit_sec)
    print(span_sec)
    if (span_sec < unit_min):
        return "%.3f s" % span_sec
    elif (span_sec < unit_hour):
        return "%.3f min" % (span_sec / unit_min)
    elif (span_sec < unit_day):
        return "%.3f h" % (span_sec / unit_hour)
    elif (span_sec < unit_day * 30):
        return "%.3f d" % (span_sec / unit_day)
    else:
        return time2str(t2)


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
