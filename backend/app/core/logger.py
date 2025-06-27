"""
Logger Configuration Module

구조화된 로깅 시스템 제공
개발/프로덕션 환경별 로깅 레벨 자동 조정
"""
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from app.core.config import settings

# 로그 디렉토리 생성
if settings.LOG_FILE:
    log_dir = Path(settings.LOG_FILE).parent
    log_dir.mkdir(parents=True, exist_ok=True)

class ColoredFormatter(logging.Formatter):
    """컬러 로그 포맷터 (개발 환경용)"""
    
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "[%(levelname)s] %(asctime)s - %(name)s - %(message)s" + reset,
        logging.INFO: grey + "[%(levelname)s] %(asctime)s - %(name)s - %(message)s" + reset,
        logging.WARNING: yellow + "[%(levelname)s] %(asctime)s - %(name)s - %(message)s" + reset,
        logging.ERROR: red + "[%(levelname)s] %(asctime)s - %(name)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "[%(levelname)s] %(asctime)s - %(name)s - %(message)s" + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

def setup_logger(
    name: str,
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    로거 설정
    
    Args:
        name: 로거 이름
        level: 로그 레벨 (기본값: 설정 파일에서 가져옴)
        log_file: 로그 파일 경로
    
    Returns:
        설정된 로거 인스턴스
    """
    logger = logging.getLogger(name)
    
    # 이미 핸들러가 있으면 재설정하지 않음
    if logger.handlers:
        return logger
    
    # 로그 레벨 설정
    log_level = getattr(logging, level or settings.LOG_LEVEL.upper())
    logger.setLevel(log_level)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    if settings.is_development:
        console_handler.setFormatter(ColoredFormatter())
    else:
        console_handler.setFormatter(
            logging.Formatter(
                "[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
    logger.addHandler(console_handler)
    
    # 파일 핸들러 (설정된 경우)
    if log_file or settings.LOG_FILE:
        file_path = log_file or settings.LOG_FILE
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter(
                "[%(levelname)s] %(asctime)s - %(name)s - %(funcName)s:%(lineno)d - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
        )
        logger.addHandler(file_handler)
    
    return logger

# 기본 로거 인스턴스
logger = setup_logger("app") 