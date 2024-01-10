'限制某些时间频率'
import json
import os
import time

from ylt import CACHE_DIR

RATELIMIT_FILE = "./ratelimit.json"
ratelimit_path = f"{CACHE_DIR}/{RATELIMIT_FILE}"


if not os.path.exists(ratelimit_path):
    with open(ratelimit_path, "w", encoding="utf-8") as file:
        file.write("{}")


def get_last_time(key):
    """_summary_

    Args:
        key (_type_): _description_

    Returns:
        _type_: _description_
    """
    data = get_data()
    if key in data:
        return data[key]

    return -1


def over_limit(key, span_sec):
    """查看该事件key是否已经过去span_sec秒

    Args:
        key (_type_): _description_
        span_sec (_type_): 已经过去 x s,就视为可以了

    Returns:
        _type_: _description_
    """
    sec = time.time() - get_last_time(key)
    return sec > span_sec, sec


def clear_old(data):
    """太久远的key删除掉

    Args:
        data (_type_): _description_

    Returns:
        _type_: _description_
    """
    for key in list(data.keys()):
        # 太久的，不保留
        if time.time() - data[key] > 60 * 60 * 24 * 365:
            data.pop(key)
    return data


def save_record(key):
    """记录某个时间

    Args:
        key (_type_): _description_
    """
    data = get_data()
    data[key] = time.time()

    clear_old(data)
    with open(ratelimit_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)


def get_data():
    """获取本地数据

    Returns:
        dict: _description_
    """
    with open(ratelimit_path, "r", encoding="utf-8") as fp:
        return json.load(fp)
