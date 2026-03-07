#!/usr/bin/env python3
"""
Claude API Release Notes ページをパースして JSON 形式で出力するスクリプト。

Usage:
    python parse_release_notes.py --days 7 --feed /tmp/claude_release_notes.html
    curl -sL "https://platform.claude.com/docs/en/release-notes/overview" | python parse_release_notes.py --days 7
"""

import argparse
import json
import re
import sys
from datetime import datetime, timedelta


def parse_date_string(date_str: str) -> str:
    """様々な日付形式をパースして YYYY-MM-DD 形式に変換する。"""
    # Remove ordinal suffixes
    date_str = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_str)

    # Try common formats
    formats = [
        "%B %d, %Y",  # March 7, 2026
        "%b %d, %Y",  # Mar 7, 2026
        "%d %B %Y",   # 7 March 2026
        "%d %b %Y",   # 7 Mar 2026
        "%Y-%m-%d",   # 2026-03-07
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return ""


def extract_release_notes(content: str) -> list:
    """リリースノートをパースしてアイテムのリストを返す。"""
    items = []

    # Split by date headers (### February 19, 2026)
    date_pattern = r"###\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})"
    parts = re.split(date_pattern, content)

    # Parts will be: [preamble, date1, content1, date2, content2, ...]
    for i in range(1, len(parts), 2):
        if i + 1 >= len(parts):
            break

        date_str = parts[i]
        section_content = parts[i + 1]

        parsed_date = parse_date_string(date_str)
        if not parsed_date:
            continue

        # Extract bullet points from this section
        bullets = re.findall(r"^[-*]\s+(.+?)(?=\n[-*]|\n\n|\n###|$)", section_content, re.MULTILINE | re.DOTALL)

        for bullet in bullets:
            # Clean up the bullet text
            text = bullet.strip()
            text = re.sub(r"\s+", " ", text)  # Normalize whitespace

            # Skip empty bullets
            if not text:
                continue

            # Extract title (first sentence or up to first period/colon)
            title_match = re.match(r"^(.+?(?:\.|:|\?|!))(?:\s|$)", text)
            if title_match:
                title = title_match.group(1).strip()
            else:
                title = text[:100] + ("..." if len(text) > 100 else "")

            # Remove markdown formatting from title
            title = re.sub(r"\*\*(.+?)\*\*", r"\1", title)
            title = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", title)

            # Extract links
            links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)

            items.append({
                "title": title,
                "date": parsed_date,
                "description": text,
                "category": "release-notes",
                "links": [{"text": t, "url": u} for t, u in links],
            })

    return items


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


def main():
    parser = argparse.ArgumentParser(description="Parse Claude API Release Notes")
    parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    parser.add_argument("--feed", type=str, help="Path to HTML/MD file (default: stdin)")
    args = parser.parse_args()

    # Read input
    if args.feed:
        with open(args.feed, encoding="utf-8") as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    # Parse release notes
    items = extract_release_notes(content)

    # Filter by date
    filtered_items = filter_by_days(items, args.days)

    # Sort by date (newest first)
    filtered_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Output as JSON
    result = {
        "source": "claude-release-notes",
        "total_items": len(filtered_items),
        "days": args.days,
        "items": filtered_items,
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
