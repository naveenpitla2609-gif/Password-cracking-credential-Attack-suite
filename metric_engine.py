import math
import re
from pathlib import Path
from datetime import datetime


# ============================================================
# LOG FILE SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_DIR / "logs"

# logs folder లేకపోతే create అవుతుంది
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "metric_engine.log"


# ============================================================
# PASSWORD INPUT
# ============================================================

password = input("Enter Password:")


# ============================================================
# PASSWORD LENGTH ANALYSIS
# ============================================================

length = len(password)


# ============================================================
# CHARACTER TYPE CHECKS
# ============================================================

has_upper = any(c.isupper() for c in password)
has_lower = any(c.islower() for c in password)
has_digit = any(c.isdigit() for c in password)
has_special = any(not c.isalnum() for c in password)


# ============================================================
# CHARACTER POOL SIZE
# ============================================================

pool_size = 0

if has_lower:
    pool_size += 26

if has_upper:
    pool_size += 26

if has_digit:
    pool_size += 10

if has_special:
    pool_size += 32


# ============================================================
# SHANNON ENTROPY
# ============================================================

if length > 0 and pool_size > 0:
    shannon_entropy = length * math.log2(pool_size)
else:
    shannon_entropy = 0


# ============================================================
# PATTERN ANALYSIS
# ============================================================

keyboard_patterns = [
    "qwerty",
    "asdf",
    "zxcv",
    "qwert",
    "asdfg"
]

keyboard_found = any(
    pattern in password.lower()
    for pattern in keyboard_patterns
)


sequential_found = False

for i in range(len(password) - 2):

    a = ord(password[i])
    b = ord(password[i + 1])
    c = ord(password[i + 2])

    if b == a + 1 and c == b + 1:
        sequential_found = True
        break


repeated_found = bool(
    re.search(r"(.)\1\1", password)
)


# ============================================================
# SECURITY SCORE
# ============================================================

score = 0

if length >= 12:
    score += 1

if has_upper:
    score += 1

if has_lower:
    score += 1

if has_digit:
    score += 1

if has_special:
    score += 1

if not keyboard_found:
    score += 1

if not sequential_found and not repeated_found:
    score += 1


# ============================================================
# RISK LEVEL
# ============================================================

if score <= 2:
    risk = "VERY LOW"

elif score <= 3:
    risk = "WEAK"

elif score <= 5:
    risk = "MEDIUM"

elif score == 6:
    risk = "STRONG"

else:
    risk = "VERY STRONG"


# ============================================================
# BLOCK 1 - METRIC ANALYZER
# ============================================================

print()
print("========== METRIC ANALYZER ==========")

print(f"Password Length       : {length}")
print(f"Contains Uppercase    : {has_upper}")
print(f"Contains Lowercase    : {has_lower}")
print(f"Contains Numbers      : {has_digit}")
print(f"Contains Special Char : {has_special}")

print(f"Character Pool Size   : {pool_size}")
print(f"Shannon Entropy       : {shannon_entropy:.2f} bits")

print()
print("Pattern Analysis")

print(f"Keyboard Pattern      : {keyboard_found}")
print(f"Sequential Pattern    : {sequential_found}")
print(f"Repeated Characters   : {repeated_found}")

print()
print("Security Score")

print(f"Score                 : {score}/7")
print(f"Risk Level            : {risk}")


# ============================================================
# BLOCK 2 - METRIC ANALYZER REPORT
# ============================================================

print()
print("==============================================")
print("          METRIC ANALYZER REPORT")
print("==============================================")

print(f"Password Length       : {length}")
print(f"Character Pool Size   : {pool_size}")
print(f"Shannon Entropy       : {shannon_entropy:.2f} bits")
print(f"Keyboard Pattern      : {keyboard_found}")
print(f"Sequential Pattern    : {sequential_found}")
print(f"Repeated Characters   : {repeated_found}")
print(f"Security Score        : {score}/7")
print(f"Overall Risk Level    : {risk}")


# ============================================================
# RECOMMENDATIONS
# ============================================================

print()
print("Recommendations:")

if length < 12:
    print("- Use at least 12 characters.")

if not has_upper:
    print("- Add uppercase letters.")

if not has_special:
    print("- Add special characters.")

if keyboard_found:
    print("- Avoid keyboard patterns (qwerty, asdf, zxcv).")

if sequential_found:
    print("- Avoid sequential patterns (12345, abcdef).")

if repeated_found:
    print("- Avoid repeated characters (aaa, 111).")


# ============================================================
# SAVE LOG
# ============================================================

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

log_line = (
    f"{timestamp} | INFO | Metric Analysis | "
    f"Length={length} | "
    f"Pool={pool_size} | "
    f"Entropy={shannon_entropy:.2f} bits | "
    f"Score={score}/7 | "
    f"Risk={risk}\n"
)

# "a" = APPEND
# For every run, a new line comes
with open(LOG_FILE, "a", encoding="utf-8") as file:
    file.write(log_line)


# ============================================================
# CONFIRM LOG LOCATION
# ============================================================

print()
print("Log saved successfully!")
print(f"Log file: {LOG_FILE}")
