import os

this_path = os.path.abspath('.')
cache_dir = this_path + "/cache/"


if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
