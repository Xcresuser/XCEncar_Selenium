# logger.py
import logging
import sys
from datetime import datetime
import os

def setup_logger(log_file="selenium_script.log"):
    """
    Настройка логгера для записи в файл и вывода в консоль
    """
    # Создаем директорию для логов, если ее нет
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_path = os.path.join(log_dir, log_file)
    
    # Создаем логгер
    logger = logging.getLogger("SeleniumScript")
    logger.setLevel(logging.INFO)
    
    # Очищаем существующие обработчики
    logger.handlers.clear()
    
    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Обработчик для записи в файл
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчики к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Фильтр для важных сообщений
    class ImportantFilter(logging.Filter):
        def filter(self, record):
            # Пропускаем только важные сообщения
            important_keywords = [
                'ERROR', 'Exception', 'Error', 'Traceback', 
                'time', 'Time', 'секунд', 'выполнения'
            ]
            message = record.getMessage()
            return any(keyword in message for keyword in important_keywords)
    
    # Применяем фильтр к консольному обработчику
    console_handler.addFilter(ImportantFilter())
    
    return logger

# Создаем глобальный логгер
logger = setup_logger()