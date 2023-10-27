"""初始化一些数据
"""
import os
from ylt.utils.my_file import check_dir


this_path = os.path.abspath('.')
# cache_dir = this_path + "/cache/"
# cache_dir = os.path.join(os.path.expanduser('~'), '.cache/ylt')
CACHE_DIR = "/opt/ylt/cache/"

check_dir(CACHE_DIR)
