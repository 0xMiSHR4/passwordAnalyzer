"""
password_analyzer.py
--------------------
A command-line tool to analyze password strength and generate secure passwords.
"""

import string
import secrets
import getpass
import re
import sys


MIN_LENGTH = 8
RECOMMENDED_LENGTH = 16

UPPERCASE   = string.ascii_uppercase
LOWERCASE   = string.ascii_lowercase
DIGITS      = string.digits
SPECIAL     = string.punctuation
ALL_CHARS   = UPPERCASE + LOWERCASE + DIGITS + SPECIAL

COMMON_PASSWORDS = {
    "password", "123456", "password1", "qwerty", "abc123",
    "letmein", "monkey", "1234567890", "iloveyou", "admin",
    "welcome", "login", "passw0rd", "master", "dragon",
}

STRENGTH_COLORS = {
    "Very Weak":   "\033[91m",
    "Weak":        "\033[93m",
    "Fair":        "\033[33m",
    "Strong":      "\033[92m",
    "Very Strong": "\033[96m",
}
RESET = "\033[0m"
BOLD  = "\033[1m"


def generate_strong_password(length: int = RECOMMENDED_LENGTH) -> str:
    """
    Generate a cryptographically secure password that satisfies all strength
    criteria: at least one uppercase, lowercase, digit, and special character.
    Uses `secrets` (CSPRNG) instead of `random`.
    """
    if length < 4:
        raise ValueError("Password length must be at least 4.")

    required = [
        secrets.choice(UPPERCASE),
        secrets.choice(LOWERCASE),
        secrets.choice(DIGITS),
        secrets.choice(SPECIAL),
    ]
    rest = [secrets.choice(ALL_CHARS) for _ in range(length - 4)]
    password_chars = required + rest
    secrets.SystemRandom().shuffle(password_chars)
    return "".join(password_chars)


def analyze_password(password: str) -> dict:
    """
    Analyze password strength and return a detailed report.

    Returns a dict with:
        score       – 0–100 numeric score
        strength    – "Very Weak" | "Weak" | "Fair" | "Strong" | "Very Strong"
        issues      – list of critical problems
        suggestions – list of improvement tips
        passed      – list of criteria the password already satisfies
    """
    issues      = []
    suggestions = []
    passed      = []
    score       = 0

    if password.lower() in COMMON_PASSWORDS:
        issues.append("This is one of the most commonly used passwords — change it immediately.")

    length = len(password)
    if length < MIN_LENGTH:
        issues.append(f"Too short ({length} chars). Use at least {MIN_LENGTH} characters.")
    elif length < RECOMMENDED_LENGTH:
        suggestions.append(f"Good length, but {RECOMMENDED_LENGTH}+ characters is even safer.")
        score += 10
    else:
        passed.append(f"Great length ({length} characters).")
        score += 25

    has_upper   = any(c in UPPERCASE for c in password)
    has_lower   = any(c in LOWERCASE for c in password)
    has_digit   = any(c in DIGITS    for c in password)
    has_special = any(c in SPECIAL   for c in password)

    if has_upper:
        passed.append("Contains uppercase letters.")
        score += 15
    else:
        suggestions.append("Add at least one uppercase letter (A–Z).")

    if has_lower:
        passed.append("Contains lowercase letters.")
        score += 15
    else:
        suggestions.append("Add at least one lowercase letter (a–z).")

    if has_digit:
        passed.append("Contains digits.")
        score += 15
    else:
        suggestions.append("Add at least one digit (0–9).")

    if has_special:
        passed.append("Contains special characters.")
        score += 20
    else:
        suggestions.append("Add at least one special character (!@#$%…).")

    if re.search(r"(.)\1{2,}", password):
        suggestions.append("Avoid repeating the same character 3+ times in a row.")
        score = max(0, score - 10)

    if re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde)", password.lower()):
        suggestions.append("Avoid sequential patterns like '123' or 'abc'.")
        score = max(0, score - 10)

    unique_ratio = len(set(password)) / max(len(password), 1)
    if unique_ratio > 0.75 and length >= RECOMMENDED_LENGTH:
        score += 10

    score = min(score, 100)

    if score < 20:
        strength = "Very Weak"
    elif score < 40:
        strength = "Weak"
    elif score < 60:
        strength = "Fair"
    elif score < 80:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return {
        "score":       score,
        "strength":    strength,
        "issues":      issues,
        "suggestions": suggestions,
        "passed":      passed,
    }


def colored(text: str, color_code: str) -> str:
    return f"{color_code}{text}{RESET}"


def print_report(report: dict) -> None:
    strength = report["strength"]
    color    = STRENGTH_COLORS.get(strength, "")

    print()
    print(f"  {BOLD}Score   :{RESET}  {colored(str(report['score']) + ' / 100', color)}")
    print(f"  {BOLD}Strength:{RESET}  {colored(strength, color + BOLD)}")

    if report["passed"]:
        print(f"\n  {BOLD}✔  What's good:{RESET}")
        for item in report["passed"]:
            print(f"     • {item}")

    if report["issues"]:
        print(f"\n  {BOLD}✘  Critical issues:{RESET}")
        for item in report["issues"]:
            print(f"     • {colored(item, STRENGTH_COLORS['Very Weak'])}")

    if report["suggestions"]:
        print(f"\n  {BOLD}💡 Suggestions:{RESET}")
        for item in report["suggestions"]:
            print(f"     • {item}")

    print()


def main() -> None:
    print(f"\n{BOLD}╔══════════════════════════════════╗")
    print(  "║      Password Strength Analyzer  ║")
    print(  "╚══════════════════════════════════╝" + RESET)

    try:
        password = getpass.getpass("\n  Enter your password (input hidden): ")
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        sys.exit(0)

    if not password:
        print("  No password entered. Exiting.")
        sys.exit(0)

    report = analyze_password(password)
    print_report(report)

    try:
        prompt = input("  Generate a strong password? (Y/N): ").strip().lower()
    except KeyboardInterrupt:
        print("\n  Cancelled.")
        sys.exit(0)

    if prompt == "y":
        length_input = input(
            f"  Password length? (press Enter for {RECOMMENDED_LENGTH}): "
        ).strip()
        try:
            length = int(length_input) if length_input else RECOMMENDED_LENGTH
            if length < 4:
                raise ValueError
        except ValueError:
            print(f"  Invalid input — using default length of {RECOMMENDED_LENGTH}.")
            length = RECOMMENDED_LENGTH

        new_password = generate_strong_password(length)
        print(f"\n  {BOLD}Generated password:{RESET}  {colored(new_password, STRENGTH_COLORS['Very Strong'])}")

        gen_report = analyze_password(new_password)
        print(f"  Strength: {colored(gen_report['strength'], STRENGTH_COLORS[gen_report['strength']] + BOLD)} "
              f"({gen_report['score']}/100)\n")
    elif prompt == "n":
        print("\n  Alright — keep your password safe!\n")
    else:
        print("\n  Invalid input. Remember to keep your password secure!\n")


if __name__ == "__main__":
    main()
