import datetime
import unittest

from fetch_ai_news import filter_and_sort_yesterday, generate_analysis


class FetchAiNewsTests(unittest.TestCase):
    def test_filter_and_sort_yesterday_prioritizes_yesterday_and_importance(self):
        fixed_now = datetime.datetime(2025, 12, 31, 12, 0, 0)
        yesterday = (fixed_now - datetime.timedelta(days=1)).isoformat()
        today = fixed_now.isoformat()

        articles = [
            {
                "title": "AI Regulation Framework Proposed",
                "description": "Important regulation update on AI safety.",
                "publishedAt": yesterday,
                "source": "Policy Daily",
            },
            {
                "title": "Minor AI UI Update",
                "description": "A small tweak to an app UI.",
                "publishedAt": yesterday,
                "source": "App News",
            },
            {
                "title": "Security breakthrough in AI",
                "description": "New security model released.",
                "publishedAt": yesterday,
                "source": "Security Weekly",
            },
            {
                "title": "Today news should be ignored",
                "description": "This should not appear",
                "publishedAt": today,
                "source": "Now",
            },
        ]

        sorted_articles = filter_and_sort_yesterday(articles, now=fixed_now)

        # Only yesterday's three articles should remain
        self.assertEqual(len(sorted_articles), 3)
        # The most important item should contain a high-weight keyword (regulation/security)
        top_title = sorted_articles[0]["title"].lower()
        self.assertTrue("regulation" in top_title or "security" in top_title)

    def test_generate_analysis_returns_insight_and_evaluation(self):
        article = {
            "title": "Model release",
            "description": "Major model update",
            "source": "AI News",
        }
        result = generate_analysis(article)

        self.assertIn("insight", result)
        self.assertIsInstance(result["insight"], str)
        self.assertIn("evaluation", result)
        self.assertIsInstance(result["evaluation"], str)


if __name__ == "__main__":
    unittest.main()
