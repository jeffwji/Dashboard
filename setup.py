# -*- coding: utf-8 -*-

"""
Example of how to use setuptools
"""

__version__ = "1.0.0"

from setuptools import setup, find_packages

#########
# autoupgrade 包提供了自动依赖检查，可以让 Dashboard 在安装前检查依赖的 Monitor 的版本，并自动升级到最新版。但是 test 执行在 setup
# 之前，因此 autoupgrade 包本身无法被自动安装，需要手工安装。安装命令是:
#
# $ pip install https://bitbucket.org/jorkar/autoupgrade/get/master.tar.gz
#
#from autoupgrade import AutoUpgrade
#AutoUpgrade("submodule1", index="https://pypi.company.com/repos").upgrade_if_needed()


# Read description from README file.
def long_description():
    from os import path
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


def get_depends():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    author='Jeff Wang',
    author_email='jeffwji@test.com',
    name="devops_dashboard",
    long_description=long_description(),

    version=__version__,

    package_data={
        'ui': ['templates/*.html'],
    },

    packages=find_packages(
        exclude=['tests', 'test']
    ),
    install_requires=get_depends(),

    ######
    # 因为 manage.py 处于根目录下，因此无法被打包，所以需要将 manage.py 复制到 Dashboard 模块下，然后打包。
    #
    # 启动命令: `dashboard`
    #
    # 如果希望以 `python -m Dashboard` 来启动，则需要在 `Dashboard` 模块下另外新建 `__main__.py` 文件来调用 `manage.main()` 方法
    #
    # 注意：复制到 Dashboard 后可以在命令行以脚本方式启动，但是不能直接执行，会爆出 `No module named 'Dashboard.settings'` 错误。
    # 因此不要移除根目录下的 `manage.py` 文件，仅作为开发调式使用。
    #
    entry_points={
        "console_scripts": [
            # 命令 = 模块.包名:入口函数
            "dashboard = Dashboard.manage:main"
        ]
    },
)
