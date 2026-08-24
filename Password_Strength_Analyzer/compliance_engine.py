from zxcvbn import zxcvbn
import re
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "compliance.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Bold text for terminal
BOLD = "\033[1m"
RESET = "\033[0m"


password = input("Enter Password: ")


# zxcvbn analysis
result = zxcvbn(password)

score = result['score']
feedback = result['feedback']


# Strength mapping
strength = {
    0: "Very Weak",
    1: "Weak",
    2: "Medium",
    3: "Strong",
    4: "Very Strong"
}


compliance = True


print(f"\n{BOLD}========== Compliance Engine =========={RESET}\n")


# zxcvbn result
print(f"zxcvbn Security Score: {score + 1}/5")
print(f"Password Strength: {strength[score]}\n")



# Policy Compliance
print(f"{BOLD}Policy Compliance:{RESET}\n")


if score >= 3:
    print("PASS - Password strength requirement satisfied")
else:
    print("FAIL - Password strength requirement not satisfied")
    compliance = False


if len(password) >= 8:
    print("PASS - Minimum length requirement")
else:
    print("FAIL - Minimum length requirement")
    compliance = False


if re.search(r"[A-Z]", password):
    print("PASS - Uppercase character detected")
else:
    print("FAIL - Missing uppercase character")
    compliance = False


if re.search(r"[a-z]", password):
    print("PASS - Lowercase character detected")
else:
    print("FAIL - Missing lowercase character")
    compliance = False


if re.search(r"[0-9]", password):
    print("PASS - Numeric character detected")
else:
    print("FAIL - Missing number")
    compliance = False


if re.search(r"[!@#$%^&*]", password):
    print("PASS - Special character detected")
else:
    print("FAIL - Missing special character")
    compliance = False



# Risk Analysis
print(f"\n{BOLD}Risk Analysis:{RESET}\n")


if feedback['warning']:
    print(f"WARNING: {feedback['warning']}")
else:
    print("No security warnings detected")



# Recommendations
print(f"\n{BOLD}Recommendations:{RESET}\n")


if feedback['suggestions']:
    for i, suggestion in enumerate(feedback['suggestions'], 1):
        print(f"{i}. {suggestion}")
else:
    print("No suggestions")



# Final Report
print(f"\n{BOLD}========== Final Report =========={RESET}\n")


if compliance:
    print("COMPLIANCE STATUS: PASS")
else:
    print("COMPLIANCE STATUS: FAIL")


print("=================================")

logging.info(
    "Password Strength: %s | Compliance: %s",
    strength[score],
    "PASS" if compliance else "FAIL"
)
