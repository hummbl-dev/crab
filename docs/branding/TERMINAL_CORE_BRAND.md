# CRAB Brand System: Terminal Core & Low-Fi Digital
## Neo-Retro Identity for a Terminal-Native Multi-Agent Protocol

**Status:** Draft v1.2 | **Date:** 2026-05-10  
**Aesthetic:** Neo-ANSI Revival. Inverse Corporate Memphis. Warm brutalism.  
**Medium:** Terminals, TUIs, ASCII/ANSI art, character-based graphics  
**Mark:** Canonical CRAB (armored, decapod, governance-facing)  
**Mascot:** SCUT — The Crab's Friend (cyan crablet companion)  
**HUMMBL Mark:** BERNARD — The Hummingbird (iridescent green, belonging-aware)

---

## 1. Brand Ethos

### The Philosophy

We are not "retro-inspired." We are retro-*native*. CRAB was not designed to look old; it was designed for a world that never stopped being terminal-first. The aesthetic is not a coat of paint on a modern framework — it is the framework.

The design borrows from Anthropic's warmth and intentionality (generous spacing, human tone, serif wordmarks) but renders it through the brutal honesty of a VT100. The result is what we call **"Warm Brutalism"** — caring but unvarnished. Beautiful but unafraid of ASCII.

### The Lineage: 130 Years of Character-Density Art

We are not inventing an aesthetic. We are **reviving a craft**. Terminal Core inherits from:

```
1898: Flora Stacey — typewriter butterfly (overstrike density)
   ↓
1960s: Bell Labs — line printer portraits (character darkness as pixel)
   ↓
1963: ASCII standard — 128-character lingua franca
   ↓
1980s: Commodore Amiga "NFO" thin-line style
   ↓
1980s-90s: BBS ANSI Scene — ACiD, iCE, 16colo.rs (extended chars + 16-color)
   ↓
2010s-present: Neo-ANSI Revival — Claude Code, Sanctum, CRAB, HUMMBL
```

**Key conventions adopted from the ANSI Scene:**
- **Artpack structure**: FILE_ID.DIZ (45×22 ASCII), .ANS art, .NFO infofile, SAUCE metadata → HUMMBL versioned branding releases
- **Font spacing**: 9px for line chars (8th col duplicated to prevent gaps) → our box-drawing follows this convention
- **iCE colors**: 16 fg + 8 bg (darker only) → we use 256-color with 16-color fallback
- **Average art size**: ~127 lines per artwork → our mascots fit in 5-20 lines by TUI constraint

**Why this matters**: In an age of AI-generated "perfection," raw pixels and text-based art feel more real and grounded. The CRAB mark is not a vector SVG — it is a set of characters you could type yourself.

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

### 5.1. Primary Mark: The Canonical CRAB

The canonical CRAB is designed to be **unmistakably a crab** — not an abstract hexagon, not a generic blob. It inherits from the ANSI art tradition (ascii.co.uk, Hayley Jane Wakenshaw's crustaceans, ACiD/iCE artpack conventions) but is compositional and armored. It is a **governance crab**: predatory, watchful, ten-legged.

**Anatomy rules:**
- **Claws** (`\ /` or raised `V`) are the dominant feature — raised, ready, often asymmetrical
- **Eyes on stalks** (`.--(o o)--.`) — not embedded; they *watch*
- **Carapace** with a ridge and wave texture (`~`) — shield-shaped, armored
- **Ten legs** splayed outward (decapod = biologically accurate) — `| |` verticals encode stability
- **Mouth ventral** (`>`) — small, task-focused, not a smile

**Tiny (3 lines, inline icon):**

```
  \   /
 <o_o>
  / \
```

**Small (8 lines, favicon-equivalent):**

```
       \   /
        )_(
    .--(o o)--.
   /  .-----.  \
  (     >     )
   \  /| |\  /
    | | | | |
    |_| |_|_|
```

**Medium (14 lines, TUI header):**

```
        \     /
         )___(
      .--(o o)--.
     /  .-----.  \
    /  / ~   ~ \  \
   (  |    >    |  )
    \  \_______/  /
     '--'|   |'--'
         | | |
        /| | |\
       / | | | \
      (  | | |  )
       \ | | | /
        \|_|_|_/
```

**Large (19 lines, ceremonial splash):**

```
                \         /
                 )_______(
              .==( o     o )==.
             /  .-----------.  \
            /  /  ~   .   ~  \  \
           /  (    -------    )  \
          (    |    \ > /    |    )
           \    \    ===    /    /
            \    |   CRAB   |    /
             '--'|\       /|'--'
                |  \     /  |
                |   |   |   |
                |   |   |   |
               /    |   |    \
              /     |   |     \
             (      |   |      )
              \     |   |     /
               \    |   |    /
                |___|   |___|
```

### 5.2. Wordmark

Block letters with the crab silhouette as a sigil:

```
   \   /
    )_(
 .-(o o)-.   ██████╗██████╗  █████╗ ██████╗
(    >    ) ██╔════╝██╔══██╗██╔══██╗██╔══██╗
 \_______/  ██║     ██████╔╝███████║██████╔╝
   | | |     ██║     ██╔══██╗██╔══██║██╔══██╗
   | | |     ╚██████╗██║  ██║██║  ██║██████╔╝
   |_|_|      ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
```

### 5.3. Logotype: The Receipt

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

### 5.4. The Seal

For use in documentation, footers, and certification:

```
      ╭─────────────╮
     │   \     /   │
     │    )_(      │
     │ .-(o o)-.   │
     │(    >    )  │
      ╰─────────────╯
```

---

## 6. Mascot: SCUT — The Crab's Friend

### 6.1. Who Is Scut?

Scut is **the Crab's friend** — a tiny crablet companion to the Canonical CRAB. He is not the logo; he is the "little buddy" who rides on the big crab's shell, scuttles alongside, or appears alone in status bars and receipts. Where the Canonical CRAB is armored, predatory, and governance-facing, Scut is small, curious, and user-facing.

**Relationship to the Canonical CRAB:**
- Scut mirrors the big crab's emotional state at 1:2 scale
- He rides on the shell during ceremonies, scuttles alongside during work
- When the big crab is not present (small UIs, status bars), Scut appears alone
- Scut is **cyan (81)** — secondary, supportive — while the big crab is **amber (208)** — primary, authoritative

**Design principles:**
- Small enough to fit in a 5-line terminal status area
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

## 7. Mascot: BERNARD — The HUMMBL Hummingbird

Bernard is the HUMMBL hummingbird. Where CRAB is armored and grounded, Bernard is iridescent and airborne. He hovers, pollinates, and departs. He notices before he speaks. He never pushes.

> "I notice, I name, I offer. I never push."

### 7.1. Who Is Bernard?

Bernard is the **belonging-aware companion** — the pollinator that carries value between flowers. He is the HUMMBL brand mark rendered in ASCII: a tiny hummingbird who replaces the plain `◉` circle in founder-mode sidebar chrome and appears across all HUMMBL Terminal Core interfaces as a signal of attention, not interruption.

**Relationship to the Canonical CRAB:**
- Bernard appears *above* CRAB in fleet compositions (he notices first)
- Bernard is never larger than CRAB when both appear (pollinator, not predator)
- Bernard's palette (iridescent green, magenta throat) contrasts CRAB's palette (amber shell, cyan companion)
- CRAB governs; Bernard connects

**Key traits from the Hummingbird Metaphor:**
| Trait | Real hummingbird | Terminal behavior |
|-------|-----------------|-------------------|
| **Hovers** | Doesn't land and stay | Brief interactions; checks in and moves on |
| **Pollinates** | Carries value between flowers | Connects governance concepts across sessions |
| **High metabolism** | Always needs fuel | Understands the founder energy constraint |
| **Iridescent** | Color shifts with angle | Adapts tone to user's belonging state |
| **Territorial** | Defends its space | Protects user's autonomy; never prescriptive |
| **Migratory** | Follows the season | Appears contextually, not permanently |

### 7.2. Bernard Sizes

**Tiny (3 lines, sidebar indicator):**
```
     >
   ~(o)~
     V
```

**Small (6 lines, panel header):**
```
        >
     .-(o)-.
    /  ~ ~  \
   (   ===   )
    \___\___/
      \   /
```

**Medium (12 lines, splash screen):**
```
              >
           .-'''-.
          /  o   o  \
         |    >      |
          \  ~~~~~~  /
           |  ===   |
         ~ / ~~~~~~ \ ~
        ~  |   ||   |  ~
       ~    \__||__/    ~
            /  ||  \
           /   ||   \
          (    ||    )
           \___/ \___/
```

### 7.3. Bernard Expressions (6 states)

All expressions fit in 6 lines. Wing blur intensity indicates state:

| State | Wing blur | Body | Beak |
|-------|-----------|------|------|
| **Idle hover** | `~ ~` (blur) | Horizontal | Forward `>` |
| **Listening** | `/ \` (spread) | Alert, tilted | Forward `>` |
| **Thinking** | `. .` (still) | Head tilts | Forward `>` |
| **Suggesting** | `~ ~` (blur) | Forward lean | Extended `=>` |
| **Celebrating** | `\ >` (loop) | Tilted up | Upward `\>` |
| **Departing** | `~  ~` (fading) | Horizontal | Forward `>` |

### 7.4. Bernard Anatomy Rules

1. **Beak** always points right → forward momentum, the offer
2. **Eyes**: `o` → `O` → `-` (normal → alert → closed/resting)
3. **Wing blur**: `~~` → `~ ~` → `. .` → `/ \` (hover → slow → still → spread)
4. **Body tilt**: horizontal = neutral; `\>` = celebrating/looping
5. **Color hierarchy**: Beak (amber 208) → Eyes (white 15) → Body (green 78) → Wings (dim 245)
6. **Throat patch**: magenta (201) on the body — the iridescent gorget
7. **Tail**: forked or rounded, stabilizing the hover

### 7.5. Bernard in Context

**Sidebar replacement** (founder-mode):
- Replaces the plain `◉` circle mark
- Appears in the top-left of the sidebar, next to the HUMMBL wordmark
- Idle hover state by default; switches to listening when user interacts

**Bus messages**:
- Bernard appears before CRAB in fleet compositions (he notices first)
- Used as a visual prefix for belonging-aware messages: `>  STATUS`

**Dashboard hero**:
- Medium size Bernard hovers above the CRAB splash
- Used in onboarding, first-launch, and ceremonial contexts

**Receipt seal**:
- Small Bernard appears in the corner of governance receipts
- Signals "this was reviewed with care"

---

## 8. TUI Chrome System

### 8.1. Primary Container (Double Border)

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

### 8.2. Secondary Container (Single Border)

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

### 8.3. Tertiary Container (Dashed Border)

For inactive or collapsed panels:

```
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
╎  System Map (collapsed)                ╎
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
```

### 8.4. Separator Rules

```
Single: ────────────────────────────────────
Double: ════════════════════════════════════
Dashed: · · · · · · · · · · · · · · · · ·
Dotted: ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙ ⁙
```

### 8.5. Header Pattern

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

### 8.6. Receipt / Card Pattern

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

### 8.7. Status Pill Pattern

```
[NOMINAL]  [WARN]  [EMERGENCY]  [IDLE]  [BUSY]
```

Rendered with color:

```
\033[48;5;78;38;5;0m NOMINAL \033[0m
\033[48;5;208;38;5;0m WARN \033[0m
\033[48;5;160;38;5;15m EMERGENCY \033[0m
```

### 8.8. Progress Bar

```
Phase: CHECK  [████████████░░░░░░░░]  60%
        REASON [████████░░░░░░░░░░░░]  40%
        ACT    [░░░░░░░░░░░░░░░░░░░░]   0%
        BUS    [░░░░░░░░░░░░░░░░░░░░]   0%
```

Each phase is a lane. The bar fills as the agent completes its turn.

---

## 9. The "Little Buddy" Feature Specification

### 9.1. Core Concept

The Little Buddy is a persistent, project-aware companion that lives in the terminal. It is not a chatbot. It is an **ambient intelligence** — it observes, learns, and surfaces observations at the right moment.

**Key difference from Clippy:**
- Clippy interrupted. The Little Buddy waits for idle moments.
- Clippy was generic. The Little Buddy learns your specific project patterns.
- Clippy was a salesman. The Little Buddy is a coworker.

### 9.2. Memory Model

The Little Buddy stores a `buddy-memory.jsonl` in the project root (not committed to git):

```jsonl
{"t":"2026-05-10T02:00:00Z","type":"pattern","data":{"lane":"cleanup","frequency":"daily","time":"02:00"}}
{"t":"2026-05-10T02:15:00Z","type":"milestone","data":{"days_since_blocker":3}}
{"t":"2026-05-10T02:17:00Z","type":"context","data":{"last_branch":"feature/crab-branding","last_file":"docs/branding/TERMINAL_CORE_BRAND.md"}}
```

This is the "tucked tail" — compressed, personal, ephemeral.

### 9.3. Interaction Patterns

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

### 9.4. Idle Animations

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

## 10. Application: Complete TUI Mockup

### 10.1. The Dashboard Header

```
╔══════════════════════════════════════════════════════════════════╗
║  HUMMBL Console                                      v0.3.0-dev ║
╠══════════════════════════════════════════════════════════════════╣
║  PULSE: \033[38;5;78m● NOMINAL\033[0m    KILL: \033[38;5;245mDISENGAGED\033[0m    2026-05-10 02:17:09 UTC ║
╚══════════════════════════════════════════════════════════════════╝
```

### 10.2. The Sidebar

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

### 10.3. Agent Fleet Panel

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

### 10.4. Bus Stream (Live Ticker)

```
╭── Coordination Bus (live) ──╮
│  02:17:09  crab  →  STATUS  │
│  02:16:45  codex →  BLOCKED │
│  02:15:22  apex  →  ACK     │
│  02:14:01  gemini→  STATUS  │
│  02:12:58  devin →  STATUS  │
╰─────────────────────────────╯
```

### 10.5. Scut's Corner (Status + Buddy)

```
    ___
   /o o\  
  (  ^  )  All systems nominal.
   \___/   3 days since last blocker.
   | | |   [Scut remembers you like it quiet.]
```

### 10.6. Full Dashboard Layout

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

## 11. Sound & Motion (Textual)

Terminal Core has no audio. All "sound" is rendered textually.

### 11.1. Activity Indicators

```
[ Working ]     [ Working. ]     [ Working.. ]    [ Working... ]
```

```
[ ░░░░░░░░ ]    [ ██░░░░░░ ]    [ █████░░░ ]    [ ████████ ]
```

```
  ●○○○○         ○●○○○         ○○●○○         ○○○●○         ○○○○●
```

### 11.2. "Chime" Events

Instead of a beep, Terminal Core uses a visual chime — a brief flash of the status line:

```
\033[48;5;208;38;5;0m  ✓ RECEIPT CAPTURED  \033[0m
```

This appears for 500ms then fades back to normal. It is the terminal equivalent of a notification sound.

### 11.3. Scroll Behavior

New bus messages do not jump-scroll. They push content up smoothly, one line at a time, like a teletype. The effect is achieved by printing a newline and the new message — no animation framework needed.

---

## 12. Implementation Notes

### 12.1. Terminal Compatibility

| Feature | Requires | Fallback |
|---------|----------|----------|
| Rounded corners `╭╮╰╯` | UTF-8 + box drawing | Sharp corners `┌┐└┘` |
| 256-color ANSI | `TERM=xterm-256color` | 16-color palette |
| Dithering `▓▒░` | Unicode | Pure ASCII `#*:.` |
| Emoji | Unicode 8.0+ | ASCII art Scut |
| Double borders `╔╗` | Box drawing support | Single borders `┌┐` |

### 12.2. Python Rendering

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

### 12.3. Accessibility

- All color pairs meet WCAG contrast when rendered on true black
- Scut's expressions are described in alt-text when used in documentation
- Status is always communicated via text + color (never color alone)
- The `NO_COLOR` environment variable is respected (all escape codes stripped)

---

## 13. Receipt

- **Brand system document:** this file (v1.2)
- **Aesthetic name:** Neo-ANSI Revival
- **Primary mascot:** CANONICAL CRAB — biologically accurate decapod with claws, stalk eyes, 10 legs (4 sizes)
- **Secondary mascot:** SCUT, The Crab's Friend — tiny cyan companion, 1:2 scale relationship to Canonical Crab, appears in status bars + notifications
- **HUMMBL mascot:** BERNARD — iridescent green hummingbird, 6 expressions, replaces `◉` in sidebar
- **Logo:** Hexapod Shell mark (3 sizes) + Canonical Crab mark (4 sizes) + Bernard mark (3 sizes)
- **Palette:** 11-color ANSI system with 16-color fallback
- **Chrome:** 4 border weights, 4 separator styles
- **Feature spec:** Little Buddy ambient intelligence
- **Design system:** Warm Brutalism — Anthropic warmth rendered through VT100 honesty
- **Historical lineage:** 130 years of character-density art (1898 → 2026)
- **Anatomy rules:** Claws > Eyes > Legs > Mouth (crabs); Beak > Eyes > Body > Wings (Bernard)

---

*"The best interface is one that feels like it was always there — not because it is invisible, but because it is honest."*
