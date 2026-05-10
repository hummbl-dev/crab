# CRAB Brand System: Terminal Core & Low-Fi Digital
## Neo-Retro Identity for a Terminal-Native Multi-Agent Protocol

**Status:** Draft v0.1 | **Date:** 2026-05-10  
**Aesthetic:** Inverse Corporate Memphis. Authentic nostalgia. Warm brutalism.  
**Medium:** Terminals, TUIs, ASCII/ANSI art, character-based graphics  
**Mascot:** SCUT (Shell-Compressed Utility Terminal)

---

## 1. Brand Ethos

### The Philosophy

We are not "retro-inspired." We are retro-*native*. CRAB was not designed to look old; it was designed for a world that never stopped being terminal-first. The aesthetic is not a coat of paint on a modern framework — it is the framework.

The design borrows from Anthropic's warmth and intentionality (generous spacing, human tone, serif wordmarks) but renders it through the brutal honesty of a VT100. The result is what we call **"Warm Brutalism"** — caring but unvarnished. Beautiful but unafraid of ASCII.

### Positioning Statement

> CRAB is the coordination protocol for agents that work while you sleep. It does not need a GUI to be comprehensible. It does not need a dashboard to be observable. It needs a bus, a receipt, and a little buddy who remembers what matters.

### Anti-References (What We Reject)

| Corporate Memphis | Terminal Core |
|---|---|
| Flat pastel gradients | Single-color fields with character dithering (░▒▓) |
| Geometric blob mascots | Line-art mascots with expressiveness |
| Rounded rectangles everywhere | Sharp right angles, 1px borders |
| Drop shadows and glows | No shadows. Depth via borders and spacing only. |
| "Friendly" sans-serif | Monospace everywhere. Serif used only for wordmarks in art. |
| Purple-blue gradients for "AI" | Amber, cyan, and magenta on true black |
| Animated loading spinners | Character-based progress (█░░░░) with narrative |

---

## 2. The Aesthetic: Five Principles

### 2.1. True Black, Not Dark Gray

Backgrounds are `\033[40m` (ANSI 0), not `#121212`. True black absorbs light like a CRT in a dark room. It creates a stage. Everything else is a performer.

### 2.2. Warm Phosphor, Not Neon

Primary colors are drawn from vintage monitor phosphors but warmed:
- **Amber** (ANSI 208 / 220) — the warm, inviting glow of a VT220
- **Phosphor Green** (ANSI 82 / 78) — softer than #00FF00, more like a healthy oscilloscope
- **Deep Cyan** (ANSI 81 / 51) — bioluminescent, not electric

These colors degrade gracefully to 16-color terminals:
- 208 → Yellow (ANSI 3)
- 82 → Green (ANSI 2)
- 81 → Cyan (ANSI 6)

### 2.3. Character Dithering for Texture

Where Corporate Memphis uses gradients, Terminal Core uses block-character dithering:

```
███████▓▓▓▓▓▓▓░░░░░░░        Full → 75% → 50% → 25% → empty
```

Allowed dither characters:
- `█` — Full block (100%)
- `▓` — Dark shade (75%)
- `▒` — Medium shade (50%)
- `░` — Light shade (25%)
- ` ` — Empty (0%)

### 2.4. The Rule of One Pixel

Borders are 1 character wide. No double-borders except for the outer frame of a primary container. No rounded corners. Corners are:
- `╭` `╮` `╰` `╯` — Rounded box drawing (preferred)
- `┌` `┐` `└` `┘` — Sharp box drawing (fallback)
- `+` `-` `|` `+` — ASCII fallback

### 2.5. Generous Vertical Spacing

The terminal has infinite scroll. Use it. Separate sections with blank lines. Let content breathe. A TUI should feel like a well-typeset manuscript, not a packed dashboard.

---

## 3. Color System

### 3.1. ANSI Palette (256-Color Terminal)

```
ROLE          ANSI CODE    HEX (APPROX)    VISUAL       16-COLOR FALLBACK
─────────────────────────────────────────────────────────────────────────
Background    0            #000000          ████████     Black
Primary Text  15           #E8E6DE          ████████     White (bright)
Dim Text      245          #8A8C84          ████████     White
Muted         240          #55574F          ████████     White (dim)

Amber         208          #FF8700          ▓▓▓▓▓▓▓▓     Yellow
Amber-Light   220          #FFD700          ▓▓▓▓▓▓▓▓     Yellow (bright)

Cyan          81           #5FD7FF          ▒▒▒▒▒▒▒▒     Cyan
Cyan-Dark     37           #00AFAF          ▒▒▒▒▒▒▒▒     Cyan (dim)

Magenta       201          #FF00FF          ░░░░░░░░     Magenta
Magenta-Soft  213          #FF87FF          ░░░░░░░░     Magenta (bright)

Green         82           #5FFF00          ████████     Green
Green-Soft    78           #5FD700          ████████     Green (dim)

Red           203          #FF5F5F          ████████     Red
Red-Soft      160          #D70000          ████████     Red (dim)

Rule Line     237          #3A3A3A          ────────     Black (bright)
```

### 3.2. Color Application

| Element | Color | Rationale |
|---------|-------|-----------|
| Primary actions / CTA | Amber (208) | Warm invitation to act |
| Secondary / info | Cyan (81) | Cool, neutral, informative |
| Accent / highlight | Magenta (201) | Rare, draws the eye |
| Success / nominal | Green-Soft (78) | Not jarring, still celebratory |
| Warning / caution | Amber (208) | Same as primary, context changes meaning |
| Error / emergency | Red-Soft (160) | Visible without being alarming |
| Borders / chrome | Rule Line (237) | Recedes, structures without demanding attention |
| Active selection | Cyan-Dark (37) bg + Primary Text (15) fg | Deep sea highlight |

### 3.3. Theme Variants

The dashboard supports 4 themes. These are the Terminal Core equivalents:

**Amber (Default)** — `\033[38;5;208m` primary on `\033[40m` black  
The classic. Warm, safe, inviting. Like working on a VT220 in a basement at 2am.

**Phosphor** — `\033[38;5;82m` green on `\033[40m` black  
The hacker movie aesthetic but softened. Not "university terminal room" green — "deep ocean bioluminescence" green.

**Cyanotype** — `\033[38;5;81m` cyan on `\033[40m` black  
The blueprint aesthetic. Technical, precise, architectural.

**Paper** — `\033[38;5;0m` black on `\033[48;5;230m` warm white  
For bright environments. Inverts the palette. Still Terminal Core because it uses the same spacing and border rules.

---

## 4. Typography

### 4.1. The Golden Rule

**Everything is monospace.** No exceptions. UI, body, headers, data, art. If it is not monospace, it is not Terminal Core.

### 4.2. Heading Hierarchy

```
H1: UPPERCASE WITH FULL WIDTH RULE
══════════════════════════════════════════════════
H2: Title Case With Single Width Rule
──────────────────────────────────────────────────
H3: Sentence case, no rule, just breathing room
H4: Inline — used for labels and field names
```

### 4.3. ASCII Wordmark

For large headers, use a custom ASCII wordmark rather than plain text. It signals craft:

```
   ██████╗██████╗  █████╗ ██████╗ 
  ██╔════╝██╔══██╗██╔══██╗██╔══██╗
  ██║     ██████╔╝███████║██████╔╝
  ██║     ██╔══██╗██╔══██║██╔══██╗
  ╚██████╗██║  ██║██║  ██║██████╔╝
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ 
```

This is reserved for splash screens, release notes, and ceremonial moments. Do not overuse it.

### 4.4. The Serif Exception

In ASCII art wordmarks, serif terminals may be suggested with extra pixels:

```
      _/_/_/_/  _/_/_/      _/_/    _/_/_/    
   _/        _/    _/  _/    _/  _/    _/   
  _/        _/_/_/    _/_/_/_/  _/_/_/      
 _/        _/    _/  _/    _/  _/    _/     
  _/_/_/  _/    _/  _/    _/  _/_/_/        
```

This is the "literary warmth" borrowed from Anthropic. A brand that deals in language should feel like it reads books.

---

## 5. Logo System

### 5.1. Primary Mark: The Hexapod Shell

A hexagon that reads as both a "C" (for CRAB) and a crab carapace. Works at any scale.

**Small (8x6, favicon-equivalent):**

```
   ╭──╮
  ╱ ◠◠ ╲
 │  ⏝  │
  ╰────╯
```

**Medium (16x9, TUI header icon):**

```
      ╭────────╮
     ╱    ◠◠    ╲
    │  ╱──────╲  │
    │ │   CRAB  │ │
     ╲ ╰──────╯ ╱
      ╰────────╯
```

**Large (32x12, splash screen):**

```
           ╭──────────────────╮
          ╱                    ╲
         │     ◠◠      ◠◠      │
         │    ╱  ╲    ╱  ╲     │
         │   │ <> │  │ <> │    │
          ╲   ╲──╱    ╲──╱    ╱
           ╲    ╲──────╱      ╱
            ╰────────────────╯
```

### 5.2. Logotype: The Receipt

A horizontal mark that looks like a printed receipt — appropriate for a protocol about receipts:

```
┌──────────────────────────────────────┐
│  2026-05-10 02:17:09 UTC             │
│  FROM: crab-daemon                   │
│  TYPE: STATUS                        │
│  MSG:  CRAB  v1.0.0  SHIPPED         │
│                                      │
│  ══════════════════════════════════  │
│            Thank you.                │
└──────────────────────────────────────┘
```

### 5.3. The Seal

For use in documentation, footers, and certification:

```
      ╭─────────────╮
     │   ┌─────┐   │
     │   │ ◠◠ │   │
     │   │  ⏝  │   │
     │   └──┬──┘   │
     │  CRAB 1.0  │
      ╰─────────────╯
```

---

## 6. Mascot: SCUT

### 6.1. Who Is Scut?

Scut is a small crab-like utility creature who lives in your terminal. He is not an AI. He is a companion — a "little buddy" who observes, remembers, and occasionally interjects with observations that are useful but never intrusive.

**Design principles:**
- Small enough to fit in a 6-line terminal status area
- Expressive through simple line changes (eyes, claws, posture)
- Can hold or interact with terminal elements (cursors, scrollbars, receipt icons)
- Wears a tiny hard hat when performing maintenance
- Has a small notepad he writes on when he learns something about your project

**Personality:**
- Curious but polite (he waits for idle moments)
- Proud of his memory (he references things he learned hours ago)
- Gentle humor (puns about shells, tides, and legs)
- Serious when systems are in error (he stands very still)

### 6.2. Scut Expressions

**Idle (breathing):**
```
    ___
   /o o\
  (  >  )  ~
   \___/
   | | |
```

**Working (tapping claws):**
```
    ___
   /o o\
  (  >  )  *tap* *tap*
   \___/
   > | <
```

**Thinking (one claw on chin):**
```
    ___
   /-.o\
  (  >  )  ...
   \___/
   |\| |
```

**Error (frozen, wide eyes):**
```
    ___
   /O O\
  (  o  )
   \___/
   | | |
```

**Success (celebrating, both claws up):**
```
    ___
   /o o\
  (  ^  )  \o/
   \___/
   \ | /
```

**Asleep (terminal idle >5 min):**
```
    ___
   /- -\
  (  -  )  zzz
   \___/
   | | |
```

**Waving goodbye (session end):**
```
    ___
   /o o\
  (  ^  )  bye!
   \___/
   / | \
```

### 6.3. Scut in Context

**As a status bar companion:**

```
╭──────────────── Status ────────────────╮  ___
│                                          │ /o o\
│  Bus:  ACTIVE   │   Agents: 9 online   │(  >  )  All clear!
│                                          │ \___/
╰──────────────────────────────────────────╯  | | |
```

**Delivering a receipt:**

```
    ___
   /o o\      ┌─────────────────────────────┐
  (  ^  )────→│  RECEIPT                      │
   \___/      │  Agent: git-audit             │
   | | |      │  Status: NOMINAL              │
              │  Action: No stale branches    │
              └─────────────────────────────┘
```

**During a blocker:**

```
    ___
   /O O\   ⚠  BLOCKED: unresolved blocker
  (  o  )      from: codex at 02:14:00Z
   \___/
   | | |      I'm waiting here until it clears.
```

### 6.4. Scut's "Little Buddy" Memory

Scut remembers things about your project and references them later. This is not a full RAG system — it is a **small, curated memory** (the "tucked tail" of the crustacean paradigm).

Example interactions:

```
[Scut] You haven't run the cleanup lane in 3 days. 
       Want me to schedule it? [y/n/remind me later]

[Scut] Welcome back! Last time you were working on 
       the topology-page.tsx refactor. Want to resume?

[Scut] 3 days since last BLOCKED message. 
       That's a new record! 🦀

[Scut] I noticed you always run --lane cleanup before 
       --lane git-audit. Shall I make that the default?
```

These are contextual, not chatty. Scut speaks in receipts, not paragraphs.

---

## 7. TUI Chrome System

### 7.1. Primary Container (Double Border)

For the main application window:

```
╔══════════════════════════════════════════════════╗
║  HUMMBL Console                    v0.3.0-dev  ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  [Content area]                                  ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

### 7.2. Secondary Container (Single Border)

For panels, cards, and modals:

```
┌────────────────────────────────────┐
│  Agent Fleet                       │
├────────────────────────────────────┤
│  claude-code  ● NOMINAL            │
│  codex        ○ IDLE               │
│  gemini       ● NOMINAL            │
└────────────────────────────────────┘
```

### 7.3. Tertiary Container (Dashed Border)

For inactive or collapsed panels:

```
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
╎  System Map (collapsed)                ╎
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
```

### 7.4. Separator Rules

```
Single: ────────────────────────────────────
Double: ════════════════════════════════════
Dashed: · · · · · · · · · · · · · · · · ·
Dotted: ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙
```

### 7.5. Header Pattern

```
╭─────── Agent Fleet ───────╮
│                           │
│  🦀  9 agents online     │
│                           │
╰───────────────────────────╯
```

Note: The emoji is optional. In strict ASCII mode, use Scut's small form:

```
╭─────── Agent Fleet ───────╮
│   ___                     │
│  /o o\  9 agents online   │
│  \___/                    │
╰───────────────────────────╯
```

### 7.6. Receipt / Card Pattern

For individual bus messages, agent status cards, or audit entries:

```
┌──[STATUS]─────────────────────[02:17:09Z]──┐
│                                             │
│  FROM: crab-daemon                          │
│  LANE: cleanup                              │
│                                             │
│  No stale [gone] branches found.            │
│  Worktree clean (no untracked).             │
│                                             │
└─────────────────────────────────────────────┘
```

### 7.7. Status Pill Pattern

```
[NOMINAL]  [WARN]  [EMERGENCY]  [IDLE]  [BUSY]
```

Rendered with color:

```
\033[48;5;78;38;5;0m NOMINAL \033[0m
\033[48;5;208;38;5;0m WARN \033[0m
\033[48;5;160;38;5;15m EMERGENCY \033[0m
```

### 7.8. Progress Bar

```
Phase: CHECK  [████████████░░░░░░░░]  60%
        REASON [████████░░░░░░░░░░░░]  40%
        ACT    [░░░░░░░░░░░░░░░░░░░░]   0%
        BUS    [░░░░░░░░░░░░░░░░░░░░]   0%
```

Each phase is a lane. The bar fills as the agent completes its turn.

---

## 8. The "Little Buddy" Feature Specification

### 8.1. Core Concept

The Little Buddy is a persistent, project-aware companion that lives in the terminal. It is not a chatbot. It is an **ambient intelligence** — it observes, learns, and surfaces observations at the right moment.

**Key difference from Clippy:**
- Clippy interrupted. The Little Buddy waits for idle moments.
- Clippy was generic. The Little Buddy learns your specific project patterns.
- Clippy was a salesman. The Little Buddy is a coworker.

### 8.2. Memory Model

The Little Buddy stores a `buddy-memory.jsonl` in the project root (not committed to git):

```jsonl
{"t":"2026-05-10T02:00:00Z","type":"pattern","data":{"lane":"cleanup","frequency":"daily","time":"02:00"}}
{"t":"2026-05-10T02:15:00Z","type":"milestone","data":{"days_since_blocker":3}}
{"t":"2026-05-10T02:17:00Z","type":"context","data":{"last_branch":"feature/crab-branding","last_file":"docs/branding/TERMINAL_CORE_BRAND.md"}}
```

This is the "tucked tail" — compressed, personal, ephemeral.

### 8.3. Interaction Patterns

**Observation (no action required):**
```
[Scut] 3 days since last BLOCKED. New record! 🦀
```

**Suggestion (soft prompt, default = no):**
```
[Scut] You run cleanup before git-audit 90% of the time.
       Make that the default order? [y/N]
```

**Reminder (time-based, dismissible):**
```
[Scut] It's been 24h since the last bus audit. 
       Run one now? [Y/n/remind later]
```

**Celebration (milestone reached):**
```
    ___
   /o o\   ✨  1000 receipts posted!
  (  ^  )      All agents nominal.
   \___/
   \ | /
```

**Error companion (present but not alarmist):**
```
    ___
   /O O\   A lane failed. I've saved the log.
  (  o  )      Want to see it? [Y/n/skip]
   \___/
   | | |
```

### 8.4. Idle Animations

When the terminal is idle (>30s), Scut performs small ambient animations:

```
Frame 1:    Frame 2:    Frame 3:    Frame 4:
    ___        ___        ___        ___
   /o o\      /o o\      /o -\      /o o\
  (  >  )    (  >  )~   (  >  )    (  >  )
   \___/      \___/      \___/      \___/
   | | |      | | |      | | |      | | |
```

These are non-distracting. They signal "the system is alive and watching."

---

## 9. Application: Complete TUI Mockup

### 9.1. The Dashboard Header

```
╔══════════════════════════════════════════════════════════════════╗
║  HUMMBL Console                                      v0.3.0-dev ║
╠══════════════════════════════════════════════════════════════════╣
║  PULSE: \033[38;5;78m● NOMINAL\033[0m    KILL: \033[38;5;245mDISENGAGED\033[0m    2026-05-10 02:17:09 UTC ║
╚══════════════════════════════════════════════════════════════════╝
```

### 9.2. The Sidebar

```
╭── Navigation ───╮
│                 │
│  1  Overview    │
│  ·  System Map  │
│  2  Agents      │
│  3  Foundry     │
│  4  Services    │
│  5  Bus         │
│  6  Ops         │
│  7  Security    │
│  8  Governance  │
│  9  Audit       │
│                 │
│  \033[38;5;78m● Bus: ACTIVE\033[0m   │
╰─────────────────╯
```

### 9.3. Agent Fleet Panel

```
┌─────────── Agent Fleet ────────────────────┐
│                                            │
│  \033[38;5;78m●\033[0m  claude-code    NOMINAL    14m ago    │
│  \033[38;5;78m●\033[0m  devin           NOMINAL    2h ago     │
│  \033[38;5;208m●\033[0m  gemini          WARN       5m ago     │
│  \033[38;5;78m●\033[0m  opencode        NOMINAL    1h ago     │
│  \033[38;5;245m○\033[0m  codex           IDLE       3d ago     │
│                                            │
│  \033[38;5;81m9 active  │  1 retired  │  2 under AIP\033[0m  │
│                                            │
└────────────────────────────────────────────┘
```

### 9.4. Bus Stream (Live Ticker)

```
╭── Coordination Bus (live) ──╮
│  02:17:09  crab  →  STATUS  │
│  02:16:45  codex →  BLOCKED │
│  02:15:22  apex  →  ACK     │
│  02:14:01  gemini→  STATUS  │
│  02:12:58  devin →  STATUS  │
╰─────────────────────────────╯
```

### 9.5. Scut's Corner (Status + Buddy)

```
    ___
   /o o\  
  (  ^  )  All systems nominal.
   \___/   3 days since last blocker.
   | | |   [Scut remembers you like it quiet.]
```

### 9.6. Full Dashboard Layout

```
╔══════════════════════════════════════════════════════════════════╗
║  HUMMBL Console                                      v0.3.0-dev ║
╠══════════════════════════════════════════════════════════════════╣
║  PULSE: ● NOMINAL    KILL: DISENGAGED    2026-05-10 02:17:09 UTC ║
╠════╦══════════════════════════════════════════╦════════════════╣
║    ║                                          ║                ║
║  1 ║  ┌─────── Agent Fleet ─────────────────┐ ║  ╭────────────╮║
║  · ║  │                                     │ ║  │ Bus Stream │║
║  2 ║  │  ● claude-code   NOMINAL   14m ago  │ ║  │            │║
║  3 ║  │  ● devin          NOMINAL   2h ago  │ ║  │ 02:17:09..│║
║  4 ║  │  ● gemini         WARN      5m ago  │ ║  │ 02:16:45..│║
║  5 ║  │  ● opencode       NOMINAL   1h ago  │ ║  │ 02:15:22..│║
║  6 ║  │  ○ codex          IDLE      3d ago  │ ║  │            │║
║  7 ║  │                                     │ ║  ╰────────────╯║
║  8 ║  │  9 active │ 1 retired │ 2 under AIP │ ║                ║
║  9 ║  └─────────────────────────────────────┘ ║    ___         ║
║    ║                                          ║   /o o\        ║
║    ║  ┌─────── System Health ───────────────┐ ║  (  ^  )       ║
║    ║  │                                     │ ║   \___/        ║
║    ║  │  CPU:  12%    MEM:  4.2GB           │ ║   | | |        ║
║    ║  │  DISK: 67%    NET:  2.1MB/s        │ ║                ║
║    ║  │                                     │ ║  All clear!    ║
║    ║  └─────────────────────────────────────┘ ║                ║
╚════╩══════════════════════════════════════════╩════════════════╝
```

---

## 10. Sound & Motion (Textual)

Terminal Core has no audio. All "sound" is rendered textually.

### 10.1. Activity Indicators

```
[ Working ]     [ Working. ]     [ Working.. ]    [ Working... ]
```

```
[ ░░░░░░░░ ]    [ ██░░░░░░ ]    [ █████░░░ ]    [ ████████ ]
```

```
  ●○○○○         ○●○○○         ○○●○○         ○○○●○         ○○○○●
```

### 10.2. "Chime" Events

Instead of a beep, Terminal Core uses a visual chime — a brief flash of the status line:

```
\033[48;5;208;38;5;0m  ✓ RECEIPT CAPTURED  \033[0m
```

This appears for 500ms then fades back to normal. It is the terminal equivalent of a notification sound.

### 10.3. Scroll Behavior

New bus messages do not jump-scroll. They push content up smoothly, one line at a time, like a teletype. The effect is achieved by printing a newline and the new message — no animation framework needed.

---

## 11. Implementation Notes

### 11.1. Terminal Compatibility

| Feature | Requires | Fallback |
|---------|----------|----------|
| Rounded corners `╭╮╰╯` | UTF-8 + box drawing | Sharp corners `┌┐└┘` |
| 256-color ANSI | `TERM=xterm-256color` | 16-color palette |
| Dithering `▓▒░` | Unicode | Pure ASCII `#*:.` |
| Emoji | Unicode 8.0+ | ASCII art Scut |
| Double borders `╔╗` | Box drawing support | Single borders `┌┐` |

### 11.2. Python Rendering

```python
# Color helper
class TC:
    AMBER = "\033[38;5;208m"
    CYAN = "\033[38;5;81m"
    GREEN = "\033[38;5;78m"
    RED = "\033[38;5;160m"
    DIM = "\033[38;5;245m"
    RESET = "\033[0m"
    BOLD = "\033[1m"

# Border helpers
BORDER = {
    "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
    "h": "─", "v": "│",
}

def render_card(title: str, body: str, width: int = 40) -> str:
    top = f"{BORDER['tl']}{BORDER['h'] * (width - 2)}{BORDER['tr']}"
    mid = f"{BORDER['v']} {title:<{width-4}} {BORDER['v']}"
    sep = f"├{'─' * (width - 2)}┤"
    bottom = f"{BORDER['bl']}{BORDER['h'] * (width - 2)}{BORDER['br']}"
    return "\n".join([top, mid, sep, body, bottom])
```

### 11.3. Accessibility

- All color pairs meet WCAG contrast when rendered on true black
- Scut's expressions are described in alt-text when used in documentation
- Status is always communicated via text + color (never color alone)
- The `NO_COLOR` environment variable is respected (all escape codes stripped)

---

## 12. Receipt

- **Brand system document:** this file
- **Mascot:** SCUT, 6-line ASCII crab companion
- **Logo:** Hexapod Shell mark (3 sizes)
- **Palette:** 11-color ANSI system with 16-color fallback
- **Chrome:** 4 border weights, 4 separator styles
- **Feature spec:** Little Buddy ambient intelligence
- **Next gate:** Implement Scut in the dashboard sidebar + bus notifications

---

*"The best interface is one that feels like it was always there — not because it is invisible, but because it is honest."*
