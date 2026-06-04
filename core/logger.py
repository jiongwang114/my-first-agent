# core/logger.py
import logging
import os
from datetime import datetime

def setup_logger():
    """
    初始化并配置 Agent 的全局日志系统
    """
    # 1. 自动定位项目根目录，并确保 data/logs/ 文件夹存在
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    log_dir = os.path.join(project_root, "data", "logs")
    
    # 如果文件夹不存在，自动创建它
    os.makedirs(log_dir, exist_ok=True)
    
    # 2. 按照当天的日期生成日志文件名，例如: agent_2026-06-03.log
    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"agent_{date_str}.log")
    
    # 3. 配置 logging 基础设置
    # level=logging.INFO 意味着只记录 INFO 及以上级别的信息（忽略更底层的 DEBUG 噪音）
    # encoding="utf-8" 确保存进去的中文不会乱码
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            # 将日志写入文件
            logging.FileHandler(log_file, encoding="utf-8"),
            # 如果你希望终端不仅有 print，也有标准的日志格式，可以取消下面这行的注释
            # logging.StreamHandler() 
        ]
    )
    
    # 返回配置好的 logger 对象
    return logging.getLogger("AgentLogger")

# 实例化一个全局 logger 供其他文件导入使用
logger = setup_logger()