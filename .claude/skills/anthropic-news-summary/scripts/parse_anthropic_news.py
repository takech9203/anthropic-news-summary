#!/usr/bin/env python3
"""
Anthropic News ページをパースして JSON 形式で出力するスクリプト。

Usage:
    python parse_anthropic_news.py --days 7 --feed /tmp/anthropic_news.html
    curl -sL "https://www.anthropic.com/news" | python parse_anthropic_news.py --days 7
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta
from html.parser import HTMLParser


class AnthropicNewsParser(HTMLParser):
    """Anthropic News ページの HTML をパースする。"""

    def __init__(self):
        super().__init__()
        self.items = []
        self.current_item = None
        self.in_article = False
        self.in_title = False
        self.in_date = False
        self.in_description = False
        self.capture_text = False
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get("class", "")

        # Article container detection
        if tag == "article" or (tag == "div" and "card" in class_name.lower()):
            self.in_article = True
            self.current_item = {
                "title": "",
                "date": "",
                "link": "",
                "description": "",
                "category": "news",
            }

        if self.in_article:
            # Link detection
            if tag == "a" and "href" in attrs_dict:
                href = attrs_dict["href"]
                if "/news/" in href:
                    if href.startswith("/"):
                        href = "https://www.anthropic.com" + href
                    self.current_item["link"] = href

            # Title detection
            if tag in ("h2", "h3") or (tag == "span" and "title" in class_name.lower()):
                self.in_title = True
                self.capture_text = True
                self.current_text = ""

            # Date detection
            if tag == "time" or (tag == "span" and "date" in class_name.lower()):
                self.in_date = True
                self.capture_text = True
                self.current_text = ""
                if "datetime" in attrs_dict:
                    self.current_item["date"] = attrs_dict["datetime"][:10]

            # Description detection
            if tag == "p" and not self.in_title:
                self.in_description = True
                self.capture_text = True
                self.current_text = ""

    def handle_endtag(self, tag):
        if self.in_title and tag in ("h2", "h3", "span"):
            self.in_title = False
            self.capture_text = False
            if self.current_item and self.current_text.strip():
                self.current_item["title"] = self.current_text.strip()
            self.current_text = ""

        if self.in_date and tag in ("time", "span"):
            self.in_date = False
            self.capture_text = False
            if self.current_item and self.current_text.strip() and not self.current_item["date"]:
                self.current_item["date"] = parse_date_string(self.current_text.strip())
            self.current_text = ""

        if self.in_description and tag == "p":
            self.in_description = False
            self.capture_text = False
            if self.current_item and self.current_text.strip():
                self.current_item["description"] = self.current_text.strip()
            self.current_text = ""

        if tag == "article" or (self.in_article and tag == "div"):
            if self.current_item and self.current_item.get("title"):
                self.items.append(self.current_item)
            self.in_article = False
            self.current_item = None

    def handle_data(self, data):
        if self.capture_text:
            self.current_text += data


def parse_date_string(date_str: str) -> str:
    """様々な日付形式をパースして YYYY-MM-DD 形式に変換する。"""
    # Try ISO format first
    if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
        return date_str[:10]

    # Try common formats
    formats = [
        "%B %d, %Y",  # March 7, 2026
        "%b %d, %Y",  # Mar 7, 2026
        "%d %B %Y",   # 7 March 2026
        "%d %b %Y",   # 7 Mar 2026
        "%Y/%m/%d",   # 2026/03/07
        "%m/%d/%Y",   # 03/07/2026
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return ""


def filter_by_days(items: list, days: int) -> list:
    """指定日数以内のアイテムのみをフィルタリングする。"""
    cutoff = datetime.now() - timedelta(days=days)
    filtered = []

    for item in items:
        if not item.get("date"):
            continue
        try:
            item_date = datetime.strptime(item["date"], "%Y-%m-%d")
            if item_date >= cutoff:
                filtered.append(item)
        except ValueError:
            continue

    return filtered


def parse_news_from_html(html_content: str) -> list:
    """HTML コンテンツからニュースアイテムを抽出する。"""
    parser = AnthropicNewsParser()
    parser.feed(html_content)
    return parser.items


def extract_news_from_json_ld(html_content: str) -> list:
    """JSON-LD 形式のデータからニュースを抽出する (フォールバック)。"""
    items = []

    # Look for JSON-LD script tags
    json_ld_pattern = r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>'
    matches = re.findall(json_ld_pattern, html_content, re.DOTALL)

    for match in matches:
        try:
            data = json.loads(match)
            if isinstance(data, list):
                for item in data:
                    if item.get("@type") in ("NewsArticle", "Article", "BlogPosting"):
                        items.append({
                            "title": item.get("headline", ""),
                            "date": item.get("datePublished", "")[:10] if item.get("datePublished") else "",
                            "link": item.get("url", ""),
                            "description": item.get("description", ""),
                            "category": "news",
                        })
            elif isinstance(data, dict) and data.get("@type") in ("NewsArticle", "Article", "BlogPosting"):
                items.append({
                    "title": data.get("headline", ""),
                    "date": data.get("datePublished", "")[:10] if data.get("datePublished") else "",
                    "link": data.get("url", ""),
                    "description": data.get("description", ""),
                    "category": "news",
                })
        except json.JSONDecodeError:
            continue

    return items


def main():
    parser = argparse.ArgumentParser(description="Parse Anthropic News page")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--feed", type=str, help="Path to HTML file (default: stdin)")
    args = parser.parse_args()

    # Read input
    if args.feed:
        with open(args.feed, encoding="utf-8") as f:
            html_content = f.read()
    else:
        html_content = sys.stdin.read()

    # Parse news
    items = parse_news_from_html(html_content)

    # Fallback to JSON-LD if no items found
    if not items:
        items = extract_news_from_json_ld(html_content)

    # Filter by date
    filtered_items = filter_by_days(items, args.days)

    # Sort by date (newest first)
    filtered_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Output as JSON
    result = {
        "source": "anthropic-news",
        "total_items": len(filtered_items),
        "days": args.days,
        "items": filtered_items,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
