# -*- coding: utf-8 -*-
"""
Test suite for the CSDNBlogScraper.
Note: These tests are basic unit tests, not integration tests.
"""

import sys
import os
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import Config
from src.utils import sanitize_filename, extract_username


class TestConfig(unittest.TestCase):
    """Test the Config class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = Config()
        self.assertEqual(config.min_delay, 1.5)
        self.assertEqual(config.max_delay, 3.0)
        self.assertEqual(config.max_retries, 3)
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = Config(
            blog_url="https://blog.csdn.net/test",
            min_delay=2.0,
            max_delay=4.0
        )
        self.assertEqual(config.min_delay, 2.0)
        self.assertEqual(config.max_delay, 4.0)
        self.assertEqual(config.blog_url, "https://blog.csdn.net/test")
    
    def test_config_validation(self):
        """Test configuration validation."""
        with self.assertRaises(ValueError):
            Config(min_delay=-1)
        
        with self.assertRaises(ValueError):
            Config(max_pages=0)


class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_sanitize_filename(self):
        """Test filename sanitization."""
        self.assertEqual(sanitize_filename("test/file"), "testfile")
        self.assertEqual(sanitize_filename("test\\file"), "testfile")
        self.assertEqual(sanitize_filename("test file"), "testfile")
        self.assertEqual(sanitize_filename("test file name"), "testfilename")
    
    def test_extract_username(self):
        """Test username extraction."""
        self.assertEqual(
            extract_username("https://blog.csdn.net/qq_46987323"), "qq_46987323")
        self.assertEqual(
            extract_username("https://blog.csdn.net/testname"), "testname")
        self.assertIsNone(extract_username("https://google.com"))


if __name__ == "__main__":
    print("=" * 60)
    print("Running CSDN Blog Scraper Tests")
    print("=" * 60)
    unittest.main()
