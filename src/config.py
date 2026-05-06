# -*- coding: utf-8 -*-
"""
Configuration management for the CSDN Blog Scraper.
Provides a flexible Config class with default values and easy customization.
"""

import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Config:
    """
    Configuration class for the CSDN Blog Scraper.
    
    Attributes:
        blog_url: URL of the target CSDN blog
        min_delay: Minimum delay between requests in seconds
        max_delay: Maximum delay between requests in seconds
        request_timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        max_pages: Maximum number of pages to scrape (None = all)
        output_dir: Directory to save output files
        user_agent: Custom user agent string (None = random)
        verify_ssl: Whether to verify SSL certificates
    """
    
    blog_url: str = "https://blog.csdn.net/qq_46987323"
    min_delay: float = 1.5
    max_delay: float = 3.0
    request_timeout: int = 30
    max_retries: int = 3
    max_pages: Optional[int] = None
    output_dir: str = "outputs"
    user_agent: Optional[str] = None
    verify_ssl: bool = True
    
    def __post_init__(self):
        """Validate configuration and create output directory."""
        if self.min_delay < 0:
            raise ValueError("min_delay cannot be negative")
        if self.max_delay < self.min_delay:
            raise ValueError("max_delay must be >= min_delay")
        if self.max_pages is not None and self.max_pages <= 0:
            raise ValueError("max_pages must be a positive integer or None")
        if self.request_timeout <= 0:
            raise ValueError("request_timeout must be a positive integer")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def to_dict(self) -> dict:
        """Convert config to dictionary."""
        return {
            "blog_url": self.blog_url,
            "min_delay": self.min_delay,
            "max_delay": self.max_delay,
            "request_timeout": self.request_timeout,
            "max_retries": self.max_retries,
            "max_pages": self.max_pages,
            "output_dir": self.output_dir,
            "user_agent": self.user_agent,
            "verify_ssl": self.verify_ssl,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Config":
        """Create Config instance from dictionary."""
        return cls(**data)
