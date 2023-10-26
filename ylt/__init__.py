"""初始化一些数据
"""
import os

this_path = os.path.abspath('.')
# cache_dir = this_path + "/cache/"
# cache_dir = os.path.join(os.path.expanduser('~'), '.cache/ylt')
cache_dir = "/opt/ylt/cache/"


if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
