'''pip打包'''
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

scripts = [
    "ylt/bin/sinfo-s",
    "ylt/bin/nodes",
    "ylt/bin/topn",
    "ylt/bin/ylt",
    "ylt/bin/ylt_ref_disk",
    "ylt/bin/ylt_ref_other",
]

setuptools.setup(name='ylt',
                 version='0.0.4',
                 author="yuhldr",
                 author_email="yuhldr@qq.com",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 py_modules=["ylt"],
                 scripts=scripts,
                 install_requires=["psutil"],
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 description="linux工具")
