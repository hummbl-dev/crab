#!/usr/bin/env python3
"""
Terminal Core Brand Demo — CRAB TUI Chrome Renderer
====================================================
Usage: python terminal_core_demo.py [--no-color] [--no-unicode]

A self-contained demo of the Terminal Core aesthetic showing:
- Splash screen with ANSI-colored logo
- Scut mascot expressions
- TUI chrome containers
- Receipt cards
- Status pills
- Progress bars
- The Little Buddy interaction pattern

This module has zero third-party dependencies. It uses only Python stdlib.
"""

import os
import re
import sys
import time

# ANSI escape sequence pattern for stripping
_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

# Force UTF-8 output on Windows and other platforms with narrow default encodings
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


class TerminalCore:
    """Renderer for the Terminal Core aesthetic."""

    # 256-color ANSI palette
    AMBER = "\033[38;5;208m"
    AMBER_LIGHT = "\033[38;5;220m"
    CYAN = "\033[38;5;81m"
    CYAN_DARK = "\033[38;5;37m"
    GREEN = "\033[38;5;78m"
    RED = "\033[38;5;160m"
    MAGENTA = "\033[38;5;201m"
    DIM = "\033[38;5;245m"
    WHITE = "\033[38;5;15m"
    RULE = "\033[38;5;237m"
    BG_AMBER = "\033[48;5;208m"
    BG_GREEN = "\033[48;5;78m"
    BG_RED = "\033[48;5;160m"
    BG_BLACK = "\033[40m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    # Border character sets
    ROUNDED = {"tl": "\u256d", "tr": "\u256e", "bl": "\u2570", "br": "\u256f", "h": "\u2500", "v": "\u2502", "sep": "\u251c", "ser": "\u2524"}
    SHARP = {"tl": "\u250c", "tr": "\u2510", "bl": "\u2514", "br": "\u2518", "h": "\u2500", "v": "\u2502", "sep": "\u251c", "ser": "\u2524"}
    DOUBLE = {"tl": "\u2554", "tr": "\u2557", "bl": "\u255a", "br": "\u255d", "h": "\u2550", "v": "\u2551", "sep": "\u2560", "ser": "\u2563"}
    ASCII = {"tl": "+", "tr": "+", "bl": "+", "br": "+", "h": "-", "v": "|", "sep": "+", "ser": "+"}

    def __init__(self, no_color: bool = False, no_unicode: bool = False):
        self.no_color = no_color or bool(os.environ.get("NO_COLOR"))
        self.no_unicode = no_unicode
        self.borders = self.ASCII if no_unicode else self.ROUNDED

    def _c(self, code: str, text: str) -> str:
        """Wrap text in color code if color is enabled."""
        if self.no_color:
            return text
        return f"{code}{text}{self.RESET}"

    def border_set(self, style: str = "rounded") -> dict:
        if self.no_unicode:
            return self.ASCII
        return {
            "rounded": self.ROUNDED,
            "sharp": self.SHARP,
            "double": self.DOUBLE,
        }.get(style, self.ROUNDED)

    def hr(self, width: int = 50, char: str = "\u2500", color: str = None) -> str:
        c = color or self.RULE
        return self._c(c, char * width)

    def box(self, lines: list[str], width: int = 40, style: str = "rounded",
            border_color: str = None, title: str = None) -> str:
        """Render a bordered box."""
        b = self.border_set(style)
        bc = border_color or self.CYAN
        out = []
        out.append(f"{bc}{b['tl']}{b['h'] * (width - 2)}{b['tr']}{self.RESET}")

        def _vis(text: str) -> int:
            return len(_ANSI_RE.sub("", text))

        if title:
            pad = width - len(title) - 4
            tline = f"{b['v']} {self._c(self.WHITE, self.BOLD + title)}{' ' * pad} {b['v']}"
            out.append(self._c(bc, tline))
            s = f"{b['sep']}{b['h'] * (width - 2)}{b['ser']}"
            out.append(self._c(bc, s))

        for line in lines:
            visible_len = _vis(line)
            pad = max(0, width - visible_len - 4)
            l = f"{b['v']} {line}{' ' * pad} {b['v']}"
            out.append(self._c(bc, l))

        bot = f"{b['bl']}{b['h'] * (width - 2)}{b['br']}"
        out.append(self._c(bc, bot))
        return "\n".join(out)

    def pill(self, text: str, color: str = "green") -> str:
        """Render a status pill."""
        colors = {
            "green": (self.BG_GREEN, self.RESET + self.WHITE),
            "amber": (self.BG_AMBER, self.RESET + self.WHITE),
            "red": (self.BG_RED, self.RESET + self.WHITE),
            "dim": (self._c(self.DIM, "") + self.BG_BLACK, self.RESET),
        }
        bg, fg = colors.get(color, colors["dim"])
        if self.no_color:
            return f"[{text}]"
        return f"{bg} {text} {self.RESET}"

    def progress(self, label: str, pct: int, width: int = 20) -> str:
        """Render a progress bar."""
        filled = int(width * pct / 100)
        bar = "\u2588" * filled + "\u2591" * (width - filled)
        return f"{self._c(self.DIM, label.ljust(8))} {self._c(self.AMBER, bar)} {self._c(self.DIM, str(pct) + '%')}"

    def scut(self, expression: str = "idle", message: str = "") -> str:
        """Render Scut the mascot with an expression and optional message."""
        expressions = {
            "idle": [
                "    ___",
                "   /o o\\",
                "  (  >  )  ~",
                "   \\___/",
                "   | | |",
            ],
            "working": [
                "    ___",
                "   /o o\\",
                "  (  >  )  *tap* *tap*",
                "   \\___/",
                "   > | <",
            ],
            "success": [
                "    ___",
                "   /o o\\",
                "  (  ^  )  \\o/",
                "   \\___/",
                "   \\ | /",
            ],
            "error": [
                "    ___",
                "   /O O\\",
                "  (  o  )",
                "   \\___/",
                "   | | |",
            ],
            "thinking": [
                "    ___",
                "   /-.o\\",
                "  (  >  )  ...",
                "   \\___/",
                "   |\\| |",
            ],
            "welcome": [
                "    ___",
                "   /o o\\",
                "  (  ^  )  Hi! I'm Scut.",
                "   \\___/",
                "   / | \\   I'll watch your lanes.",
            ],
        }
        art = expressions.get(expression, expressions["idle"])
        colored = [self._c(self.AMBER, line) for line in art]
        if message:
            colored[-1] = colored[-1] + "  " + self._c(self.DIM, message)
        return "\n".join(colored)

    def logo_small(self) -> str:
        if self.no_unicode:
            return "\n".join([
                self._c(self.AMBER, "  ___"),
                self._c(self.AMBER, " /") + self._c(self.WHITE, "oo") + self._c(self.AMBER, "\\"),
                self._c(self.AMBER, "(    )"),
                self._c(self.AMBER, " \\___/"),
            ])
        return "\n".join([
            self._c(self.AMBER, "  ___"),
            self._c(self.AMBER, " /") + self._c(self.WHITE, "\u25e0\u25e0") + self._c(self.AMBER, "\\"),
            self._c(self.AMBER, "(    )"),
            self._c(self.AMBER, " \\___/"),
        ])

    def logo_splash(self) -> str:
        if self.no_unicode:
            return "\n".join([
                self._c(self.AMBER, "           +------------------+"),
                self._c(self.AMBER, "          /                    \\"),
                self._c(self.AMBER, "         |   ") + self._c(self.WHITE, "oo") + self._c(self.AMBER, "      ") + self._c(self.WHITE, "oo") + self._c(self.AMBER, "      |"),
                self._c(self.AMBER, "         |  ") + self._c(self.WHITE, "/  \\") + self._c(self.AMBER, "    ") + self._c(self.WHITE, "/  \\") + self._c(self.AMBER, "     |"),
                self._c(self.AMBER, "         | ") + self._c(self.WHITE, "|    |  |    |") + self._c(self.AMBER, "    |"),
                self._c(self.AMBER, "          \\  ") + self._c(self.WHITE, "\\--/    \\--/") + self._c(self.AMBER, "    /"),
                self._c(self.AMBER, "           \\    ") + self._c(self.WHITE, "\\------/") + self._c(self.AMBER, "      /"),
                self._c(self.AMBER, "            +----------------+"),
                "",
                self._c(self.AMBER, "   ______ _____  _____  _____ "),
                self._c(self.AMBER, "  /  ____|  __ ||  __ ||  ___|"),
                self._c(self.AMBER, " |  |    | |__| | |  | | |__  "),
                self._c(self.AMBER, " |  |    |  _  /| |  | |  __| "),
                self._c(self.AMBER, " |  |___ | | > > |__| | |___ "),
                self._c(self.AMBER, "  >_____|_|  >_>_____/|_____|"),
                "",
                self._c(self.CYAN, "    Coordination Receipts for Agent Behavior"),
                self._c(self.DIM, "    Check  ->  Reason  ->  Act  ->  Bus"),
            ])
        return "\n".join([
            self._c(self.AMBER, "           \u256d\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256e"),
            self._c(self.AMBER, "          \u2571                    \u2572"),
            self._c(self.AMBER, "         \u2502   ") + self._c(self.WHITE, "\u25e0\u25e0") + self._c(self.AMBER, "      ") + self._c(self.WHITE, "\u25e0\u25e0") + self._c(self.AMBER, "      \u2502"),
            self._c(self.AMBER, "         \u2502  ") + self._c(self.WHITE, "/  \\") + self._c(self.AMBER, "    ") + self._c(self.WHITE, "/  \\") + self._c(self.AMBER, "     \u2502"),
            self._c(self.AMBER, "         \u2502 ") + self._c(self.WHITE, "\u2502    \u2502  \u2502    \u2502") + self._c(self.AMBER, "    \u2502"),
            self._c(self.AMBER, "          \u2572  ") + self._c(self.WHITE, "\\\u2500\u2500\u257f    \\\u2500\u2500\u257f") + self._c(self.AMBER, "    \u2571"),
            self._c(self.AMBER, "           \u2572    ") + self._c(self.WHITE, "\\\u2500\u2500\u2500\u2500\u2500\u2571") + self._c(self.AMBER, "      \u2571"),
            self._c(self.AMBER, "            \u2570\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u256f"),
            "",
            self._c(self.AMBER, "   \u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2557  \u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2588\u2588\u2588\u2588\u2557 "),
            self._c(self.AMBER, "  \u255a\u2550\u2550\u2550\u2550\u2550\u2557\u255a\u2550\u2550\u2550\u2550\u2550\u2557\u2588\u255a\u2550\u2550\u2550\u2550\u2588\u2557\u255a\u2550\u2550\u2550\u2550\u2588\u2557"),
            self._c(self.AMBER, "  \u2588\u2588\u2588\u2557    \u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d"),
            self._c(self.AMBER, "  \u2588\u2588\u2588\u2557    \u2588\u2588\u255a\u2550\u2550\u2588\u2588\u2557\u2588\u255a\u2550\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u255a\u2550\u2550\u2588\u2588\u2557 "),
            self._c(self.AMBER, "  \u2559\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2551  \u2588\u2588\u2588\u2557\u2588\u2588\u2551  \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d"),
            self._c(self.AMBER, "   \u255a\u2550\u2550\u2550\u2550\u2550\u255d\u255a\u2551  \u255a\u2551\u255a\u2551  \u255a\u2551\u255a\u2551\u255a\u2550\u2550\u2550\u2550\u2550\u255d "),
            "",
            self._c(self.CYAN, "    Coordination Receipts for Agent Behavior"),
            self._c(self.DIM, "    Check  \u2192  Reason  \u2192  Act  \u2192  Bus"),
        ])


def _wait(tc: TerminalCore, auto: bool = False):
    """Wait for Enter or auto-advance in non-interactive environments."""
    if auto:
        time.sleep(0.3)
        return
    try:
        input()
    except EOFError:
        time.sleep(0.3)


def demo_splash(tc: TerminalCore, auto: bool = False):
    print(tc._c(tc.BG_BLACK, "") + tc.logo_splash())
    print()
    print(tc._c(tc.DIM, "    Press Enter to continue..."))
    _wait(tc, auto)


def demo_scut(tc: TerminalCore, auto: bool = False):
    print(tc._c(tc.BG_BLACK, ""))
    print(tc._c(tc.WHITE, "=== SCUT EXPRESSIONS ==="))
    print()
    for expr in ["welcome", "idle", "working", "thinking", "success", "error"]:
        print(tc.scut(expr))
        print()
    print(tc._c(tc.DIM, "Press Enter to continue..."))
    _wait(tc, auto)


def demo_chrome(tc: TerminalCore, auto: bool = False):
    print(tc._c(tc.BG_BLACK, ""))
    print(tc._c(tc.WHITE, "=== TUI CHROME ==="))
    print()

    # Primary container
    print(tc.box(
        [tc._c(tc.DIM, "Content area")],
        width=50, style="double", border_color=tc.AMBER,
        title="HUMMBL Console v0.3.0-dev"
    ))
    print()

    # Secondary panel
    print(tc.box(
        [
            tc._c(tc.GREEN, "\u25cf") + tc._c(tc.WHITE, " claude-code  NOMINAL   14m ago"),
            tc._c(tc.DIM, "\u25cb codex         IDLE     3d ago"),
            tc._c(tc.GREEN, "\u25cf") + tc._c(tc.WHITE, " gemini        NOMINAL  5m ago"),
        ],
        width=40, style="rounded", border_color=tc.CYAN,
        title="Agent Fleet"
    ))
    print()

    # Receipt card
    print(tc.box(
        [
            tc._c(tc.WHITE, "FROM: ") + tc._c(tc.AMBER, "crab-daemon"),
            tc._c(tc.WHITE, "LANE: ") + tc._c(tc.CYAN, "cleanup"),
            "",
            tc._c(tc.WHITE, "No stale [gone] branches found."),
            tc._c(tc.WHITE, "Worktree clean (no untracked)."),
        ],
        width=45, style="sharp", border_color=tc.CYAN,
        title="[STATUS] \u2014 02:17:09Z"
    ))
    print()

    # Status pills
    print(tc._c(tc.WHITE, "Status pills: ") +
          tc.pill("NOMINAL", "green") + "  " +
          tc.pill("WARN", "amber") + "  " +
          tc.pill("EMERGENCY", "red"))
    print()

    # Progress bars
    print(tc._c(tc.WHITE, "Progress:"))
    print(tc.progress("CHECK", 100, 20))
    print(tc.progress("REASON", 60, 20))
    print(tc.progress("ACT", 0, 20))
    print(tc.progress("BUS", 0, 20))
    print()

    print(tc._c(tc.DIM, "Press Enter to continue..."))
    _wait(tc, auto)


def demo_little_buddy(tc: TerminalCore, auto: bool = False):
    print(tc._c(tc.BG_BLACK, ""))
    print(tc._c(tc.WHITE, "=== LITTLE BUDDY INTERACTIONS ==="))
    print()

    # Observation
    print(tc.scut("idle", "3 days since last BLOCKED. New record!"))
    print()

    # Suggestion
    print(tc.scut("thinking", "You run cleanup before git-audit 90% of the time."))
    print(tc._c(tc.DIM, "              Make that the default order? [y/N]"))
    print()

    # Celebration
    print(tc.scut("success", "1000 receipts posted!"))
    print()

    # Error companion
    print(tc.scut("error", "A lane failed. I've saved the log."))
    print(tc._c(tc.DIM, "              Want to see it? [Y/n/skip]"))
    print()

    print(tc._c(tc.DIM, "Press Enter to exit..."))
    _wait(tc, auto)


def main():
    no_color = "--no-color" in sys.argv
    no_unicode = "--no-unicode" in sys.argv
    auto_advance = "--auto-advance" in sys.argv
    no_clear = "--no-clear" in sys.argv

    tc = TerminalCore(no_color=no_color, no_unicode=no_unicode)

    # Clear screen if possible
    if not no_clear:
        os.system("cls" if os.name == "nt" else "clear")

    demo_splash(tc, auto=auto_advance)
    if not no_clear:
        os.system("cls" if os.name == "nt" else "clear")

    demo_scut(tc, auto=auto_advance)
    if not no_clear:
        os.system("cls" if os.name == "nt" else "clear")

    demo_chrome(tc, auto=auto_advance)
    if not no_clear:
        os.system("cls" if os.name == "nt" else "clear")

    demo_little_buddy(tc, auto=auto_advance)

    # Reset terminal
    print(tc.RESET)


if __name__ == "__main__":
    main()