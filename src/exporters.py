# -*- coding: utf-8 -*-
"""
Exporters for the CSDN Blog Scraper.
Supports multiple output formats: JSON, CSV, and TXT.
"""

import os
import json
import csv
from typing import List, Dict, Any, Optional
from datetime import datetime


class BaseExporter:
    """Base class for all exporters."""
    
    def export(self, articles: List[Dict[str, Any]], filepath: str) -> None:
        """
        Export articles to a file.
        
        Args:
            articles: List of article dictionaries
            filepath: Path to output file
        """
        raise NotImplementedError("Subclasses must implement export method")
    
    def _ensure_dir(self, filepath: str) -> None:
        """Ensure directory exists for the output file."""
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)


class JSONExporter(BaseExporter):
    """Exports articles to JSON format."""
    
    def export(self, articles: List[Dict[str, Any]], filepath: str) -> None:
        """
        Export articles to JSON file.
        
        Args:
            articles: List of article dictionaries
            filepath: Path to output JSON file
        """
        self._ensure_dir(filepath)
        
        output_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "article_count": len(articles),
            },
            "articles": articles,
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Successfully exported {len(articles)} articles to {filepath}")


class CSVExporter(BaseExporter):
    """Exports articles to CSV format."""
    
    def export(self, articles: List[Dict[str, Any]], filepath: str) -> None:
        """
        Export articles to CSV file.
        
        Args:
            articles: List of article dictionaries
            filepath: Path to output CSV file
        """
        self._ensure_dir(filepath)
        
        if not articles:
            print("⚠️ No articles to export")
            return
        
        fieldnames = ["index", "title", "url", "date", "views"]
        
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for idx, article in enumerate(articles, 1):
                row = {
                    "index": idx,
                    "title": article.get("title", ""),
                    "url": article.get("url", ""),
                    "date": article.get("date", ""),
                    "views": article.get("views", ""),
                }
                writer.writerow(row)
        
        print(f"✅ Successfully exported {len(articles)} articles to {filepath}")


class TXTExporter(BaseExporter):
    """Exports articles to plain text format."""
    
    def export(self, articles: List[Dict[str, Any]], filepath: str) -> None:
        """
        Export articles to text file.
        
        Args:
            articles: List of article dictionaries
            filepath: Path to output text file
        """
        self._ensure_dir(filepath)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CSDN BLOG ARTICLE LIST\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Articles: {len(articles)}\n")
            f.write("=" * 80 + "\n\n")
            
            for idx, article in enumerate(articles, 1):
                f.write(f"[{idx}] {article.get('title', 'No title')}\n")
                f.write(f"    URL: {article.get('url', '')}\n")
                f.write(f"    Date: {article.get('date', 'Unknown')}\n")
                f.write(f"    Views: {article.get('views', 'Unknown')}\n")
                f.write("\n")
        
        print(f"✅ Successfully exported {len(articles)} articles to {filepath}")


class ExporterFactory:
    """Factory for creating exporters."""
    
    _exporters = {
        "json": JSONExporter,
        "csv": CSVExporter,
        "txt": TXTExporter,
    }
    
    @classmethod
    def get_exporter(cls, format: str) -> BaseExporter:
        """
        Get exporter for specified format.
        
        Args:
            format: Output format (json, csv, txt)
            
        Returns:
            Exporter instance
        """
        format = format.lower()
        if format not in cls._exporters:
            raise ValueError(f"Unsupported format: {format}. Available formats: {list(cls._exporters.keys())}")
        return cls._exporters[format]()
    
    @classmethod
    def list_formats(cls) -> List[str]:
        """List available export formats."""
        return list(cls._exporters.keys())
