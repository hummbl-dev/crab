# HUMMBL Terminal Core — Unified Design System

**Status:** Draft v1.0 | **Date:** 2026-05-10  
**Scope:** Cross-brand design system for CRAB (governance protocol) and HUMMBL (belonging platform)  
**Source:** `TERMINAL_CORE_BRAND.md` (aesthetic foundation) + `CANONICAL_ART_TOOLKIT.md` (composable elements)  
**Aesthetic:** Neo-ANSI Revival | Warm Brutalism

---

## 1. Design System Architecture

### 1.1. The Three-Layer Model

```
┌─────────────────────────────────────────┐
│  LAYER 3: APPLICATION                   │
│  Dashboards, TUIs, CLI output, web    │
│  → Uses tokens, components, mascots     │
├─────────────────────────────────────────┤
│  LAYER 2: COMPONENTS                      │
│  Mascots, chrome, containers, patterns  │
│  → Composed from toolkit elements       │
├─────────────────────────────────────────┤
│  LAYER 1: TOKENS                          │
│  Colors, spacing, typography, animation   │
│  → The shared vocabulary                  │
└─────────────────────────────────────────┘
```

### 1.2. Brand Relationship: CRAB + HUMMBL

```
                    HUMMBL
               (belonging platform)
                      │
         ┌────────────┼────────────┐
         │            │            │
      CRAB       Bernard      Open Brain
   (protocol)   (mascot)     (cognition)
         │            │            │
         └────────────┴────────────┘
                      │
               Terminal Core
               (shared aesthetic)
```

**Rule:** CRAB and HUMMBL share Terminal Core but serve different emotional registers:
- **CRAB** = armored, vigilant, governance-facing. Amber shell. Decides.
- **HUMMBL** = iridescent, connecting, belonging-facing. Green body + magenta throat. Notices.
- **Scut** = companion, user-facing, cyan. Bridges the two.

### 1.3. The Fleet Principle

When multiple mascots appear together, they form a **fleet** with explicit hierarchy:

```
Bernard (notices first, airborne)
   ↓
CRAB (governs, grounded)
   ↓
Scut (companion, bridges)
```

**Fleet rules:**
1. Bernard never appears below CRAB (he notices first)
2. Scut never appears above Bernard (he's the bridge, not the scout)
3. When space is constrained, mascots appear solo — never cramped
4. Fleet compositions use the 16-line compact variant (see section 6.3)

---

## 2. Design Tokens

### 2.1. Color Tokens

All colors use ANSI 256-color escape sequences with mandatory 16-color fallback.

| Token | 256-Color | 16-Color Fallback | Hex Approx | Usage |
|-------|-----------|-------------------|------------|-------|
| `--tc-amber` | `\033[38;5;208m` | `\033[38;5;3m` | `#FF8700` | CRAB shell, authority, beak |
| `--tc-amber-light` | `\033[38;5;220m` | `\033[38;5;11m` | `#FFD700` | Highlights, hover states |
| `--tc-cyan` | `\033[38;5;81m` | `\033[38;5;6m` | `#5FD7FF` | Scut body, secondary accent |
| `--tc-cyan-deep` | `\033[38;5;37m` | `\033[38;5;6m` | `#00AFAF` | Deep water, shadow |
| `--tc-green` | `\033[38;5;78m` | `\033[38;5;2m` | `#5FD75F` | Bernard body, success |
| `--tc-magenta` | `\033[38;5;201m` | `\033[38;5;5m` | `#FF5FFF` | Bernard throat, accent |
| `--tc-red-soft` | `\033[38;5;160m` | `\033[38;5;1m` | `#D70000` | Error, halt |
| `--tc-dim` | `\033[38;5;245m` | `\033[38;5;7m` | `#8A8A8A` | Legs, wings, metadata |
| `--tc-white` | `\033[38;5;15m` | `\033[38;5;7m` | `#FFFFFF` | Eyes, primary text |
| `--tc-black` | `\033[40m` | `\033[40m` | `#000000` | Background |
| `--tc-reset` | `\033[0m` | `\033[0m` | — | Reset all attributes |

**Color blindness considerations:**
- Deuteranopia (red-green): Amber (208) and cyan (81) remain distinguishable
- Protanopia: Green (78) and amber (208) may blur — use size/texture as secondary signal
- Achromatopsia: Rely on character darkness (crab shell uses `)` `(` which are darker than `~` ` `)

### 2.2. Spacing Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--space-xs` | 1 line | Tight grouping, status inline |
| `--space-sm` | 2 lines | Panel internal padding |
| `--space-md` | 4 lines | Section separation |
| `--space-lg` | 8 lines | Major section break |
| `--space-xl` | 12 lines | Splash screen breathing room |
| `--gutter` | 4 spaces | Left margin indent |
| `--col-width` | 80 chars | Maximum terminal width |
| `--col-narrow` | 45 chars | FILE_ID.DIZ width |
| `--col-wide` | 132 chars | Wide terminal (optional) |

### 2.3. Typography Tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--font-mono` | System monospace | All text, all contexts |
| `--font-serif` | ASCII art serif | Wordmarks only (decorative) |
| `--size-body` | 1 line | Standard text |
| `--size-heading` | 2 lines | Sub-headings (with underline) |
| `--size-hero` | 5-8 lines | Major headings (block letters) |
| `--line-height` | 1.0 | No extra spacing between lines |
| `--tracking` | 0 | Natural monospace spacing |

### 2.4. Animation Tokens

All "animation" in Terminal Core is character-substitution, not frame animation.

| Token | Pattern | Duration (manual) |
|-------|---------|-----------------|
| `--anim-flutter` | `~` → `~ ~` → `~~` → `~ ~` | 200ms per substitution |
| `--anim-tap` | `|` → `>` → `|` → `<` | 300ms per substitution |
| `--anim-pulse` | `o` → `O` → `o` | 500ms per substitution |
| `--anim-fade` | Full color → dim (245) → invisible | 1s per step |
| `--anim-appear` | Reverse of fade | 200ms per step |

**Constraint:** Animations must respect `prefers-reduced-motion`. If enabled, show static final state only.

---

## 3. Mascot System

### 3.1. Mascot Decision Tree

```
Is the user interacting with governance? (bus, receipts, protocols)
  → YES → Use CRAB
    → Is there a status companion? → Add Scut (cyan)
    → Is there a belonging signal? → Add Bernard (green) above

Is the user interacting with belonging? (sidebar, onboarding, chat)
  → YES → Use Bernard
    → Is there governance context? → Add CRAB below

Is space constrained (< 8 lines)?
  → YES → Use Tiny variant (3 lines)
    → CRAB: tiny crab mark
    → Bernard: tiny hummingbird mark
    → Scut: 5-line fixed (always small)
```

### 3.2. Expression Selection Matrix

| Context | CRAB Expression | Scut Expression | Bernard Expression |
|---------|----------------|---------------|-------------------|
| Idle/standby | Medium, neutral | IDLE | IDLE HOVER |
| User active | — | — | LISTENING |
| Processing | Medium, working | WORKING | THINKING |
| Error | Medium, alert | ERROR | — |
| Success | Large, neutral | SUCCESS | CELEBRATING |
| Warning | — | BLOCKED | — |
| Welcome | Large, neutral | WELCOME | SUGGESTING |
| Goodbye | — | WAVING | DEPARTING |
| Maintenance | — | MAINTENANCE | — |

### 3.3. Fleet Compositions

**Composition A: Full Fleet (20 lines, ceremonial)**
```
Bernard (12 lines, medium)
  ↓ 4 lines spacing
CRAB (19 lines, large)  [Note: this is 35 lines total — too tall]
```

**Composition B: Compact Fleet (16 lines, dashboard hero)**
```
Bernard small (6 lines)
  ↓ 2 lines spacing
CRAB small (8 lines)
  ↓ 0 lines overlap
Scut rides on CRAB shell
```

**Composition C: Sidebar Pair (8 lines, tight)**
```
Bernard tiny (3 lines)
  ↓ 1 line spacing
CRAB tiny (3 lines) + Scut (5 lines, offset)
```

**Composition D: Status Only (5 lines, minimal)**
```
Scut only (5 lines, expression varies)
```

---

## 4. TUI Component System

### 4.1. Container Hierarchy

```
PRIMARY CONTAINER    — Double border ═║  (most important content)
  ├─ SECONDARY       — Single border ─│  (sub-panels)
  │   └─ TERTIARY    — Dashed border ┄┆  (metadata, help text)
  └─ HEADER          — Top rule + title  (section labels)
```

**Spacing rule:** Containers nest at `--space-sm` (2 lines) minimum padding.

### 4.2. Status Patterns

**Status Pill:** `[ STATUS ]` with color-coded brackets
- OK: `\033[38;5;78m[ OK ]\033[0m`
- WARN: `\033[38;5;208m[ WARN ]\033[0m`
- ERROR: `\033[38;5;160m[ ERROR ]\033[0m`
- IDLE: `\033[38;5;245m[ IDLE ]\033[0m`

**Progress Bar:** `[████░░░░░░] 40%`
- Fill: `\033[38;5;208m█\033[0m`
- Empty: `\033[38;5;245m░\033[0m`
- Label: `\033[38;5;15m\033[0m`

**Activity Indicator:** `⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏` (braille spinner) or `~` `*` `·` for minimal

### 4.3. Receipt / Card Pattern

All receipts use the same horizontal format:

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

**Receipt rules:**
1. Timestamp in UTC, ISO 8601 format
2. FROM field uses canonical agent identity (bare name, no parentheticals)
3. TYPE field uses bus message types: PROPOSAL, ACK, STATUS, BLOCKED, DECISION
4. Horizontal rule separates metadata from message
5. Scut may appear in the corner as a seal

---

## 5. Cross-Platform Rendering

### 5.1. Terminal Matrix

| Platform | ANSI Support | Unicode Box-Draw | Notes |
|----------|-------------|-------------------|-------|
| iTerm2 (macOS) | 256-color | Yes | Full support, true black |
| Windows Terminal | 256-color | Yes | Best on Windows |
| VS Code terminal | 256-color | Yes | May need font config |
| Git Bash (MSYS) | 16-color fallback | Partial | `\` may escape |
| PuTTY | 16-color | Partial | Use 16-color mode |
| Linux TTY | 16-color | No | Use ASCII alternatives |
| Docker/Alpine | 256-color | Yes | Full support |

### 5.2. Windows-Specific Guidelines

**Backslash handling:**
- The `\` character in ASCII art may be interpreted as escape in PowerShell
- **Workaround:** Use `type filename.txt` in CMD, or `cat` in Git Bash
- **Code workaround:** When embedding in Python strings, use raw strings (`r"..."`) or byte literals

**Encoding:**
- Files must be UTF-8 with LF line endings
- BOM should not be present
- `chcp 65001` sets UTF-8 in Windows CMD

### 5.3. Web Rendering

For dashboard/web contexts:
- Wrap art in `<pre class="terminal-art">` with `white-space: pre`
- Use CSS classes for color (e.g., `.tc-amber { color: #FF8700; }`)
- Strip ANSI codes server-side: `re.sub(r'\033\[[0-9;]*m', '', text)`
- Respect `prefers-reduced-motion` for animated states

### 5.4. `NO_COLOR` Support

All rendering code must check for `NO_COLOR` environment variable:

```python
import os

def render_art(text):
    if os.environ.get('NO_COLOR'):
        return strip_ansi(text)
    return text
```

---

## 6. Accessibility

### 6.1. Color Blindness Matrix

| Pair | Deuteranopia | Protanopia | Achromatopsia | Mitigation |
|------|-------------|------------|---------------|------------|
| Amber/Cyan | ✓ Distinguishable | ✓ Distinguishable | ✗ Use darkness diff | Shell darker than legs |
| Green/Magenta | ✓ Distinguishable | ⚠ May blur | ✗ Use texture diff | Wing blur vs solid body |
| White/Dim | ✓ Distinguishable | ✓ Distinguishable | ✗ Use contrast | Eyes always brightest |
| CRAB/Bernard | ✓ Distinguishable | ⚠ May blur | ✗ Use shape | Claws vs beak distinct |

### 6.2. Reduced Motion

When `prefers-reduced-motion` is enabled:
- Show static expressions (no flutter/tap/pulse animation)
- Use "Idle" state as the canonical static representation
- Replace braille spinner with static `...` or `—`

### 6.3. Screen Readers

For non-visual contexts:
- Mascots should have `aria-label` describing state: "Scut is working"
- ASCII art should be hidden from screen readers: `aria-hidden="true"`
- Text content must be fully described without relying on visual art

---

## 7. Versioning & Artpack Standards

### 7.1. Artpack Structure

For tagged releases, follow ANSI Scene conventions:

```
hummbl-terminal-core-v1.2.0/
  ├── FILE_ID.DIZ      (45×22 ASCII — see template below)
  ├── CRAB.ANS         (Canonical CRAB with SAUCE metadata)
  ├── BERNARD.ANS      (Bernard with SAUCE metadata)
  ├── SCUT.ANS         (Scut expressions with SAUCE metadata)
  ├── BRAND.NFO        (This design system, plain text)
  ├── TOOLKIT.NFO      (Canonical art toolkit, plain text)
  └── SAUCE/           (Metadata records)
```

### 7.2. FILE_ID.DIZ Template

```
Terminal Core v1.2 Neo-ANSI Revival
CRAB: armored decapod. Bernard:
iridescent hummingbird. Scut: cyan
companion. Warm Brutalism for agent
governance. HUMMBL Research Institute.
(c) 2026 hummbl.io
```

**Rules:** 45 columns × 22 lines maximum. Plain ASCII. No ANSI codes.

### 7.3. SAUCE Metadata

```
SAUCE00
Title:    Canonical CRAB
Author:   Devin / HUMMBL
Group:    HUMMBL Research Institute
Date:     20260510
FileSize: [bytes]
DataType: 1 (Character)
FileType: 1 (ASCII)
TInfo1:   80 (terminal width)
TInfo2:   25 (terminal height)
Comments: 0
TFlags:   00000000
```

### 7.4. Versioning Rules

- **Major (X.0.0):** New mascot, breaking palette changes, renamed tokens
- **Minor (x.Y.0):** New expressions, new sizes, new components
- **Patch (x.y.Z):** Bug fixes, color corrections, documentation updates

---

## 8. Usage Decision Tree

### 8.1. "What Mascot Should I Use?"

```
Is this a governance message? (bus, receipt, protocol status)
  ├─ YES → CRAB
  │       ├─ Tiny: inline status, tmux segment
  │       ├─ Small: panel header, favicon
  │       ├─ Medium: dashboard panel, bus card
  │       └─ Large: splash screen, release notes
  │
  └─ NO → Is this a belonging interaction? (sidebar, onboarding, chat)
          ├─ YES → Bernard
          │       ├─ Tiny: sidebar indicator, inline
          │       ├─ Small: panel header, seal
          │       └─ Medium: splash screen, hero
          │
          └─ NO → Is this a companion moment? (idle, ambient, nudge)
                  ├─ YES → Scut
                  │       └─ Always 5-line, expression varies
                  │
                  └─ NO → Use abstract mark (hexapod shell)
```

### 8.2. "What Expression Should I Use?"

```
Is there user action required?
  ├─ YES → SUGGESTING (Bernard) / WORKING (Scut)
  ├─ NO → Is there an error?
  │       ├─ YES → ERROR (Scut) / alert eyes (CRAB)
  │       └─ NO → Is there a success?
  │               ├─ YES → SUCCESS (Scut) / CELEBRATING (Bernard)
  │               └─ NO → Is the system busy?
  │                       ├─ YES → BUSY (Scut) / THINKING (Bernard)
  │                       └─ NO → IDLE (all)
```

### 8.3. "What Size Should I Use?"

| Available Lines | Mascot | Size |
|----------------|--------|------|
| 1-3 | Any | Tiny |
| 4-8 | CRAB | Small |
| 4-8 | Bernard | Small |
| 4-8 | Scut | Full (5L) |
| 9-14 | CRAB | Medium |
| 9-14 | Bernard | Medium |
| 15-20 | CRAB | Large |
| 15-20 | Bernard | Medium (leave room for chrome) |
| 21+ | Fleet | Full composition |

---

## 9. Quality Checklist

Before any Terminal Core art ships:

- [ ] All ANSI codes are syntactically valid (`\033[38;5;Nm` or `\033[0m`)
- [ ] No `NO_COLOR` environment variable bypasses code
- [ ] 16-color fallback works (test with `TERM=vt100`)
- [ ] No line exceeds 80 columns
- [ ] No literal `\n` backslash-n sequences in art
- [ ] Reset (`\033[0m`) appears at end of each colored block
- [ ] Expression is distinguishable from others in the set
- [ ] Anatomy rules are followed (crab: claws > eyes > legs; bird: beak > eyes > body)
- [ ] Mascot is appropriate for the governance/belonging context
- [ ] Art renders correctly with `cat` on Unix and `type` on Windows

---

## 10. Receipt

- **Design system document:** this file (v1.0)
- **Brand foundation:** `TERMINAL_CORE_BRAND.md` (v1.2)
- **Composable toolkit:** `CANONICAL_ART_TOOLKIT.md`
- **Mascots:** CRAB (4 sizes), Bernard (3 sizes, 6 expressions), Scut (14 expressions)
- **Color system:** 11-token ANSI palette with 16-color fallback
- **Spacing system:** 6 tokens (XS to XL) + gutter + column widths
- **Animation system:** 5 substitution patterns with reduced-motion support
- **Accessibility:** Color-blind matrix, screen reader guidelines, `NO_COLOR` support
- **Versioning:** SemVer for artpacks, SAUCE metadata spec
- **Platforms:** Unix terminals, Windows Terminal, web, Docker
- **Next gate:** Implement dashboard TUI with fleet composition + test on all platforms

---

*"The best interface is one that feels like it was always there — not because it is invisible, but because it is honest."*
