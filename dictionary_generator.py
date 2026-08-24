usernames = [
    "admin",
    "administrator",
    "employee",
    "manager",
    "root",
    "guest",
    "security",
    "company",
    "user",
    "developer",
    "support",
    "network",
    "linux",
    "windows",
    "database",
    "server",
    "system",
    "login",
    "password",
    "test"
]


# Common Numeric Patterns

patterns = [
    "123",
    "1234",
    "12345",
    "123456",
    "@123",
    "@1234",
    "#123",
    "#2025",
    "2024",
    "2025",
    "2026",
    "!123",
    "@2025",
    "01",
    "007",
    "99"
]


# Keyboard Patterns

keyboard_patterns = [
    "qwerty123",
    "qwerty@123",
    "asdf123",
    "asdf@123",
    "zxcvbn123",
    "zxcvbn@123"
]


# Leet Speak Passwords

leet_speak_patterns = [

    "adm1n",
    "p@ssword",
    "p@ssw0rd",
    "r00t",
    "s3curity",
    "l0gin",
    "us3r",
    "m@nager",
    "c0mpany",
    "d3veloper",
    "w1nd0ws",
    "l1nux",
    "s3rv3r",
    "n3tw0rk"
]


# Common Numeric Password Patterns

patterns = [

    # Sequential Numbers
    "1234",
    "12345",
    "123456",
    "12345678",

    # Repeated Numbers
    "1111",
    "2222",
    "3333",
    "4444",
    "5555",
    "6666",
    "7777",
    "8888",
    "9999",
    "0000",

    # Common Human Choices
    "1212",
    "1122",
    "2211",
    "4321",
    "2580",
    "2468",
    "1357",
    "147258",
    "258369",
    "159753",

    # Years
    "2000",
    "2001",
    "2002",
    "2024",
    "2025",
    "2026",

    # Common Suffixes
    "@123",
    "@1234",
    "@2025",
    "#123",
    "#2025",
    "!123",
    "_123",
    "_2025",

    # Miscellaneous
    "007",
    "786",
    "999",
    "1010",
    "9090"
]


# Keyboard Patterns

keyboard_patterns = [
    "qwerty123",
    "qwerty@123",
    "asdf123",
    "asdf@123",
    "zxcvbn123",
    "zxcvbn@123"
]


# Store Generated Passwords

wordlist = []


# Generate Passwords using Username Patterns

for username in usernames:

    # Original Username
    wordlist.append(username)

    # Username + Numeric Patterns
    for pattern in patterns:
        wordlist.append(username + pattern)
        wordlist.append(pattern + username)

    # Username + Keyboard Patterns
    for keyboard in keyboard_patterns:
        wordlist.append(username + keyboard)
        wordlist.append(keyboard + username)


# Hybrid Passwords

for username in usernames:

    wordlist.append(username.capitalize() + "@123")
    wordlist.append(username.capitalize() + "123")
    wordlist.append(username.upper() + "@2025")
    wordlist.append(username + "_123")
    wordlist.append(username + "@2025")
    wordlist.append(username + "#2025")


# Remove Duplicate Passwords

wordlist = list(set(wordlist))


# Save Passwords into Text File

with open("Generated_Wordlists.txt", "w") as file:
    for password in wordlist:
        file.write(password + "\n")


# Display Output

print("\nWordlist Generated Successfully!")
print("Total Passwords Generated :", len(wordlist))
print("Output File : Generated_Wordlists.txt")
# Store Generated Passwords

wordlist = []


# Generate Passwords using Username Patterns

for username in usernames:

    # Original Username
    wordlist.append(username)

    # Username + Numeric Patterns
    for pattern in patterns:
        wordlist.append(username + pattern)
        wordlist.append(pattern + username)

    # Username + Keyboard Patterns
    for keyboard in keyboard_patterns:
        wordlist.append(username + keyboard)
        wordlist.append(keyboard + username)


# Hybrid Passwords

for username in usernames:

    wordlist.append(username.capitalize() + "@123")
    wordlist.append(username.capitalize() + "123")
    wordlist.append(username.upper() + "@2025")
    wordlist.append(username + "_123")
    wordlist.append(username + "@2025")
    wordlist.append(username + "#2025")


# Remove Duplicate Passwords

wordlist = list(set(wordlist))


# Save Passwords into Text File

with open("Generated_Wordlists.txt", "w") as file:
    for password in wordlist:
        file.write(password + "\n")


# Display Output

print("\nWordlist Generated Successfully!")
print("Total Passwords Generated :", len(wordlist))
print("Output File : Generated_Wordlists.txt")