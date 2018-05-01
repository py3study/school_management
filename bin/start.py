import os
import sys
sys.path.append(os.path.dirname(os.getcwd()))  #添加项目根目录到系统环境变量

from core import Main
from core import CheckFiles  # 检测配置项中的文本文件是否存在，不存在则创建

if __name__ == '__main__':
    Main.main()  # 程序核心入口