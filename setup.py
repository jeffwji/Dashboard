"""
Example of how to use setuptools
"""

from __init__ import __version__                      # 2) 或直接在本地定义 version

from setuptools import setup, find_packages


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
    # 因为 manage.py 处于根目录下，因此无法被打包，所以需要将 manage.py 转移到 Dashboard 模块下，然后打包。
    #
    # 启动命令: `dashboard`
    #
    # 如果希望以 `python -m Dashboard` 来启动，则需要在 `Dashboard` 模块下另外新建 `__main__.py` 文件来调用 `manage.main()` 方法
    #
    entry_points={
        "console_scripts": [
            # 命令 = 模块.包名:入口函数
            "dashboard = Dashboard.manage:main"
        ]
    },
)
