import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='ylt',
                 version='0.0.2',
                 author="yuhldr",
                 author_email="***REMOVED***",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 py_modules=["ylt"],
                 install_requires=["psutil"],
                 include_package_data=True,
                 packages=setuptools.find_packages(),
                 description="linux工具")
