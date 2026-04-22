# 🔐 Password Strength Analyzer

A command-line tool that evaluates how secure your password is, tells you exactly why, and can generate a cryptographically strong replacement — all without your password ever leaving your machine.

---

## Features

| Feature | Details |
|---|---|
| **Strength scoring** | 0–100 numeric score with a five-tier label (Very Weak → Very Strong) |
| **Detailed feedback** | Separate lists for what's good ✔, critical issues ✘, and improvement tips 💡 |
| **Common password check** | Flags passwords found in the most-used password lists |
| **Pattern detection** | Catches sequential runs (`123`, `abc`) and repeated characters (`aaa`) |
| **Secure generation** | Uses Python's `secrets` module (CSPRNG) — not `random` |
| **Configurable length** | Choose any length when generating; defaults to 16 characters |
| **Hidden input** | Password is never echoed to the terminal (`getpass`) |
| **Colour-coded output** | ANSI colours highlight strength at a glance |

---

## Requirements

- Python **3.6 or later**
- No third-party packages — only the standard library

---

## Quick Start

```bash
# Clone or download the repo
git clone https://github.com/your-username/passwordAnalyzer.git
cd passwordAnalyzer

# Run the analyzer
python password_analyzer.py
```

---

## Usage Walkthrough

```
╔══════════════════════════════════╗
║      Password Strength Analyzer  ║
╚══════════════════════════════════╝

  Enter your password (input hidden): 

  Score   :  62 / 100
  Strength:  Strong

  ✔  What's good:
     • Great length (18 characters).
     • Contains uppercase letters.
     • Contains lowercase letters.
     • Contains digits.

  💡 Suggestions:
     • Add at least one special character (!@#$%…).

  Generate a strong password? (Y/N): y
  Password length? (press Enter for 16): 20

  Generated password:  x#K9mL!qR2@nWdYv&Tz0
  Strength: Very Strong (95/100)
```

---

## How Scoring Works

| Criterion | Points |
|---|---|
| Length ≥ 16 characters | +25 |
| Length 8–15 characters | +10 |
| Contains uppercase letters | +15 |
| Contains lowercase letters | +15 |
| Contains digits | +15 |
| Contains special characters | +20 |
| High character uniqueness + long | +10 |
| Sequential pattern detected | −10 |
| Repeated characters (3+) detected | −10 |

| Score | Label |
|---|---|
| 0–19 | Very Weak |
| 20–39 | Weak |
| 40–59 | Fair |
| 60–79 | Strong |
| 80–100 | Very Strong |

---

## License

MIT — free to use, modify, and distribute.
