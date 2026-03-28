#!/usr/bin/env python3
"""Tests for ai_cli.py"""

import io
import sys
import unittest

from ai_cli import build_parser, cmd_news, cmd_summary, cmd_report, cmd_search, load_saved_news


class TestBuildParser(unittest.TestCase):
    def test_news_command_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["news"])
        self.assertEqual(args.command, "news")
        self.assertEqual(args.limit, 0)
        self.assertFalse(args.analysis)
        self.assertFalse(args.save)

    def test_news_command_with_options(self):
        parser = build_parser()
        args = parser.parse_args(["news", "-n", "3", "-a", "-s"])
        self.assertEqual(args.limit, 3)
        self.assertTrue(args.analysis)
        self.assertTrue(args.save)

    def test_summary_command(self):
        parser = build_parser()
        args = parser.parse_args(["summary"])
        self.assertEqual(args.command, "summary")

    def test_report_command_defaults(self):
        parser = build_parser()
        args = parser.parse_args(["report"])
        self.assertEqual(args.command, "report")
        self.assertFalse(args.save)

    def test_report_command_save_flag(self):
        parser = build_parser()
        args = parser.parse_args(["report", "--save"])
        self.assertTrue(args.save)

    def test_search_command(self):
        parser = build_parser()
        args = parser.parse_args(["search", "GPT"])
        self.assertEqual(args.command, "search")
        self.assertEqual(args.keyword, "GPT")

    def test_no_command_returns_zero(self):
        from ai_cli import main
        # When no command is given, main should print help and return 0
        result = main([])
        self.assertEqual(result, 0)


class TestCmdNews(unittest.TestCase):
    def _run(self, argv):
        parser = build_parser()
        args = parser.parse_args(argv)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            result = cmd_news(args)
        finally:
            sys.stdout = old_stdout
        return result, captured.getvalue()

    def test_returns_zero(self):
        rc, _ = self._run(["news"])
        self.assertEqual(rc, 0)

    def test_output_contains_header(self):
        _, output = self._run(["news"])
        self.assertIn("AI", output)

    def test_limit_reduces_output(self):
        _, full = self._run(["news"])
        _, limited = self._run(["news", "-n", "2"])
        # The limited run should show fewer articles (less total output)
        self.assertLess(len(limited), len(full))

    def test_analysis_flag_adds_analysis_text(self):
        _, no_analysis = self._run(["news", "-n", "1"])
        _, with_analysis = self._run(["news", "-n", "1", "-a"])
        self.assertGreater(len(with_analysis), len(no_analysis))


class TestCmdSummary(unittest.TestCase):
    def test_returns_zero(self):
        parser = build_parser()
        args = parser.parse_args(["summary"])
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            rc = cmd_summary(args)
        finally:
            sys.stdout = old_stdout
        self.assertEqual(rc, 0)

    def test_output_contains_top_news(self):
        parser = build_parser()
        args = parser.parse_args(["summary"])
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_summary(args)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        self.assertIn("Top", output)


class TestCmdReport(unittest.TestCase):
    def test_returns_zero(self):
        parser = build_parser()
        args = parser.parse_args(["report"])
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            rc = cmd_report(args)
        finally:
            sys.stdout = old_stdout
        self.assertEqual(rc, 0)

    def test_output_contains_analysis(self):
        parser = build_parser()
        args = parser.parse_args(["report"])
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            cmd_report(args)
        finally:
            sys.stdout = old_stdout
        output = captured.getvalue()
        self.assertIn("解析", output)
        self.assertIn("评价", output)


class TestCmdSearch(unittest.TestCase):
    def _run_search(self, keyword):
        parser = build_parser()
        args = parser.parse_args(["search", keyword])
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            rc = cmd_search(args)
        finally:
            sys.stdout = old_stdout
        return rc, captured.getvalue()

    def test_returns_zero_when_found(self):
        rc, output = self._run_search("AI")
        self.assertEqual(rc, 0)
        self.assertIn("找到", output)

    def test_returns_zero_when_not_found(self):
        rc, output = self._run_search("xyznonexistentkeyword12345")
        self.assertEqual(rc, 0)
        self.assertIn("未找到", output)

    def test_search_gpt_finds_articles(self):
        rc, output = self._run_search("GPT")
        self.assertEqual(rc, 0)
        self.assertIn("GPT", output)


class TestLoadSavedNews(unittest.TestCase):
    def test_returns_none_for_missing_file(self):
        result = load_saved_news("/tmp/nonexistent_file_xyz.json")
        self.assertIsNone(result)

    def test_loads_articles_from_valid_file(self):
        import json
        import tempfile
        data = {"articles": [{"title": "Test", "source": "Test"}]}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            fname = f.name
        try:
            result = load_saved_news(fname)
            self.assertIsNotNone(result)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["title"], "Test")
        finally:
            import os
            os.unlink(fname)


if __name__ == "__main__":
    unittest.main()
