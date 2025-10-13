#!/usr/bin/env python3
"""
AI Daily News Fetcher
This script fetches the latest AI news and saves it to a JSON file.
"""

import json
import os
from datetime import datetime
from typing import List, Dict
import urllib.request
import urllib.error

def fetch_news_from_newsapi() -> List[Dict]:
    """
    Fetch AI-related news from NewsAPI.
    For demo purposes, returns sample data if API key is not available.
    """
    # NewsAPI endpoint for AI news
    # In production, you would use: api_key = os.environ.get('NEWS_API_KEY')
    # url = f'https://newsapi.org/v2/everything?q=artificial+intelligence&sortBy=publishedAt&apiKey={api_key}'
    
    # For now, return sample data (since we don't have API key in demo)
    sample_news = [
        {
            "title": "OpenAI Releases GPT-5 with Enhanced Reasoning Capabilities",
            "description": "OpenAI announces the release of GPT-5, featuring improved reasoning, longer context windows, and better accuracy in complex tasks.",
            "url": "https://example.com/news/1",
            "publishedAt": datetime.now().isoformat(),
            "source": "AI Tech News"
        },
        {
            "title": "Google DeepMind Achieves Breakthrough in Protein Folding",
            "description": "DeepMind's latest AI model can predict protein structures with unprecedented accuracy, opening new possibilities in drug discovery.",
            "url": "https://example.com/news/2",
            "publishedAt": datetime.now().isoformat(),
            "source": "Science Daily"
        },
        {
            "title": "AI Regulation Framework Proposed by EU Parliament",
            "description": "European Union proposes comprehensive AI regulations focusing on transparency, safety, and ethical considerations.",
            "url": "https://example.com/news/3",
            "publishedAt": datetime.now().isoformat(),
            "source": "Tech Policy Review"
        },
        {
            "title": "Meta Introduces Advanced AI Image Generation Model",
            "description": "Meta unveils new image generation AI with improved photorealism and creative capabilities.",
            "url": "https://example.com/news/4",
            "publishedAt": datetime.now().isoformat(),
            "source": "Digital Innovation"
        },
        {
            "title": "Autonomous Vehicles Reach New Safety Milestone",
            "description": "Self-driving car technology powered by advanced AI achieves 10 million miles without accidents in real-world testing.",
            "url": "https://example.com/news/5",
            "publishedAt": datetime.now().isoformat(),
            "source": "Automotive Tech"
        }
    ]
    
    return sample_news

def save_news_to_file(news_data: List[Dict], filename: str = 'ai_news_data.json'):
    """
    Save news data to a JSON file with timestamp.
    """
    output_data = {
        "last_updated": datetime.now().isoformat(),
        "news_count": len(news_data),
        "articles": news_data
    }
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully saved {len(news_data)} news articles to {filename}")
    print(f"Last updated: {output_data['last_updated']}")

def main():
    """
    Main function to fetch and save AI news.
    """
    print("Fetching latest AI news...")
    
    try:
        news_articles = fetch_news_from_newsapi()
        save_news_to_file(news_articles)
        print("News fetch completed successfully!")
        
    except Exception as e:
        print(f"Error fetching news: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
