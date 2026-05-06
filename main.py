# -*- coding: utf-8 -*-
"""
CSDN Blog Scraper - Command Line Interface
A professional, extensible tool for scraping CSDN blog articles.

Usage:
    python main.py --help
    python main.py -u "https://blog.csdn.net/qq_46987323" -f json
    python main.py --url "https://blog.csdn.net/yourname" --output csv
"""

import sys
import argparse
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src import CSDNBlogScraper, Config, setup_logger, ExporterFactory


def print_banner():
    """Print the welcome banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                  CSDN BLOG SCRAPER - v1.0.0                    ║
║          A professional tool for scraping CSDN blogs          ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CSDN Blog Scraper - Scrape CSDN blog articles with ease",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -u "https://blog.csdn.net/qq_46987323"
  python main.py --url "https://blog.csdn.net/yourname" -f csv
  python main.py -u "https://blog.csdn.net/name" --max-pages 5
  python main.py -u "https://blog.csdn.net/name" --min-delay 2 --max-delay 4
        """
    )
    
    parser.add_argument(
        "-u", "--url",
        required=True,
        help="URL of the target CSDN blog"
    )
    parser.add_argument(
        "-f", "--format",
        default="txt",
        choices=ExporterFactory.list_formats(),
        help=f"Output format ({', '.join(ExporterFactory.list_formats())}) (default: txt)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output filename (default: auto-generated)"
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=1.5,
        help="Minimum delay between requests in seconds (default: 1.5)"
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=3.0,
        help="Maximum delay between requests in seconds (default: 3.0)"
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        help="Maximum number of pages to scrape (default: all pages)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Request timeout in seconds (default: 30)"
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Maximum number of retry attempts (default: 3)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--list-formats",
        action="store_true",
        help="List available output formats and exit"
    )
    
    args = parser.parse_args()
    
    if args.list_formats:
        print_banner()
        print("\n📋 Available export formats:")
        for fmt in ExporterFactory.list_formats():
            print(f"   - {fmt}")
        print()
        sys.exit(0)
    
    print_banner()
    
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(log_file="outputs/scraper.log", log_level=log_level)
    
    try:
        config = Config(
            blog_url=args.url,
            min_delay=args.min_delay,
            max_delay=args.max_delay,
            request_timeout=args.timeout,
            max_retries=args.retries,
            max_pages=args.max_pages,
        )
        
        scraper = CSDNBlogScraper(config, logger)
        articles = scraper.scrape_all_articles()
        
        if articles:
            filepath = scraper.save(articles, format=args.format, filename=args.output)
            print(f"\n🎉 Done! Articles saved to: {filepath}")
        else:
            print("\n⚠️ No articles found!")
            
    except KeyboardInterrupt:
        print("\n\n👋 User interrupted. Exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if log_level == logging.DEBUG:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
