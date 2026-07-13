# Canonical Art Toolkit
## Composable ASCII/ANSI Elements for Terminal Core

**Status:** Draft v1.0 | **Date:** 2026-05-10  
**Source:** `HUMMBL_TERMINAL_CORE_DESIGN_SYSTEM.md` (token spec)  
**Purpose:** Reusable building blocks for creating new Terminal Core art

---

## 1. Mascot Part Library

### 1.1. CRAB Anatomy Parts

All CRAB expressions are built from these parts. Combine to create new states.

**Claws (choose one):**
```
A:  \   /       (neutral, symmetrical)
B:  \     /     (wide, alert)
C:  >   <       (working, tapping)
D:  \   /  \o/   (celebrating, one claw up)
```

**Eyes (choose one):**
```
a:  (o o)        (normal)
b:  (O O)        (alert)
c:  (- -)        (sleepy)
d:  (. o)        (thinking, one eye half-closed)
e:  (o_o)        (focused)
```

**Mouth (choose one):**
```
1:  (  >  )      (neutral, task focus)
2:  (  ^  )      (happy)
3:  (  o  )      (shock)
4:  (  -  )      (sleepy)
```

**Carapace (size-appropriate):**
```
Small:   /  .-----.  \
Medium:  /  / ~   ~ \  \
Large:   /  /  ~   .   ~  \  \
```

**Legs (choose one):**
```
I:   | | | | |     (neutral, vertical)
II:  /| | |\       (splayed, calm)
III: > | <          (working, claws tapping)
IV:  \ | /          (celebrating, spread)
```

**Assembly: Small CRAB = Claws-A + Eyes-a + Mouth-1 + Carapace-Small + Legs-II**

### 1.2. Bernard Anatomy Parts

**Beak (choose one):**
```
A:  >              (neutral, forward)
B:  =>             (suggesting, extended)
C:  \>             (celebrating, loop)
```

**Eyes (choose one):**
```
a:  (o o)          (normal)
b:  (O O)          (alert)
c:  (- -)          (sleepy/resting)
```

**Body (choose one):**
```
1:  (   ===   )    (neutral, horizontal)
2:  (  ===  )      (small, compact)
3:  |  ===   |      (medium, with wing attachment points)
```

**Wing Blur (choose one):**
```
I:   ~ ~            (hovering, fast blur)
II:  . .            (thinking, slow)
III: / \            (listening, spread)
IV:  ~  ~           (departing, fading)
```

**Tail (choose one):**
```
A:  \___/ \___/     (forked, medium)
B:  \   /           (small, rounded)
C:  V               (tiny, minimal)
```

**Assembly: Small Bernard = Beak-A + Eyes-a + Body-2 + Wing-I + Tail-B**

### 1.3. Scut Anatomy Parts

Scut is a 1:2 scale CRAB. Use CRAB parts but halve all dimensions.

```
Head:    ___
Eyes:    /o o\  or /O O\  or /- -\
Mouth:   (  >  )  or (  ^  )  or (  o  )
Body:    \___/
Legs:    | | |  or > | <  or \ | /
```

---

## 2. Box Drawing Reference

### 2.1. Border Characters

```
Light:  ┌ ┐ └ ┘ │ ─  (thin, secondary)
Heavy:  ╔ ╗ ╚ ╝ ║ ═  (thick, primary)
Double: ╭ ╮ ╰ ╯ │ ─  (rounded, tertiary)
Dashed: ┄ ┆ ┈ ┊  (metadata, help)
```

### 2.2. Separator Characters

```
Horizontal:  ───  ═══  ━━━  ░░░  ▒▒▒  ▓▓▓
Vertical:    │    ║    ┃    ░    ▒    ▓
Corner:      ├    ╠    ┣    ╞    ╡
```

### 2.3. Texture Characters

```
Light:   ░  (25% density)
Medium:  ▒  (50% density)
Heavy:   ▓  (75% density)
Solid:   █  (100% density)
```

### 2.4. Spacing Characters

```
Hair:      (space)
Thin:      ·  (middle dot)
Medium:    ~  (tilde, for hover)
Wide:      —  (em dash)
```

---

## 3. Color Swatches

### 3.1. ANSI 256-Color Swatches

Render these lines to see exact colors on your terminal:

```
\033[38;5;208m██ AMBER (208)      \033[38;5;220m██ AMBER-LIGHT (220)
\033[38;5;81m██ CYAN (81)        \033[38;5;37m██ CYAN-DEEP (37)
\033[38;5;78m██ GREEN (78)       \033[38;5;201m██ MAGENTA (201)
\033[38;5;160m██ RED-SOFT (160)   \033[38;5;245m██ DIM (245)
\033[38;5;15m██ WHITE (15)        \033[40m  \033[38;5;15m██ BLACK (bg)\033[0m
```

### 3.2. 16-Color Fallback Swatches

```
\033[38;5;3m██ AMBER (3)         \033[38;5;11m██ AMBER-LIGHT (11)
\033[38;5;6m██ CYAN (6)          \033[38;5;6m██ CYAN-DEEP (6)
\033[38;5;2m██ GREEN (2)         \033[38;5;5m██ MAGENTA (5)
\033[38;5;1m██ RED-SOFT (1)      \033[38;5;7m██ DIM (7)
\033[38;5;7m██ WHITE (7)         \033[40m  \033[38;5;7m██ BLACK (bg)\033[0m
```

### 3.3. Background Combinations

```
\033[48;5;208;38;5;0m  AMBER on BLACK   \033[0m   \033[48;5;0;38;5;208m  BLACK on AMBER   \033[0m
\033[48;5;81;38;5;0m  CYAN on BLACK    \033[0m   \033[48;5;0;38;5;81m  BLACK on CYAN    \033[0m
\033[48;5;78;38;5;0m  GREEN on BLACK   \033[0m   \033[48;5;0;38;5;78m  BLACK on GREEN   \033[0m
\033[48;5;201;38;5;0m  MAGENTA on BLACK \033[0m   \033[48;5;0;38;5;201m  BLACK on MAGENTA \033[0m
```

---

## 4. Layout Templates

### 4.1. Dashboard Panel (60×14 lines)

```
╔══════════════════════════════════════════════════════════════╗
║  \033[38;5;208mCRAB\033[0m  v1.2.0                                  [ OK ]  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║   \033[38;5;78m     >\033[0m                      \033[38;5;208m       \   /\033[0m          ║
║   \033[38;5;78m   ~(o)~\033[0m                    \033[38;5;208m        )_(\033[0m          ║
║   \033[38;5;78m     V\033[0m                      \033[38;5;208m    .--(o o)--.\033[0m      ║
║                                \033[38;5;208m   /  .-----.  \\\033[0m     ║
║                                \033[38;5;208m  (     >     )\033[0m      ║
║                                \033[38;5;245m   \  /| |\  /\033[0m       ║
║                                \033[38;5;245m    | | | | |\033[0m        ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Bus: 3 messages  │  Agents: 5 live  │  Health: NOMINAL     ║
╚══════════════════════════════════════════════════════════════╝
```

### 4.2. Sidebar Header (24×8 lines)

```
┌────────────────────────┐
│  \033[38;5;78m>\033[0m  HUMMBL             │
│  \033[38;5;78m~o~\033[0m                   │
│  \033[38;5;78mV\033[0m    Governance       │
├────────────────────────┤
│  Dashboard             │
│  Fleet                 │
│  Bus                   │
│  Settings              │
└────────────────────────┘
```

### 4.3. Receipt Card (40×10 lines)

```
┌──────────────────────────────────────┐
│  2026-05-10 02:17:09 UTC             │
│  FROM: crab-daemon                   │
│  TYPE: STATUS                        │
│  MSG:  NOMINAL                       │
│                                      │
│  \033[38;5;81m    ___\033[0m                            │
│  \033[38;5;81m   /o o\                            │
│  \033[38;5;81m  (  >  )\033[0m  Verified.             │
│  \033[38;5;81m   \___/\033[0m                            │
└──────────────────────────────────────┘
```

### 4.4. Status Bar (80×1 line)

```
\033[38;5;245m[\033[38;5;78m✓\033[38;5;245m] Bus OK  │  [\033[38;5;208m!\033[38;5;245m] 2 alerts  │  \033[38;5;81m>\033[38;5;245m Bernard  │  \033[38;5;208m\ /\033[38;5;245m CRAB  │  14:32 UTC\033[0m
```

### 4.5. Splash Screen (80×24 lines)

```
\033[40m\033[38;5;245m
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│   \033[38;5;78m              >\033[38;5;245m                                                            │
│   \033[38;5;78m           .-'''-.\033[38;5;245m                                                        │
│   \033[38;5;78m          /  o   o  \\\033[38;5;245m                                                       │
│   \033[38;5;78m         |    >      |\033[38;5;245m                                                      │
│   \033[38;5;78m          \  ~~~~~~  /\033[38;5;245m                                                       │
│   \033[38;5;78m           |  ===   |\033[38;5;245m                                                       │
│   \033[38;5;245m         ~ / ~~~~~~ \ ~\033[38;5;245m                                                      │
│   \033[38;5;245m        ~  |   ||   |  ~\033[38;5;245m                                                     │
│   \033[38;5;245m       ~    \__||__/    ~\033[38;5;245m                                                    │
│                                                                              │
│   \033[38;5;208m                \         /\033[38;5;245m                                                   │
│   \033[38;5;208m                 )_______(\033[38;5;245m                                                  │
│   \033[38;5;208m              .==( o     o )==.\033[38;5;245m                                               │
│   \033[38;5;208m             /  .-----------.  \\\033[38;5;245m                                             │
│   \033[38;5;208m            /  /  ~   .   ~  \  \\\033[38;5;245m                                            │
│   \033[38;5;208m           /  (    -------    )  \\\033[38;5;245m                                           │
│   \033[38;5;208m          (    |    \ > /    |    )\033[38;5;245m                                          │
│   \033[38;5;208m           \    \    ===    /    /\033[38;5;245m                                           │
│                                                                              │
│   \033[38;5;15m   HUMMBL Terminal Core — v1.2.0\033[38;5;245m                                             │
│   \033[38;5;245m   Neo-ANSI Revival · Warm Brutalism · Agent-Native\033[38;5;245m                        │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
\033[0m
```

---

## 5. Expression Builder

### 5.1. CRAB Expression Builder

To build a new CRAB expression:

1. **Choose size** (tiny/small/medium/large)
2. **Choose claw state** (A-D)
3. **Choose eye state** (a-e)
4. **Choose mouth state** (1-4)
5. **Choose leg state** (I-IV)
6. **Assemble from parts**
7. **Apply color:** amber (208) shell, white (15) eyes, dim (245) legs
8. **Add reset** at end

**Example: "CRAB — Surprised"**
```
Claws:  A (\   /)
Eyes:   b (O O)
Mouth:  3 (o)
Legs:   I (| | | | |)

Result:
\033[38;5;208m       \   /
\033[38;5;208m        )_(
\033[38;5;208m    .--(\033[38;5;15mO O\033[38;5;208m)--.
\033[38;5;208m   /  .-----.  \\\033[38;5;208m  (     \033[38;5;15mo\033[38;5;208m     )
\033[38;5;208m   \  /\033[38;5;245m| |\033[38;5;208m\  /
\033[38;5;245m    | | | | |
\033[38;5;245m    |_| |_|_|\033[0m
```

### 5.2. Bernard Expression Builder

To build a new Bernard expression:

1. **Choose size** (tiny/small/medium)
2. **Choose beak** (A-C)
3. **Choose eyes** (a-c)
4. **Choose wing blur** (I-IV)
5. **Choose body tilt** (horizontal/tilted)
6. **Apply color:** green (78) body, magenta (201) throat, amber (208) beak
7. **Add reset** at end

**Example: "Bernard — Startled"**
```
Beak:    A (>)
Eyes:    b (O O)
Wings:   III (/ \)
Body:    tilted back

Result:
\033[38;5;208m        >\033[0m
\033[38;5;78m   /\-(\033[38;5;15mO\033[38;5;78m)-/\\\033[0m
\033[38;5;78m  /  \033[38;5;245m~   ~\033[38;5;78m  \\\033[0m
\033[38;5;78m (   \033[38;5;201m=====\033[38;5;78m   )\033[0m
\033[38;5;78m  \\___\\___/\033[0m
\033[38;5;78m    \\   /\033[0m
```

### 5.3. Scut Expression Builder

Scut uses the same grammar as CRAB but at 1:2 scale. All Scut expressions are 5 lines.

**Example: "Scut — Curious"**
```
Eyes:   d (. o)
Mouth:  >
Claws:  neutral

Result:
\033[38;5;81m    ___
\033[38;5;81m   /\033[38;5;15m. o\033[38;5;81m\
\033[38;5;81m  (  \033[38;5;15m>\033[38;5;81m  )  ?
\033[38;5;81m   \___/
\033[38;5;81m   | | |\033[0m
```

---

## 6. Animation Patterns

### 6.1. Wing Flutter (Bernard)

```
Frame 1:  ~ ~     (hover)
Frame 2:  ~~      (upstroke)
Frame 3:  ~ ~     (hover)
Frame 4:  ~~      (downstroke)
```

**Code pattern:**
```python
frames = ["~ ~", "~~", "~ ~", "~~"]
for frame in frames:
    print(f"\033[38;5;78m    /  \033[38;5;245m{frame}\033[38;5;78m  \\\033[0m")
    time.sleep(0.2)
```

### 6.2. Claw Tap (Scut)

```
Frame 1:  | | |
Frame 2:  > | <
Frame 3:  | | |
Frame 4:  < | >
```

**Code pattern:**
```python
frames = ["| | |", "> | <", "| | |", "< | >"]
for frame in frames:
    print(f"\033[38;5;81m   {frame}\033[0m")
    time.sleep(0.3)
```

### 6.3. Eye Pulse (CRAB)

```
Frame 1:  o o     (normal)
Frame 2:  O O     (alert)
Frame 3:  o o     (normal)
```

**Code pattern:**
```python
frames = ["o o", "O O", "o o"]
for frame in frames:
    print(f"\033[38;5;208m    .--(\033[38;5;15m{frame}\033[38;5;208m)--.\033[0m")
    time.sleep(0.5)
```

### 6.4. Progress Fill

```
Frame 1:  [░░░░░░░░░░]  0%
Frame 2:  [██░░░░░░░░] 20%
Frame 3:  [████░░░░░░] 40%
Frame 4:  [██████░░░░] 60%
Frame 5:  [████████░░] 80%
Frame 6:  [██████████] 100%
```

**Code pattern:**
```python
for i in range(0, 11, 2):
    fill = "█" * i + "░" * (10 - i)
    pct = i * 10
    print(f"\033[38;5;245m[{\033[38;5;208m{fill}\033[38;5;245m}] {pct}%\033[0m")
    time.sleep(0.5)
```

---

## 7. FILE_ID.DIZ Template

For artpack releases, create a 45×22 ASCII file:

```
123456789012345678901234567890123456789012345
--------------------------------------------
|                                          |
|     \   /                                |
|      )_(     Terminal Core v1.2          |
|  .--(o o)--.  Neo-ANSI Revival           |
| (    >    )  HUMMBL Research             |
|  \_______/   Institute                   |
|    | | |                                 |
|                                          |
|  CRAB: armored decapod                   |
|  BERNARD: iridescent hummingbird         |
|  SCUT: cyan companion                    |
|                                          |
|  Warm Brutalism for agent governance     |
|                                          |
|  https://hummbl.io                       |
|  (c) 2026 HUMMBL Research Institute      |
|                                          |
--------------------------------------------
```

**Rules:**
- Exactly 45 columns wide
- Maximum 22 lines
- Plain ASCII only (no ANSI, no Unicode)
- Must include version number and organization
- Should show at least one mascot silhouette

---

## 8. Quick Reference Card

### 8.1. Color Codes

```
208 = Amber (CRAB shell, beak)     78  = Green (Bernard body)
81  = Cyan (Scut body)               201 = Magenta (Bernard throat)
15  = White (eyes, focal points)     245 = Dim (legs, wings, metadata)
0   = Reset all
```

### 8.2. Mascot Sizes

```
CRAB:     3L tiny | 8L small | 14L medium | 19L large
Bernard:  3L tiny | 6L small | 12L medium
Scut:     5L fixed
```

### 8.3. Expression States

```
CRAB:     neutral | working | alert | relaxed
Bernard:  idle | listening | thinking | suggesting | celebrating | departing
Scut:     idle | working | thinking | error | success | asleep | etc.
```

### 8.4. Composition Hierarchy

```
Bernard (airborne, notices first)
  ↓ 2-4 lines
CRAB (grounded, governs)
  ↓ 0-2 lines
Scut (companion, bridges)
```

---

## 9. Receipt

- **Toolkit document:** this file (v1.0)
- **Design system:** `HUMMBL_TERMINAL_CORE_DESIGN_SYSTEM.md`
- **Composable parts:** CRAB (5 claw × 5 eye × 4 mouth × 4 leg = 400 combinations), Bernard (3 beak × 3 eye × 3 body × 4 wing × 3 tail = 108 combinations), Scut (4 eye × 4 mouth × 4 claw = 64 combinations)
- **Templates:** Dashboard panel, sidebar, receipt card, status bar, splash screen
- **Animation patterns:** 4 substitution sequences with timing
- **Artpack standard:** FILE_ID.DIZ template + SAUCE metadata spec
- **Next gate:** Create `terminal_core_demo.py` that renders all templates with live animation

---

*"Good art is not invented. It is composed — from the same handful of characters, arranged with care."*
