# Password Cracking & Credential Attack Suite 🛡️

A comprehensive, modular cybersecurity testing suite developed during an internship at **Unified Mentor Pvt. Ltd**. This framework automates the workflow from directory generation to structural credential testing, vulnerability simulation, and automated compliance reporting.

## 📌 Project Overview

This native, modular cybersecurity framework is designed to automate the lifecycle of credential vulnerability testing and defensive baseline analytics within controlled laboratory environments. The framework integrates advanced custom dictionary generation engines with offline cryptographic hash extraction modules to evaluate the resistance of authentication schemas against brute-force vector matrices. By embedding a localized Flask-driven web target loop, the system simulates real-world attack flows and enables clean traffic analysis through upstream proxy auditing suites like Burp Suite. Furthermore, the architecture implements predictive threat calculation models using Shannon Entropy metrics to profile offline crack-time variables against enterprise password policies. All diagnostic logs and runtime evidence are programmatically aggregated into an automated audit layout to demonstrate structural mitigation timelines against modern credential attacks.

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

### 🖥️ 1. Flask Security Laboratory Gateway
> **Description:** *Automated multi-threaded target execution matrix showing the localized authentication server initialization.*
  
![Terminal 1](Bruite_Force_Simulator/Python%20scrrenshots/Terminal%201.png)

---

### 🛡️ 2. Burp Suite Proxy Interception Framework
> **Description:** *Live cryptographic HTTP POST request analysis and intruder payload verification metrics.*

![login 3](Bruite_Force_Simulator/Burpsuite%20screenshots/login%203.jpg)

---

## ⚠️  Authorization Notice & Disclaimer
All testing activities within this suite are designed strictly for authorized, controlled laboratory environments. Unauthorized deployment against external networks is strictly prohibited.
