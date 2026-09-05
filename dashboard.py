import streamlit as st
from pathlib import Path
import math
import re

# =========================================================
# PAGE SETTINGS
# =========================================================
st.set_page_config(
    page_title="Security Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent

# =========================================================
# FILE SEARCH
# =========================================================
def find_file(file_names):
    for name in file_names:
        matches = list(BASE.rglob(name))
        if matches:
            return matches[0]
    return None


WORDLIST_FILE = find_file([
    "Generated_Wordlist.txt",
    "Generated_Wordlists.txt",
    "wordlist.txt",
])

REPORT_FILE = find_file([
    "Password security Audit report.pdf",
    "Password_Security_Audit_Report.pdf",
    "Password_Credential_Attack_Suite_Report.pdf",
])

DOCUMENTED_WORDLIST_COUNT = 2040


def load_wordlist():
    if WORDLIST_FILE is None:
        return []

    try:
        return [
            line.strip()
            for line in WORDLIST_FILE.read_text(
                encoding="utf-8",
                errors="ignore"
            ).splitlines()
            if line.strip()
        ]
    except Exception:
        return []


WORDLIST = load_wordlist()

WORDLIST_COUNT = (
    len(WORDLIST)
    if WORDLIST
    else DOCUMENTED_WORDLIST_COUNT
)

UNIQUE_COUNT = (
    len(set(WORDLIST))
    if WORDLIST
    else DOCUMENTED_WORDLIST_COUNT
)


# =========================================================
# DARK UI
# =========================================================
st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(37,99,235,0.16),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(14,165,233,0.10),
                transparent 30%
            ),
            #07111f;
        color: #eef5ff;
    }

    header[data-testid="stHeader"] {
        background: #07111f !important;
    }

    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    #MainMenu,
    footer {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        background: #091525;
        border-right: 1px solid rgba(148,163,184,0.15);
    }

    [data-testid="stSidebar"] * {
        color: #e8f0fb;
    }

    .brand {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .brand-sub {
        color: #91a4bb;
        font-size: 12px;
        margin-bottom: 20px;
    }

    .hero {
        padding: 30px;
        border-radius: 22px;
        border: 1px solid rgba(96,165,250,0.22);
        background:
            linear-gradient(
                135deg,
                rgba(15,32,55,0.97),
                rgba(8,22,39,0.92)
            );
        box-shadow: 0 18px 50px rgba(0,0,0,0.25);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 31px;
        font-weight: 850;
        line-height: 1.2;
    }

    .hero-text {
        color: #a9bbd0;
        font-size: 14px;
        line-height: 1.6;
        margin-top: 10px;
    }

    .section-title {
        font-size: 23px;
        font-weight: 800;
        margin-top: 22px;
    }

    .section-sub {
        color: #91a4bb;
        font-size: 13px;
        margin-bottom: 16px;
    }

    .metric {
        min-height: 120px;
        padding: 20px;
        border-radius: 17px;
        background: #0c1a2c;
        border: 1px solid rgba(148,163,184,0.15);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }

    .metric-label {
        color: #91a4bb;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.7px;
    }

    .metric-value {
        color: #f6fbff;
        font-size: 27px;
        font-weight: 850;
        margin-top: 7px;
    }

    .metric-note {
        color: #71869e;
        font-size: 11px;
        margin-top: 5px;
    }

    .module {
        min-height: 130px;
        padding: 21px;
        border-radius: 18px;
        background: linear-gradient(
            145deg,
            #0d1d31,
            #0a1728
        );
        border: 1px solid rgba(148,163,184,0.14);
        margin-bottom: 15px;
    }

    .module-icon {
        font-size: 26px;
    }

    .module-title {
        font-size: 17px;
        font-weight: 800;
        margin-top: 7px;
    }

    .module-text {
        color: #94a9bf;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 6px;
    }

    .status {
        display: inline-block;
        padding: 6px 11px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 800;
        margin-right: 5px;
    }

    .green {
        color: #9bf2bd;
        background: rgba(34,197,94,0.12);
        border: 1px solid rgba(34,197,94,0.25);
    }

    .blue {
        color: #9bd4ff;
        background: rgba(59,130,246,0.12);
        border: 1px solid rgba(59,130,246,0.25);
    }

    .value-box {
        padding: 14px 17px;
        border-radius: 13px;
        background: #081423;
        border: 1px solid rgba(96,165,250,0.20);
        font-family: monospace;
        font-size: 14px;
        overflow-wrap: anywhere;
        margin-bottom: 10px;
    }

    .word-pill {
        display: inline-block;
        margin: 4px;
        padding: 8px 11px;
        border-radius: 10px;
        background: #0d2035;
        border: 1px solid rgba(96,165,250,0.15);
        color: #d7e9fb;
        font-size: 12px;
    }

    .result {
        padding: 18px;
        border-radius: 15px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.24);
        margin: 10px 0;
    }

    .result-title {
        font-size: 16px;
        font-weight: 800;
    }

    .result-text {
        color: #a8bbce;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 5px;
    }

    .stTextInput input {
        background: #091727 !important;
        color: #f1f7ff !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# UI HELPERS
# =========================================================
def metric(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def module(icon, title, text):
    st.markdown(
        f"""
        <div class="module">
            <div class="module-icon">{icon}</div>
            <div class="module-title">{title}</div>
            <div class="module-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def heading(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="section-title">{icon} {title}</div>
        <div class="section-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def badge(text, style="green"):
    st.markdown(
        f'<span class="status {style}">{text}</span>',
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown(
        '<div class="brand">🛡️ Security Lab</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-sub">Password & Credential Security Assessment</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Modules",
        [
            "🏠 Dashboard",
            "📁 Directory Generation",
            "🔐 Hash Extraction",
            "⚡ Brute-Force Simulator",
            "🔑 Password Strength Analyzer",
            "📑 Report Generation",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    badge("LAB MODE", "green")
    badge("CONTROLLED TESTING", "blue")


# =========================================================
# DASHBOARD
# =========================================================
if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <div class="hero-title">
                🛡️ Password Cracking & Credential Attack Suite
            </div>

            <div class="hero-text">
                Integrated cybersecurity laboratory dashboard for
                password security, credential assessment and controlled
                authentication testing.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric(
            "Word List Entries",
            f"{WORDLIST_COUNT:,}",
            "Generated password candidates"
        )

    with c2:
        metric(
            "Unique Entries",
            f"{UNIQUE_COUNT:,}",
            "Unique candidates"
        )

    with c3:
        metric(
            "Project Modules",
            "5",
            "Security assessment modules"
        )

    with c4:
        metric(
            "Project Report",
            "READY",
            "Original security report"
        )

    heading(
        "🧩",
        "Project Modules",
        "Security assessment capabilities included in the project."
    )

    a, b = st.columns(2)

    with a:
        module(
            "📁",
            "Directory Generation",
            "Generates and validates password candidate wordlists."
        )

        module(
            "🔐",
            "Hash Extraction",
            "Documented Linux and Windows credential hash assessment."
        )

        module(
            "⚡",
            "Brute-Force Simulator",
            "Controlled authentication testing using laboratory targets."
        )

    with b:
        module(
            "🔑",
            "Password Strength Analyzer",
            "Analyzes password length, character diversity, entropy and common patterns."
        )

        module(
            "📑",
            "Report Generation",
            "Provides the original project security assessment report."
        )

    st.markdown(
        """
        <div class="result">
            <div class="result-title">
                🛡️ Authorized Laboratory Testing
            </div>
            <div class="result-text">
                All documented attack demonstrations are intended for
                controlled cybersecurity laboratory environments and
                authorized security testing.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# DIRECTORY GENERATION
# =========================================================
elif page == "📁 Directory Generation":

    heading(
        "📁",
        "Directory Generation",
        "Generated password-candidate wordlist verification."
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric(
            "Word List Entries",
            f"{WORDLIST_COUNT:,}",
            "Generated wordlist"
        )

    with c2:
        metric(
            "Unique Entries",
            f"{UNIQUE_COUNT:,}",
            "Unique candidates"
        )

    with c3:
        metric(
            "Status",
            "VERIFIED",
            "Project evidence"
        )

    badge("WORDLIST VERIFIED", "green")

    st.markdown("### 🔎 Search Wordlist")

    search = st.text_input(
        "Search",
        placeholder="Search password candidates...",
        label_visibility="collapsed"
    )

    if WORDLIST:

        filtered = [
            word
            for word in WORDLIST
            if not search or search.lower() in word.lower()
        ]

        page_size = 60

        total_pages = max(
            1,
            math.ceil(len(filtered) / page_size)
        )

        current_page = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1
        )

        start = (current_page - 1) * page_size

        visible = filtered[
            start:start + page_size
        ]

        st.caption(
            f"Showing {len(visible):,} of "
            f"{len(filtered):,} matching entries"
        )

        pills = "".join(
            f'<span class="word-pill">{word}</span>'
            for word in visible
        )

        st.markdown(
            pills,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="result">
                <div class="result-title">
                    2,040 Wordlist Entries Documented
                </div>

                <div class="result-text">
                    The project documentation records 2,040 generated
                    password candidates. The original wordlist file
                    can be added to the repository for live browsing.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# HASH EXTRACTION
# =========================================================
elif page == "🔐 Hash Extraction":

    heading(
        "🔐",
        "Hash Extraction",
        "Documented credential-hash extraction results from controlled laboratory systems."
    )

    linux, windows = st.tabs([
        "🐧 Linux",
        "🪟 Windows"
    ])

    # -----------------------------------------------------
    # LINUX
    # -----------------------------------------------------
    with linux:

        module(
            "🐧",
            "Kali Linux Hash Extraction",
            "Controlled test-account assessment using /etc/shadow, "
            "Name-That-Hash and John the Ripper."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric(
                "Environment",
                "Kali Linux",
                "Controlled laboratory"
            )

        with c2:
            metric(
                "Account",
                "projectuser",
                "Test account"
            )

        with c3:
            metric(
                "Hash Type",
                "Yescrypt",
                "Identified format"
            )

        st.markdown("### 📌 Extraction Details")

        details = [
            ("Hash Source", "/etc/shadow"),
            ("Hash File", "new_clean.txt"),
            ("Wordlist", "my_wordlist.txt"),
            ("Tool", "John the Ripper"),
            ("Hash Format", "crypt"),
        ]

        for label, value in details:

            left, right = st.columns([1, 2])

            with left:
                st.caption(label)

            with right:
                st.markdown(
                    f'<div class="value-box">{value}</div>',
                    unsafe_allow_html=True
                )

        st.markdown("### 🔓 Recovery Result")

        st.markdown(
            """
            <div class="result">
                <div class="result-title">
                    Password Recovery: Successful
                </div>

                <div class="result-text">
                    Documented laboratory password:
                    <b>cybersec2026</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "The documented report confirms successful Linux hash "
            "extraction and password recovery. The exact Linux hash "
            "value is not displayed because it was not available in "
            "the extracted report evidence."
        )

    # -----------------------------------------------------
    # WINDOWS
    # -----------------------------------------------------
    with windows:

        module(
            "🪟",
            "Windows Hash Extraction",
            "Controlled Windows SAM assessment with NTLM classification "
            "and documented password recovery."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric(
                "Environment",
                "Windows / Kali Linux",
                "Controlled laboratory"
            )

        with c2:
            metric(
                "Hash Type",
                "NTLM",
                "Identified format"
            )

        with c3:
            metric(
                "Source",
                "SAM Hive",
                "Windows Registry"
            )

        st.markdown("### 👤 Extracted Accounts")

        left, right = st.columns(2)

        with left:

            module(
                "👤",
                "Administrator",
                "Documented NTLM credential result."
            )

            st.markdown("**NTLM Hash**")

            st.markdown(
                '<div class="value-box">'
                '520126a03f5d5a8d836f1c4f34ede7ce'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("**Plaintext Password**")

            st.markdown(
                '<div class="value-box">'
                'Admin123!'
                '</div>',
                unsafe_allow_html=True
            )

            badge("SUCCESSFUL", "green")

        with right:

            module(
                "👤",
                "udaym",
                "Documented NTLM credential result."
            )

            st.markdown("**NTLM Hash**")

            st.markdown(
                '<div class="value-box">'
                '4d707b38c263996f3711b50a867297ff'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown("**Plaintext Password**")

            st.markdown(
                '<div class="value-box">'
                'udaym123!'
                '</div>',
                unsafe_allow_html=True
            )

            badge("SUCCESSFUL", "green")

        st.markdown("### 📝 Result")

        st.success(
            "Documented Windows test accounts were successfully "
            "classified as NTLM credentials and recovered in the "
            "controlled laboratory environment."
        )


# =========================================================
# BRUTE-FORCE SIMULATOR
# =========================================================
elif page == "⚡ Brute-Force Simulator":

    heading(
        "⚡",
        "Brute-Force Simulator",
        "Documented controlled authentication assessments."
    )

    flask, burp = st.tabs([
        "🐍 Python Flask Lab",
        "🕷️ Burp Suite / OWASP Juice Shop"
    ])

    # -----------------------------------------------------
    # FLASK
    # -----------------------------------------------------
    with flask:

        module(
            "🐍",
            "Controlled Python Flask Authentication Lab",
            "Local authentication simulation demonstrating repeated "
            "credential attempts in a controlled environment."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric(
                "Target",
                "Local Flask Lab",
                "Controlled target"
            )

        with c2:
            metric(
                "Username",
                "admin",
                "Documented lab account"
            )

        with c3:
            metric(
                "Successful Response",
                "200 OK",
                "Authentication event"
            )

        st.markdown("### 🔐 Documented Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            metric(
                "Password",
                "Hacker123!",
                "Laboratory result"
            )

        with c2:
            metric(
                "Request",
                "#081",
"Successful request"
            )

        with c3:
            metric(
                "Response Time",
                "1.67 sec",
                "Documented time"
            )

        badge(
            "200 OK — AUTHENTICATION SUCCESSFUL",
            "green"
        )

        st.markdown("### 📊 Request Behaviour")

        st.markdown(
            """
            <div class="result">
                <div class="result-title">
                    401 Unauthorized → 200 OK
                </div>

                <div class="result-text">
                    Failed authentication attempts returned 401
                    responses. The documented successful laboratory
                    authentication event returned 200 OK.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -----------------------------------------------------
    # BURP
    # -----------------------------------------------------
    with burp:

        module(
            "🕷️",
            "Burp Suite Web Credential Assessment",
            "Authorized web authentication assessment against the "
            "OWASP Juice Shop laboratory environment."
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric(
                "Target",
                "OWASP Juice Shop",
                "Controlled laboratory"
            )

        with c2:
            metric(
                "Tool",
                "Burp Suite",
                "Web assessment"
            )

        with c3:
            metric(
                "Response",
                "200 OK",
                "Successful response"
            )

        c1, c2 = st.columns(2)

        with c1:
            metric(
                "Successful Request",
                "#66",
                "Documented request"
            )

        with c2:
            metric(
                "Result",
                "Successful",
                "Documented condition"
            )

        badge(
            "ASSESSMENT COMPLETED",
            "green"
        )

        st.markdown(
            """
            <div class="result">
                <div class="result-title">
                    Web Authentication Analysis
                </div>

                <div class="result-text">
                    Authentication traffic was captured and analyzed
                    in the controlled OWASP Juice Shop environment.
                    Response behaviour was used to identify the
                    documented success condition.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# PASSWORD STRENGTH ANALYZER
# =========================================================
elif page == "🔑 Password Strength Analyzer":

    heading(
        "🔑",
        "Password Strength Analyzer",
        "Enter your own password to generate a fresh security assessment."
    )

    password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter your password...",
        help="The password is analyzed during this session."
    )

    if not password:

        st.info(
            "Enter a password above to start the analysis."
        )

    else:

        length = len(password)

        lower = bool(
            re.search(r"[a-z]", password)
        )

        upper = bool(
            re.search(r"[A-Z]", password)
        )

        number = bool(
            re.search(r"\d", password)
        )

        special = bool(
            re.search(r"[^A-Za-z0-9]", password)
        )

        classes = sum([
            lower,
            upper,
            number,
            special
        ])

        pool = 0

        if lower:
            pool += 26

        if upper:
            pool += 26

        if number:
            pool += 10

        if special:
            pool += 32

        entropy = (
            length * math.log2(pool)
            if pool > 0
            else 0
        )

        common_patterns = [
            "password",
            "123456",
            "12345678",
            "qwerty",
            "admin",
            "admin123",
            "letmein",
            "welcome",
            "cybersec",
            "hacker"
        ]

        predictable = any(
            pattern in password.lower()
            for pattern in common_patterns
        )

        score = 0

        if length >= 8:
            score += 1

        if length >= 12:
            score += 1

        if length >= 16:
            score += 1

        score += classes

        if predictable:
            score = max(
                0,
                score - 2
            )

        if score <= 2:

            strength = "Weak"
            risk = "HIGH RISK"

        elif score <= 4:

            strength = "Moderate"
            risk = "MEDIUM RISK"

        elif score <= 6:

            strength = "Strong"
            risk = "LOW RISK"

        else:

            strength = "Very Strong"
            risk = "LOW RISK"

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric(
                "Strength",
                strength,
                "Overall assessment"
            )

        with c2:
            metric(
                "Risk",
                risk,
                "Security risk"
            )

        with c3:
            metric(
                "Length",
                str(length),
                "Characters"
            )

        with c4:
            metric(
                "Entropy",
                f"{entropy:.1f} bits",
                "Estimated entropy"
            )

        st.markdown("### 📋 Compliance Checks")

        checks = [
            (
                "Minimum length ≥ 8",
                length >= 8
            ),
            (
                "Lowercase character",
                lower
            ),
            (
                "Uppercase character",
                upper
            ),
            (
                "Number",
                number
            ),
            (
                "Special character",
                special
            ),
            (
                "No obvious common pattern",
                not predictable
            ),
        ]

        for label, passed in checks:

            if passed:
                st.success(
                    f"✓ {label}"
                )
            else:
                st.error(
                    f"✗ {label}"
                )

        st.markdown("### 🧠 Threat Analysis")

        if predictable:

            st.warning(
                "A predictable or commonly used pattern was detected. "
                "Use a longer, unique password or passphrase."
            )

        else:

            st.success(
                "No listed common-pattern indicator was detected. "
                "Continue using long, unique credentials and MFA."
            )


# =========================================================
# REPORT GENERATION
# =========================================================
elif page == "📑 Report Generation":

    heading(
        "📑",
        "Report Generation",
        "Original project security assessment report."
    )

    module(
        "📑",
        "Security Assessment & Audit Report",
        "The original project PDF is provided for documentation and HR review."
    )

    if REPORT_FILE:

        st.success(
            "Original project report found."
        )

        with open(
            REPORT_FILE,
            "rb"
        ) as report:

            report_data = report.read()

        st.download_button(
            label="⬇️ Download Original Project Report",
            data=report_data,
            file_name=REPORT_FILE.name,
            mime="application/pdf",
            use_container_width=True
        )

    else:

        st.warning(
            "The original PDF was not found in the repository. "
            "Add the project report PDF to the repository."
        )

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#60758c;
            font-size:11px;
            margin-top:35px;
            padding:15px;
        ">
            Controlled Cybersecurity Testing • Authorized Laboratory Environment
        </div>
        """,
        unsafe_allow_html=True
    )
