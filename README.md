# Password Cracking & Credential Attack Suite 🛡️

A comprehensive, modular cybersecurity testing suite developed during an internship at **Unified Mentor Pvt. Ltd**. This framework automates the workflow from directory generation to structural credential testing, vulnerability simulation, and automated compliance reporting.

## 📌 Project Overview

---

## 🚀 Key Modules & Features

### 1. Dictionary Generator
* Generates optimized target wordlists with thousands of predictive password variations.
* Output Verification: Generates `Generated_Wordlist.txt` with structured dictionary metrics.

### 2. Hash Extraction & Cryptanalysis
* **Linux Environment:** Automated `/etc/shadow` extraction, hash identification via `Name-That-Hash`, and target recovery using `John the Ripper (crypt format)`.
* **Windows Environment:** Implements offline SAM/System hive registry extraction and parsing via `samdump2` to analyze NTLM cryptographic configurations.

### 3. Brute-Force Simulator
* Implements a localized Flask authentication gateway (Port 5000) named *Security Lab Authentication*.
* Features an automated multi-threaded attack script (`brute_force.py`) using structured payload matrices.
* Full integration with proxy analysis workflows via **Burp Suite (Sniper Mode)**.

### 4. Password Strength Analyzer
* **Compliance Engine:** Uses `zxcvbn` architecture to validate corporate security complexity policies.
* **Metric Engine:** Computes advanced mathematical properties including **Shannon Entropy** and character pool distribution ratios.
* **Threat Engine:** Conducts predictive offline crack-time mapping and threat vector classifications.

### 5. Automated Report Generator
* Consolidates diagnostic execution variables, cryptographic logs, and runtime evidence directly into a finalized executive audit PDF.

---

## 🛠️ Installation & Setup

```bash
# Clone the repository
git clone https://github.com

# Navigate into the project folder
cd Credential-Attack-Strength-Suite

# Install required framework dependencies
pip install -r requirements.txt
```

---

## 📊 Analytics Summary Matrix

| Environment | Analytical Tool | Target Cipher Scheme | Plaintext Recovery Status |
| :--- | :--- | :--- | :--- |
| Kali Linux | John the Ripper | Yescrypt (crypt) | Successfully Recovered |
| Windows OS | Samdump2 / JTR | NTLM (nt routine) | Compromised / Plaintext Extracted |
| Flask App | brute_force.py | Plaintext HTTP POST | 200 OK Status Triggered |

---

## 🖨️ Screenshots & Evidence
*(Include active terminal execution flows here)*

*Flask Authentication Laboratory Web UI:*
  ![Design UI 1](Bruite_Force_Simulator/Python%20scrrenshots/Design%20UI%201.png)

*Burp Suite Proxy Interception Framework:*
  ![Login 2](Bruite_Force_Simulator/Burpsuite%20screenshots/Login%202.jpg)

---

## ⚖️ Authorization Notice & Disclaimer
All testing activities within this suite are designed strictly for authorized, controlled laboratory environments. Unauthorized deployment against external networks is strictly prohibited.
