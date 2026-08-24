from zxcvbn import zxcvbn
from pathlib import Path
from datetime import datetime


# ============================================================
# LOG FILE LOCATION
# ~/credentialsuite/Threat_engine/threat_engine.py
#                    |
#                    └── ../logs/threat_engine.log
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "threat_engine.log"

# Create logs folder automatically if it doesn't exist
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# GET PASSWORD
# ============================================================

password = input("Enter Password: ")


# ============================================================
# ANALYZE PASSWORD
# ============================================================

result = zxcvbn(password)

score = result["score"]
feedback = result["feedback"]


# ============================================================
# STRENGTH LEVEL
# ============================================================

strength = {
    0: "Very Weak",
    1: "Weak",
    2: "Medium",
    3: "Strong",
    4: "Very Strong"
}


# ============================================================
# RISK LEVEL
# ============================================================

risk_levels = {
    0: "Very High",
    1: "High",
    2: "Medium",
    3: "Low",
    4: "Very Low"
}


display_score = score + 1

strength_text = strength[score]
risk_text = risk_levels[score]


# ============================================================
# CRACK TIME
# ============================================================

crack_time = result["crack_times_display"][
    "offline_fast_hashing_1e10_per_second"
]

if "less than a second" in crack_time.lower():
    crack_time = "1 second"

elif crack_time:
    parts = crack_time.split()

    if len(parts) == 2:
        number = parts[0]
        unit = parts[1]

        if number != "1" and not unit.endswith("s"):
            unit = unit + "s"

        crack_time = number + " " + unit


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print("\n================ Password Analysis ================\n")

print(f"zxcvbn Score: {display_score} / 5")
print(f"Password Strength: {strength_text}")
print(f"Risk Level: {risk_text}")
print(f"Estimated Crack Time: {crack_time}")


# ============================================================
# WARNING
# ============================================================

if feedback["warning"]:
    print("Feedback Warning:", feedback["warning"])
else:
    print("Feedback Warning: No warnings")


# ============================================================
# SUGGESTIONS
# ============================================================

print("\nSuggestions:")

letters = ["A", "B", "C", "D", "E"]

if feedback["suggestions"]:

    for i, suggestion in enumerate(feedback["suggestions"]):
        print(f"{letters[i]}. {suggestion}")

else:
    print("No suggestions. Your password is strong.")


print("====================================================")


# ============================================================
# SAVE LOG
# IMPORTANT:
# Password itself is NOT saved.
# Every execution APPENDS a new entry.
# ============================================================

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

log_entry = (
    f"{timestamp} | "
    f"Threat Engine | "
    f"Score: {display_score}/5 | "
    f"Strength: {strength_text} | "
    f"Risk: {risk_text} | "
    f"Crack Time: {crack_time}\n"
)

with open(LOG_FILE, "a", encoding="utf-8") as log:
    log.write(log_entry)


print(f"\nLog saved to: {LOG_FILE}")
