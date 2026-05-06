# -*- coding: utf-8 -*-
"""
Utility functions for the CSDN Blog Scraper.
Includes logging setup, filename sanitization, and other helper functions.
"""

import os
import re
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional


def setup_logger(
    name: str = "csdn_scraper",
    log_file: Optional[str] = None,
    log_level: int = logging.INFO
) -> logging.Logger:
    """
    Setup a logger with both file and console output.
    
    Args:
        name: Logger name
        log_file: Path to log file (optional)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.handlers.clear()
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize a filename by removing or replacing invalid characters.
    
    Args:
        filename: Original filename
        max_length: Maximum length of the sanitized filename
        
    Returns:
        Sanitized filename
    """
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    sanitized = sanitized.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    sanitized = sanitized.strip()
    sanitized = sanitized[:max_length] if len(sanitized) > max_length else sanitized
    return sanitized or "untitled"


def extract_username(url: str) -> Optional[str]:
    """
    Extract CSDN username from blog URL.
    
    Args:
        url: CSDN blog URL
        
    Returns:
        Username if found, None otherwise
    """
    match = re.search(r'blog\.csdn\.net/([a-zA-Z0-9_]+)', url)
    return match.group(1) if match else None
