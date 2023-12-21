"""缓存数据
"""
import json


def read_json_file(file_path, data_default=None):
    """获取json数据

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        if data_default is None:
            return {}
        return data_default


def write_json_file(file_path, data):
    """保存json数据

    Args:
        data (_type_): _description_
        file_path (_type_): _description_
    """

    with open(file_path, 'w', encoding="utf8") as file:
        file.write(json.dumps(data, indent=4, ensure_ascii=False))
