"""
Structured logging configuration for Day 78 monitoring.
Logs to both console (human-readable) and file (JSON for parsing).
"""

import logging
import logging.handlers
import json
from pathlib import Path
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure structured logging with JSON format to files and plain text to console.
    
    Args:
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove default handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # JSON file handler (structured logs for parsing/monitoring)
    json_file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "app.json",
        maxBytes=10_485_760,  # 10MB
        backupCount=5
    )
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(timestamp)s %(level)s %(name)s %(message)s"
    )
    json_file_handler.setFormatter(json_formatter)
    root_logger.addHandler(json_file_handler)
    
    # Error file handler (errors in separate file)
    error_file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "error.json",
        maxBytes=10_485_760,
        backupCount=5
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(json_formatter)
    root_logger.addHandler(error_file_handler)
    
    # Console handler (plain text for development)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Suppress noisy third-party loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given module name."""
    return logging.getLogger(name)
