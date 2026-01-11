from loguru import logger
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(BASE_DIR, exist_ok=True)

PENSION_ONE_LOG_PATH = os.path.join(BASE_DIR, "shipay.log")

logger.remove()

logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}"
)

logger.add(
    PENSION_ONE_LOG_PATH,
    rotation="10 MB", 
    retention="15 days",    
    compression="zip",      
    level="INFO",
    enqueue=True,           
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)