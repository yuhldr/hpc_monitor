"""初始化一些数据
"""
import os

from ylt.utils.my_file import check_dir

THIS_PATH = "/opt/ylt/"
CACHE_DIR = THIS_PATH + "/cache/"
# cache_dir = os.path.join(os.path.expanduser('~'), '.cache/ylt')

check_dir(CACHE_DIR)
