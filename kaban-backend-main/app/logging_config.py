import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Создаем директорию для логов если её нет
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Файл логов
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    """
    Настраивает логирование приложения.
    Логи записываются в файл и выводятся в консоль.
    """
    # Создаем логгер для приложения
    logger = logging.getLogger("kaban")
    logger.setLevel(logging.INFO)
    
    # Убираем дублирование логов от других библиотек
    logger.propagate = False
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler для файла с ротацией
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,  # Хранить 5 резервных копий
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler для консоли
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Добавляем handlers к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Создаем глобальный логгер
logger = setup_logging()


