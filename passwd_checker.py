#!/usr/bin/env python3
import string
import math

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Load dictionary (top passwords)
with open("demo_passwords.txt", "r", encoding="utf-8", errors="ignore") as f:
    common_passwords = [line.strip() for line in f]

def password_score(password):
    """NIST-inspired scoring system returning percentage."""
    score = 0
    total_points = 7  # max possible points

    # Length check
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1

    # Character diversity
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    # Bonus: No repeated characters
    if len(set(password)) == len(password):
        score += 1

    percentage = math.floor((score / total_points) * 100)
    return percentage

def crack_time_estimate(percentage):
    """Estimate crack time based on score percentage."""
    if percentage < 30:
        return "Instant to minutes"
    elif percentage < 50:
        return "Minutes to hours"
    elif percentage < 70:
        return "Hours to days"
    elif percentage < 85:
        return "Days to months"
    else:
        return "Months to years"

def strength_bar(percentage, length=20):
    """Generate a visual strength bar."""
    filled_length = int(length * percentage // 100)
    bar = "█" * filled_length + "░" * (length - filled_length)
    return f"[{bar}]"

def check_password(password):
    if password in common_passwords:
        return (f"{RED}❌ This password is in the dictionary list — easily crackable!\n"
                f"{strength_bar(0)} 0% Strength\n"
                f"⏳ Estimated crack time: Instant{RESET}")
    else:
        percentage = password_score(password)
        crack_time = crack_time_estimate(percentage)
        color = GREEN if percentage >= 70 else (YELLOW if percentage >= 40 else RED)
        return (f"{color}✅ Not in dictionary.\n"
                f"{strength_bar(percentage)} {percentage}% Strength\n"
                f"⏳ Estimated crack time: {crack_time}{RESET}")

if __name__ == "__main__":
    print(f"{CYAN}🔐 Dictionary-Based Password Strength Checker (NIST-based){RESET}\n")
    pwd = input(f"{YELLOW}Enter a password to check:{RESET} ").strip()
    print("\n" + check_password(pwd))
