#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

该文件原本在根目录下，无法被 wheel 打包，因此转移到该模块(Dashboard)下。它的作用和 __main__.py 类似，作为外部脚本启动服务使用。
"""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Dashboard.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# 入口函数
if __name__ == '__main__':
    main()
