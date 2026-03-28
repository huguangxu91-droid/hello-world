#!/usr/bin/env python3
"""
AI CLI - Command Line Interface for AI News and Insights

Usage:
    python3 ai_cli.py <command> [options]

Commands:
    news      Fetch and display the latest AI news
    summary   Show a brief summary of top AI news
    report    Generate and display the daily AI news report
    search    Search news articles by keyword
    help      Show this help message
"""

import argparse
import json
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

from fetch_ai_news import (
    fetch_news_from_newsapi,
    filter_and_sort_yesterday,
    save_news_to_file,
    save_report,
    generate_analysis,
)

# ─────────────────────────────────────────────────────────────────────────────
# Formatting helpers
# ─────────────────────────────────────────────────────────────────────────────

def _divider(char: str = "─", width: int = 60) -> str:
    return char * width


def _print_header(title: str) -> None:
    print(_divider("═"))
    print(f"  {title}")
    print(_divider("═"))


def _print_article(idx: int, article: Dict, *, show_analysis: bool = False) -> None:
    print(f"\n{idx}. {article.get('title', '无标题')}")
    print(f"   来源: {article.get('source', '未知')}  |  时间: {article.get('publishedAt', 'N/A')[:19]}")
    desc = article.get("description", "")
    if desc:
        # Wrap description at 70 chars for readability
        print(f"   摘要: {desc[:200]}{'...' if len(desc) > 200 else ''}")
    if show_analysis:
        analysis = generate_analysis(article)
        print(f"   解析: {analysis['insight']}")
        print(f"   评价: {analysis['evaluation']}")


# ─────────────────────────────────────────────────────────────────────────────
# Command handlers
# ─────────────────────────────────────────────────────────────────────────────

def cmd_news(args: argparse.Namespace) -> int:
    """Fetch and display the latest AI news articles."""
    _print_header("🤖 AI 最新新闻 / AI Latest News")
    articles = fetch_news_from_newsapi()
    prioritized = filter_and_sort_yesterday(articles)
    limit = args.limit if args.limit > 0 else len(prioritized)
    display = prioritized[:limit]
    for idx, article in enumerate(display, start=1):
        _print_article(idx, article, show_analysis=args.analysis)
    print(f"\n{_divider()}")
    print(f"共显示 {len(display)} 条新闻（共 {len(prioritized)} 条）")
    if args.save:
        save_news_to_file(prioritized)
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    """Display a brief summary of the top AI news."""
    _print_header("📋 AI 新闻摘要 / AI News Summary")
    articles = fetch_news_from_newsapi()
    prioritized = filter_and_sort_yesterday(articles)
    top_n = min(5, len(prioritized))
    print(f"\n今日 Top {top_n} AI 要闻：\n")
    for idx, article in enumerate(prioritized[:top_n], start=1):
        title = article.get("title", "无标题")
        source = article.get("source", "未知")
        score = article.get("importance_score", 0.0)
        print(f"  {idx}. [{source}] {title}  (重要度: {score:.1f})")
    print()
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    """Generate and display (or save) the daily AI news report."""
    _print_header("📰 AI 日报 / AI Daily Report")
    articles = fetch_news_from_newsapi()
    prioritized = filter_and_sort_yesterday(articles)
    date_str = (datetime.now()).strftime("%Y-%m-%d")
    print(f"\nAI 要闻报告 – {date_str}\n{_divider()}")
    for idx, article in enumerate(prioritized, start=1):
        _print_article(idx, article, show_analysis=True)
    print(f"\n{_divider()}")
    if args.save:
        save_report(prioritized)
        print("报告已保存至 ai_news_report.txt")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    """Search news articles by keyword."""
    keyword = args.keyword.lower()
    _print_header(f"🔍 搜索: {args.keyword}")
    articles = fetch_news_from_newsapi()
    matches = [
        a for a in articles
        if keyword in a.get("title", "").lower()
        or keyword in a.get("description", "").lower()
        or keyword in a.get("source", "").lower()
    ]
    if not matches:
        print(f"\n未找到包含 '{args.keyword}' 的新闻。")
        return 0
    print(f"\n找到 {len(matches)} 条相关新闻：")
    for idx, article in enumerate(matches, start=1):
        _print_article(idx, article)
    return 0


def load_saved_news(filepath: str) -> Optional[List[Dict]]:
    """Load articles from a saved JSON file (ai_news_data.json)."""
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("articles", [])


# ─────────────────────────────────────────────────────────────────────────────
# Argument parser
# ─────────────────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai_cli",
        description="AI CLI – 命令行 AI 新闻工具 / Command-line AI news tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", metavar="<command>")

    # news
    p_news = subparsers.add_parser("news", help="获取并展示最新 AI 新闻")
    p_news.add_argument("-n", "--limit", type=int, default=0, metavar="N",
                        help="显示条数（默认全部）")
    p_news.add_argument("-a", "--analysis", action="store_true",
                        help="同时展示每条新闻的 AI 解析")
    p_news.add_argument("-s", "--save", action="store_true",
                        help="保存数据到 ai_news_data.json")

    # summary
    subparsers.add_parser("summary", help="展示 Top 5 AI 新闻摘要")

    # report
    p_report = subparsers.add_parser("report", help="生成每日 AI 新闻报告")
    p_report.add_argument("-s", "--save", action="store_true",
                          help="保存报告到 ai_news_report.txt")

    # search
    p_search = subparsers.add_parser("search", help="按关键词搜索新闻")
    p_search.add_argument("keyword", help="搜索关键词")

    return parser


# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────

def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    dispatch = {
        "news": cmd_news,
        "summary": cmd_summary,
        "report": cmd_report,
        "search": cmd_search,
    }

    if args.command in dispatch:
        return dispatch[args.command](args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
