'''pip打包'''
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='ylt',
                 version='0.0.3',
                 author="yuhldr",
                 author_email="yuhldr@qq.com",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 py_modules=["ylt"],
                 install_requires=["psutil"],
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 description="linux工具")
