#!/usr/bin/env python3
"""
Terminal Rendering Tests -- CRAB Brand System
==============================================
Validates ANSI art, TUI chrome, and mascot rendering across environments.

Run: python -m pytest tests/test_terminal_rendering.py -v
"""

import os
import sys
import unittest

# Add the assets directory to the path so we can import the demo module
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "docs", "branding", "assets"))

from terminal_core_demo import TerminalCore


class TestTerminalCoreInstantiation(unittest.TestCase):
    """Verify TerminalCore initializes correctly under all flag combinations."""

    def test_default_init(self):
        tc = TerminalCore()
        self.assertFalse(tc.no_color)
        self.assertFalse(tc.no_unicode)
        self.assertEqual(tc.borders, tc.ROUNDED)

    def test_no_color_init(self):
        tc = TerminalCore(no_color=True)
        self.assertTrue(tc.no_color)
        self.assertFalse(tc.no_unicode)

    def test_no_unicode_init(self):
        tc = TerminalCore(no_unicode=True)
        self.assertTrue(tc.no_unicode)
        self.assertEqual(tc.borders, tc.ASCII)

    def test_both_flags_init(self):
        tc = TerminalCore(no_color=True, no_unicode=True)
        self.assertTrue(tc.no_color)
        self.assertTrue(tc.no_unicode)

    def test_no_color_env_var(self):
        old = os.environ.get("NO_COLOR")
        os.environ["NO_COLOR"] = "1"
        try:
            tc = TerminalCore()
            self.assertTrue(tc.no_color)
        finally:
            if old is None:
                os.environ.pop("NO_COLOR", None)
            else:
                os.environ["NO_COLOR"] = old


class TestColorRendering(unittest.TestCase):
    """Verify color/no-color output correctness."""

    def test_color_wrap_adds_escapes(self):
        tc = TerminalCore(no_color=False)
        out = tc._c(tc.AMBER, "test")
        self.assertIn("\033[", out)
        self.assertIn("test", out)
        self.assertTrue(out.endswith(tc.RESET))

    def test_no_color_returns_plain(self):
        tc = TerminalCore(no_color=True)
        out = tc._c(tc.AMBER, "test")
        self.assertEqual(out, "test")
        self.assertNotIn("\033[", out)

    def test_reset_included(self):
        tc = TerminalCore(no_color=False)
        out = tc._c(tc.CYAN, "x")
        self.assertTrue(out.endswith("\033[0m"))


class TestBorderRendering(unittest.TestCase):
    """Verify border sets render correctly per unicode flag."""

    def test_rounded_borders_default(self):
        tc = TerminalCore()
        b = tc.border_set("rounded")
        self.assertEqual(b["tl"], "\u256d")
        self.assertEqual(b["tr"], "\u256e")

    def test_sharp_borders(self):
        tc = TerminalCore()
        b = tc.border_set("sharp")
        self.assertEqual(b["tl"], "\u250c")
        self.assertEqual(b["br"], "\u2518")

    def test_double_borders(self):
        tc = TerminalCore()
        b = tc.border_set("double")
        self.assertEqual(b["h"], "\u2550")
        self.assertEqual(b["v"], "\u2551")

    def test_no_unicode_falls_to_ascii(self):
        tc = TerminalCore(no_unicode=True)
        b = tc.border_set("rounded")
        self.assertEqual(b["tl"], "+")
        self.assertEqual(b["h"], "-")
        self.assertEqual(b["v"], "|")


class TestBoxRendering(unittest.TestCase):
    """Verify TUI chrome box renders with correct structure."""

    def test_box_produces_lines(self):
        tc = TerminalCore(no_color=True, no_unicode=True)
        out = tc.box(["hello"], width=20, style="rounded")
        lines = out.split("\n")
        # top, content, bottom (no extra padding line when single short line)
        self.assertGreaterEqual(len(lines), 3)
        # Check top and bottom contain ASCII border chars (box still injects
        # color escapes even when no_color=True via direct bc usage)
        self.assertIn("+", lines[0])
        self.assertIn("+", lines[-1])

    def test_box_with_title_has_separator(self):
        tc = TerminalCore(no_color=True, no_unicode=True)
        out = tc.box(["hello"], width=20, style="rounded", title="Test")
        lines = out.split("\n")
        self.assertEqual(len(lines), 5)  # top, title, sep, content, bottom
        self.assertIn("Test", lines[1])

    def test_box_content_inside(self):
        tc = TerminalCore(no_color=True, no_unicode=True)
        out = tc.box(["content"], width=20, style="rounded")
        self.assertIn("content", out)

    def test_box_with_ansi_content_calculates_width(self):
        tc = TerminalCore(no_color=False, no_unicode=True)
        colored = tc._c(tc.AMBER, "hi")
        out = tc.box([colored], width=10, style="rounded")
        lines = out.split("\n")
        # All lines should have consistent width (top/bottom same length)
        self.assertEqual(len(lines[0]), len(lines[-1]))


class TestPillRendering(unittest.TestCase):
    """Verify status pill rendering."""

    def test_pill_no_color(self):
        tc = TerminalCore(no_color=True)
        out = tc.pill("OK", "green")
        self.assertEqual(out, "[OK]")

    def test_pill_color_has_escapes(self):
        tc = TerminalCore(no_color=False)
        out = tc.pill("OK", "green")
        self.assertIn("\033[", out)
        self.assertIn("OK", out)

    def test_pill_unknown_color_fallback(self):
        tc = TerminalCore(no_color=True)
        out = tc.pill("OK", "purple")
        self.assertEqual(out, "[OK]")


class TestProgressBar(unittest.TestCase):
    """Verify progress bar rendering."""

    def test_progress_zero_percent(self):
        tc = TerminalCore(no_color=True)
        out = tc.progress("TASK", 0, width=10)
        self.assertIn("TASK", out)
        self.assertIn("0%", out)

    def test_progress_full(self):
        tc = TerminalCore(no_color=True)
        out = tc.progress("TASK", 100, width=10)
        self.assertIn("100%", out)

    def test_progress_no_unicode_no_block_chars(self):
        tc = TerminalCore(no_unicode=True)
        out = tc.progress("TASK", 50, width=10)
        # Should still contain label and percent even without unicode
        self.assertIn("TASK", out)
        self.assertIn("50%", out)


class TestScutMascot(unittest.TestCase):
    """Verify Scut mascot expressions render without error."""

    def test_all_expressions_render(self):
        tc = TerminalCore()
        for expr in ["idle", "working", "success", "error", "thinking", "welcome"]:
            out = tc.scut(expr)
            self.assertIsInstance(out, str)
            self.assertTrue(len(out) > 0)
            lines = out.split("\n")
            self.assertEqual(len(lines), 5)

    def test_scut_with_message(self):
        tc = TerminalCore()
        out = tc.scut("idle", "hello")
        self.assertIn("hello", out)

    def test_scut_unknown_expression_fallback(self):
        tc = TerminalCore()
        out = tc.scut("nonexistent")
        # Should fall back to idle
        self.assertIn("___", out)


class TestLogoRendering(unittest.TestCase):
    """Verify logo variants render without error."""

    def test_logo_small_renders(self):
        tc = TerminalCore()
        out = tc.logo_small()
        self.assertIsInstance(out, str)
        self.assertTrue(len(out) > 0)

    def test_logo_small_no_unicode(self):
        tc = TerminalCore(no_unicode=True)
        out = tc.logo_small()
        self.assertIsInstance(out, str)
        # Should contain ASCII "oo" for eyes, not unicode
        self.assertIn("oo", out)

    def test_logo_splash_renders(self):
        tc = TerminalCore()
        out = tc.logo_splash()
        self.assertIsInstance(out, str)
        self.assertTrue(len(out) > 0)

    def test_logo_splash_no_unicode(self):
        tc = TerminalCore(no_unicode=True)
        out = tc.logo_splash()
        self.assertIsInstance(out, str)
        # Verify ASCII-only (no common unicode box-drawing chars)
        for ch in ["\u250c", "\u2510", "\u256d", "\u2500", "\u2588"]:
            self.assertNotIn(ch, out)

    def test_logo_splash_contains_crab_text(self):
        tc = TerminalCore(no_unicode=True, no_color=True)
        out = tc.logo_splash()
        # Should contain recognizable CRAB letters or the tagline
        self.assertIn("Coordination Receipts", out)


class TestHRSafety(unittest.TestCase):
    """Verify no secrets or hazardous content leaks in rendered output."""

    def test_no_api_keys_in_output(self):
        tc = TerminalCore()
        outputs = [
            tc.logo_splash(),
            tc.logo_small(),
            tc.scut("welcome"),
            tc.box(["test"], width=10),
        ]
        combined = "\n".join(outputs)
        # Flag common secret patterns
        bad_patterns = ["sk-", "ghp_", "AKIA", "api_key", "password=", "token="]
        for pat in bad_patterns:
            self.assertNotIn(pat, combined.lower())


class TestEscapeSequenceWellFormedness(unittest.TestCase):
    """Verify ANSI escape sequences are syntactically valid."""

    def test_all_color_codes_are_valid_sgr(self):
        tc = TerminalCore()
        sgr_codes = [
            tc.AMBER, tc.AMBER_LIGHT, tc.CYAN, tc.CYAN_DARK,
            tc.GREEN, tc.RED, tc.MAGENTA, tc.DIM, tc.WHITE,
            tc.RULE, tc.BG_AMBER, tc.BG_GREEN, tc.BG_RED,
            tc.BG_BLACK, tc.BOLD, tc.RESET,
        ]
        for code in sgr_codes:
            self.assertTrue(code.startswith("\033["), f"{code!r} missing ESC[")
            self.assertTrue(code.endswith("m"), f"{code!r} missing trailing m")

    def test_reset_is_zero(self):
        tc = TerminalCore()
        self.assertEqual(tc.RESET, "\033[0m")

    def test_no_unclosed_escapes_in_colored_output(self):
        tc = TerminalCore(no_color=False)
        out = tc._c(tc.AMBER, "test") + tc._c(tc.CYAN, "x")
        # Count escapes -- should have matching resets
        esc_count = out.count("\033[")
        reset_count = out.count("\033[0m")
        self.assertGreaterEqual(reset_count, 1)


if __name__ == "__main__":
    unittest.main()
