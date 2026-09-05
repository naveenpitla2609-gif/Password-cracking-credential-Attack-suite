import streamlit as st
from pathlib import Path
import math
import re

# ============================================================
# PAGE
# ============================================================
st.set_page_config(
    page_title="Security Lab | Password & Credential Assessment",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE = Path(__file__).resolve().parent

# ============================================================
# PROJECT FILE DISCOVERY
# ============================================================
def find_first(names):
    for root in [BASE] + [p for p in BASE.iterdir() if p.is_dir()]:
        for name in names:
            candidate = root / name
            if candidate.exists() and candidate.is_file():
                return candidate

    # Recursive fallback
    for name in names:
        matches = list(BASE.rglob(name))
        if matches:
            return matches[0]

    return None


WORDLIST_FILE = find_first([
    "Generated_Wordlist.txt",
    "Generated_Wordlists.txt",
    "wordlist.txt",
])

REPORT_FILE = find_first([
    "Password security Audit report.pdf",
    "Password_Security_Audit_Report.pdf",
    "Password_Credential_Attack_Suite_Report.pdf",
])

# The project report documents 2,040 generated entries.
# If the real wordlist is present, the live count is used instead.
DOCUMENTED_WORDLIST_COUNT = 2040


def load_wordlist():
    if not WORDLIST_FILE:
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

WORDLIST_ENTRIES = (
    len(WORDLIST)
    if WORDLIST
    else DOCUMENTED_WORDLIST_COUNT
)

UNIQUE_ENTRIES = (
    len(set(WORDLIST))
    if WORDLIST
    else DOCUMENTED_WORDLIST_COUNT
)

# ============================================================
# CSS - UI ONLY
# ============================================================
st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(36, 99, 235, .14),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(14, 165, 233, .10),
                transparent 28%
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
        border-right: 1px solid rgba(148,163,184,.14);
    }

    [data-testid="stSidebar"] * {
        color: #e8f0fb;
    }

    .brand {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -.5px;
        margin-bottom: 3px;
    }

    .brand-sub {
        color: #91a4bb;
        font-size: 12px;
        margin-bottom: 20px;
    }

    .hero {
        padding: 28px 30px;
        border: 1px solid rgba(96,165,250,.22);
        border-radius: 22px;
        background:
            linear-gradient(
                135deg,
                rgba(15,32,55,.96),
                rgba(8,22,39,.88)
            );
        box-shadow: 0 18px 50px rgba(0,0,0,.22);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 31px;
        line-height: 1.15;
        font-weight: 850;
        letter-spacing: -1px;
    }

    .hero-text {
        color: #a9bbd0;
        margin-top: 10px;
        max-width: 900px;
        font-size: 14px;
        line-height: 1.6;
    }

    .section-title {
        font-size: 22px;
        font-weight: 800;
        margin: 20px 0 4px;
    }

    .section-sub {
        color: #91a4bb;
        font-size: 13px;
        margin-bottom: 15px;
    }

    .metric {
        min-height: 125px;
        padding: 19px;
        border-radius: 17px;
        background: #0c1a2c;
        border: 1px solid rgba(148,163,184,.15);
        box-shadow: 0 12px 30px rgba(0,0,0,.15);
    }

    .metric-label {
        color: #91a4bb;
        font-size: 12px;
        font-weight: 650;
        text-transform: uppercase;
        letter-spacing: .7px;
    }

    .metric-value {
        font-size: 27px;
        font-weight: 850;
        margin-top: 7px;
        color: #f6fbff;
    }

    .metric-note {
        color: #71869e;
        font-size: 11px;
        margin-top: 5px;
    }

    .module {
        min-height: 135px;
        padding: 21px;
        border-radius: 18px;
        background:
            linear-gradient(
                145deg,
                #0d1d31,
                #0a1728
            );
        border: 1px solid rgba(148,163,184,.14);
        margin-bottom: 14px;
    }

    .module-icon {
        font-size: 25px;
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
        letter-spacing: .3px;
    }

    .green {
        color: #9bf2bd;
        background: rgba(34,197,94,.12);
        border: 1px solid rgba(34,197,94,.25);
    }

    .blue {
        color: #9bd4ff;
        background: rgba(59,130,246,.12);
        border: 1px solid rgba(59,130,246,.25);
    }

    .amber {
        color: #ffd58a;
        background: rgba(245,158,11,.12);
        border: 1px solid rgba(245,158,11,.25);
    }

    .value-box {
        padding: 15px 17px;
        border-radius: 13px;
        background: #081423;
        border: 1px solid rgba(96,165,250,.20);
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        font-size: 14px;
        overflow-wrap: anywhere;
    }

    .word-pill {
        display: inline-block;
        margin: 4px 5px 4px 0;
        padding: 8px 11px;
        border-radius: 10px;
        background: #0d2035;
        border: 1px solid rgba(96,165,250,.15);
        color: #d7e9fb;
        font-size: 12px;
    }

    .result-good {
        padding: 17px;
        border-radius: 15px;
        background: rgba(34,197,94,.08);
        border: 1px solid rgba(34,197,94,.24);
    }

    .result-title {
        font-weight: 800;
        font-size: 16px;
    }

    .result-text {
        color: #a8bbce;
        font-size: 13px;
        margin-top: 5px;
        line-height: 1.55;
    }

    .wordlist-box {
        background: #081423;
        border: 1px solid rgba(96,165,250,.20);
        border-radius: 16px;
        padding: 8px 0;
        overflow: hidden;
    }

    .word-row {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 9px 17px;
        border-bottom: 1px solid rgba(148,163,184,.09);
        font-size: 13px;
    }

    .word-row:last-child {
        border-bottom: 0;
    }

    .word-number {
        width: 48px;
        flex: 0 0 48px;
        color: #6f87a0;
        font-size: 11px;
        font-weight: 700;
        text-align: right;
    }

    .word-value {
        color: #e4effb;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
        overflow-wrap: anywhere;
    }

    .time-note {
        color: #91a4bb;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 8px;
    }

    .footer-note {
        text-align: center;
        color: #60758c;
        font-size: 11px;
        margin-top: 35px;
        padding: 15px;
    }

    .stTextInput input {
        background: #091727 !important;
        color: #f1f7ff !important;
        border-color: rgba(148,163,184,.20) !important;
    }

    div[data-testid="stFileDownloadButton"] button,
    .stDownloadButton button {
        width: 100%;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SMALL UI HELPERS
# ============================================================
def metric_card(label, value, note=""):
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


def module_card(icon, title, text):
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


def section_header(icon, title, subtitle):
    st.markdown(
        f"""
        <div class="section-title">{icon} {title}</div>
        <div class="section-sub">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


def status_badge(text, kind="green"):
    st.markdown(
        f'<span class="status {kind}">{text}</span>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.markdown(
        '<div class="brand">🛡️ Security Lab</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-sub">'
        'Password & Credential Security Assessment'
        '</div>',
        unsafe_allow_html=True,
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

    status_badge(
        "LAB MODE",
        "green",
    )

    status_badge(
        "CONTROLLED TESTING",
        "blue",
    )


# ============================================================
# DASHBOARD
# ============================================================
if page == "🏠 Dashboard":

    # Native Streamlit text is intentionally used here.
    # This prevents the project title/description from appearing
    # as raw HTML code in the Dashboard.

    st.title(
        "🛡️ Password Cracking & Credential Attack Suite"
    )

    st.caption(
        "Integrated security laboratory dashboard for a documented "
        "password and credential security assessment. Results shown "
        "here represent controlled, authorized laboratory testing."
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card(
            "Word List Entries",
            f"{WORDLIST_ENTRIES:,}",
            "Generated wordlist",
        )

    with c2:
        metric_card(
            "Unique Entries",
            f"{UNIQUE_ENTRIES:,}",
            "Unique candidates",
        )

    with c3:
        metric_card(
            "Project Modules",
            "5",
            "Documented modules",
        )

    with c4:
        metric_card(
            "Project Report",
            "READY",
            "Original PDF",
        )

    section_header(
        "🧩",
        "Project Modules",
        "Five documented security assessment modules.",
    )

    cols = st.columns(2)

    with cols[0]:

        module_card(
            "📁",
            "Directory Generation",
            "Creates and verifies password candidate "
            "wordlists for controlled testing.",
        )

        module_card(
            "🔐",
            "Hash Extraction",
            "Documents Linux and Windows credential-hash "
            "extraction and recovery results.",
        )

        module_card(
            "⚡",
            "Brute-Force Simulator",
            "Presents the controlled Flask authentication "
            "simulation and web credential assessment.",
        )

    with cols[1]:

        module_card(
            "🔑",
            "Password Strength Analyzer",
            "Interactive analysis using compliance, metric "
            "and threat-oriented checks.",
        )

        module_card(
            "📑",
            "Automated Report Generator",
            "Provides the original professional security "
            "assessment report.",
        )

        module_card(
            "🛡️",
            "Security Focus",
            "Highlights strong passwords, MFA, rate limiting, "
            "monitoring and secure password storage.",
        )


# ============================================================
# DIRECTORY GENERATION
# ============================================================
elif page == "📁 Directory Generation":

    section_header(
        "📁",
        "Directory Generation",
        "Generated password-candidate wordlist verification and review.",
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card(
            "Word List Entries",
            f"{WORDLIST_ENTRIES:,}",
            "Generated_Wordlist.txt",
        )

    with c2:
        metric_card(
            "Unique Entries",
            f"{UNIQUE_ENTRIES:,}",
            "Unique candidates",
        )

    with c3:
        metric_card(
            "Source",
            "FOUND" if WORDLIST_FILE else "DOCUMENTED",
            "Live file when available",
        )

    status_badge(
        "WORDLIST VERIFIED",
        "green",
    )

    st.markdown("### 🔎 Search Wordlist")

    query = st.text_input(
        "Search",
        placeholder="Type a word or pattern...",
        label_visibility="collapsed",
    )

    if WORDLIST:

        filtered = [
            x
            for x in WORDLIST
            if not query or query.lower() in x.lower()
        ]

        page_size = 60

        total_pages = max(
            1,
            math.ceil(len(filtered) / page_size),
        )

        current = st.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )

        start = (current - 1) * page_size

        shown = filtered[
            start:start + page_size
        ]

        st.caption(
            f"Showing {len(shown):,} of "
            f"{len(filtered):,} matching entries"
        )

        rows = []

        for offset, word in enumerate(shown):

            number = start + offset + 1

            safe_word = (
                str(word)
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;")
                .replace("'", "&#39;")
            )

            rows.append(
                f'<div class="word-row">'
                f'<div class="word-number">'
                f'{number:04d}'
                f'</div>'
                f'<div class="word-value">'
                f'{safe_word}'
                f'</div>'
                f'</div>'
            )

        st.markdown(
            '<div class="wordlist-box">'
            + "".join(rows)
            + '</div>',
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="result-good">

                <div class="result-title">
                    2,040 entries documented
                </div>

                <div class="result-text">
                    The project report records 2,040 generated
                    password entries. Add the original
                    Generated_Wordlist.txt file to the repository
                    to enable live word-by-word browsing.
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# HASH EXTRACTION
# ============================================================
elif page == "🔐 Hash Extraction":

    section_header(
        "🔐",
        "Hash Extraction",
        "Documented credential-hash extraction results from "
        "controlled Linux and Windows environments.",
    )

    linux_tab, windows_tab = st.tabs(
        [
            "🐧 Linux",
            "🪟 Windows",
        ]
    )

    # --------------------------------------------------------
    # LINUX
    # --------------------------------------------------------
    with linux_tab:

        module_card(
            "🐧",
            "Kali Linux Hash Extraction",
            "Controlled test account assessment using "
            "/etc/shadow, Name-That-Hash and John the Ripper.",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Environment",
                "Kali Linux",
                "Controlled laboratory",
            )

        with c2:
            metric_card(
                "Account",
                "projectuser",
                "Test account",
            )

        with c3:
            metric_card(
                "Hash Type",
                "Yescrypt",
                "Identified from evidence",
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

            a, b = st.columns([1, 2])

            with a:
                st.caption(label)

            with b:
                st.markdown(
                    f'<div class="value-box">{value}</div>',
                    unsafe_allow_html=True,
                )

        st.markdown("### 🔓 Recovery Result")

        st.success(
            "Password Recovery: Successful — "
            "documented test password: 1122"
        )

        st.markdown("### 🔐 Hash Value")

        st.info(
            "The report confirms successful extraction and recovery, "
            "but the exact Linux hash string is not reproduced in the "
            "report text. The UI therefore does not invent a hash value."
        )

    # --------------------------------------------------------
    # WINDOWS
    # --------------------------------------------------------
    with windows_tab:

        module_card(
            "🪟",
            "Windows Hash Extraction",
            "Controlled Windows SAM assessment with NTLM "
            "classification and successful password recovery.",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Environment",
                "Windows / Kali Linux",
                "Controlled laboratory",
            )

        with c2:
            metric_card(
                "Hash Type",
                "NTLM",
                "Identified format",
            )

        with c3:
            metric_card(
                "Source",
                "SAM Hive",
                "Windows Registry",
            )

        st.markdown("### 👤 Extracted Accounts")

        a1, a2 = st.columns(2)

        # Administrator
        with a1:

            module_card(
                "👤",
                "Administrator",
                "Documented NTLM credential result.",
            )

            st.markdown("**NTLM Hash**")

            st.markdown(
                '<div class="value-box">'
                '520126a03f5d5a8d836f1c4f34ede7ce'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Plaintext Password**")

            st.markdown(
                '<div class="value-box">'
                'Admin123!'
                '</div>',
                unsafe_allow_html=True,
            )

            status_badge(
                "SUCCESSFUL",
                "green",
            )

        # udaym
        with a2:

            module_card(
                "👤",
                "udaym",
                "Documented NTLM credential result.",
            )

            st.markdown("**NTLM Hash**")

            st.markdown(
                '<div class="value-box">'
                '4d707b38c263996f3711b50a867297ff'
                '</div>',
                unsafe_allow_html=True,
            )

            st.markdown("**Plaintext Password**")

            st.markdown(
                '<div class="value-box">'
                'udaym123!'
                '</div>',
                unsafe_allow_html=True,
            )

            status_badge(
                "SUCCESSFUL",
                "green",
            )

        st.markdown("### 📝 Result")

        st.success(
            "Windows credential hashes were classified as NTLM "
            "and the documented test accounts were successfully "
            "recovered in plaintext."
        )


# ============================================================
# BRUTE FORCE SIMULATOR
# ============================================================
elif page == "⚡ Brute-Force Simulator":

    section_header(
        "⚡",
        "Brute-Force Simulator",
        "Two separate controlled laboratory assessments.",
    )

    python_tab, burp_tab = st.tabs(
        [
            "🐍 Python Flask Lab",
            "🕷️ Burp Suite / OWASP Juice Shop",
        ]
    )

    # --------------------------------------------------------
    # PYTHON FLASK
    # --------------------------------------------------------
    with python_tab:

        module_card(
            "🐍",
            "Controlled Python Flask Authentication Lab",
            "A local authentication simulation used to "
            "demonstrate repeated credential attempts.",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Target",
                "Local Flask Lab",
                "Controlled laboratory",
            )

        with c2:
            metric_card(
                "Username",
                "admin",
                "Documented lab account",
            )

        with c3:
            metric_card(
                "Successful Response",
                "200 OK",
                "Authentication event",
            )

        st.markdown("### 🔐 Documented Result")

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Password",
                "Hacker123!",
                "Successful laboratory result",
            )

        with c2:
            metric_card(
                "Request",
                "#081",
                "Documented request",
            )

        with c3:
            metric_card(
                "Response Time",
                "1.67 sec",
                "Documented assessment time",
            )

        status_badge(
            "200 OK — AUTHENTICATION SUCCESSFUL",
            "green",
        )

        st.markdown("### 📊 Request Behaviour")

        st.info(
            "401 Unauthorized → 200 OK\n\n"
            "Failed authentication attempts returned 401 responses. "
            "The successful laboratory authentication event returned "
            "200 OK."
        )

    # --------------------------------------------------------
    # BURP / JUICE SHOP
    # --------------------------------------------------------
    with burp_tab:

        module_card(
            "🕷️",
            "Burp Suite Web Credential Assessment",
            "Authorized web authentication assessment against "
            "the intentionally vulnerable OWASP Juice Shop "
            "laboratory target.",
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            metric_card(
                "Target",
                "OWASP Juice Shop",
                "Controlled laboratory",
            )

        with c2:
            metric_card(
                "Tool",
                "Burp Suite",
                "Web security assessment",
            )

        with c3:
            metric_card(
                "Response",
                "200 OK",
                "Successful documented response",
            )

        c1, c2 = st.columns(2)

        with c1:
            metric_card(
                "Successful Request",
                "#66",
                "Documented request",
            )

        with c2:
            metric_card(
                "Result",
                "Successful",
                "Authentication condition identified",
            )

        status_badge(
            "ASSESSMENT COMPLETED",
            "green",
        )

        st.info(
            "Web Authentication Analysis\n\n"
            "Authentication traffic was captured and analyzed in "
            "the controlled OWASP Juice Shop environment. Response "
            "behaviour was used to identify the documented success "
            "condition."
        )


# ============================================================
# PASSWORD STRENGTH ANALYZER
# ============================================================
elif page == "🔑 Password Strength Analyzer":

    section_header(
        "🔑",
        "Password Strength Analyzer",
        "Enter your own password to generate a fresh security assessment.",
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter a password to analyze...",
        help="The password is analyzed in memory for this session.",
    )

    if not password:

        st.info(
            "Enter a password above to start the analysis."
        )

    else:

        length = len(password)

        lower = bool(
            re.search(
                r"[a-z]",
                password
            )
        )

        upper = bool(
            re.search(
                r"[A-Z]",
                password
            )
        )

        digit = bool(
            re.search(
                r"\d",
                password
            )
        )

        special = bool(
            re.search(
                r"[^A-Za-z0-9]",
                password
            )
        )

        classes = sum(
            [
                lower,
                upper,
                digit,
                special,
            ]
        )

        pool = 0

        if lower:
            pool += 26

        if upper:
            pool += 26

        if digit:
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
            "kali123",
            "cybersec",
            "hacker",
        ]

        predictable = any(
            p in password.lower()
            for p in common_patterns
        )

        # ----------------------------------------------------
        # STRENGTH SCORE
        # ----------------------------------------------------
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

        # ----------------------------------------------------
        # MAIN METRICS
        # ----------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            metric_card(
                "Strength",
                strength,
                "Overall assessment",
            )

        with c2:
            metric_card(
                "Risk",
                risk,
                "Threat-oriented result",
            )

        with c3:
            metric_card(
                "Length",
                str(length),
                "Characters",
            )

        with c4:
            metric_card(
                "Entropy",
                f"{entropy:.1f} bits",
                "Shannon-style estimate",
            )

        # ----------------------------------------------------
        # THEORETICAL CRACKING TIME
        # ----------------------------------------------------
        # This is a theoretical offline estimate.
        # It assumes 1 billion guesses per second.
        # Real-world results depend on hashing algorithm,
        # hardware, rate limiting and attack strategy.

        expected_guesses = (
            2 ** entropy
            if entropy < 1024
            else float("inf")
        )

        guesses_per_second = 1_000_000_000

        expected_seconds = (
            expected_guesses / 2
        ) / guesses_per_second

        def format_duration(seconds):

            if seconds < 1:
                return "< 1 sec"

            if seconds < 60:
                return f"{seconds:.1f} sec"

            if seconds < 3600:
                return f"{seconds / 60:.1f} min"

            if seconds < 86400:
                return f"{seconds / 3600:.1f} hr"

            if seconds < 31557600:
                return f"{seconds / 86400:.1f} days"

            years = (
                seconds / 31557600
            )

            if years < 1_000_000:
                return f"{years:.1f} years"

            return f"{years:.2e} years"

        time_cols = st.columns(2)

        with time_cols[0]:

            metric_card(
                "Estimated Cracking Time",
                format_duration(
                    expected_seconds
                ),
                "Theoretical average at 1B guesses/sec",
            )

        with time_cols[1]:

            wordlist_seconds = (
                WORDLIST_ENTRIES
                / 1_000_000_000
            )

            metric_card(
                "Project Wordlist Scan",
                format_duration(
                    wordlist_seconds
                ),
                f"{WORDLIST_ENTRIES:,} candidates "
                "at 1B guesses/sec",
            )

        st.markdown(
            """
            <div class="time-note">
                Estimated cracking time is a theoretical
                offline-attack estimate, not an actual crack.
                Actual results depend on the password-hashing
                algorithm, hardware, rate limits and attack strategy.
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ----------------------------------------------------
        # COMPLIANCE CHECKS
        # ----------------------------------------------------
        st.markdown(
            "### 📋 Compliance Checks"
        )

        checks = [
            (
                "Minimum length ≥ 8",
                length >= 8,
            ),
            (
                "Lowercase character",
                lower,
            ),
            (
                "Uppercase character",
                upper,
            ),
            (
                "Number",
                digit,
            ),
            (
                "Special character",
                special,
            ),
            (
                "No obvious common pattern",
                not predictable,
            ),
        ]

        for label, ok in checks:

            st.write(
                (
                    "✅ "
                    if ok
                    else "❌ "
                )
                + label
            )

        # ----------------------------------------------------
        # THREAT ANALYSIS
        # ----------------------------------------------------
        st.markdown(
            "### 🧠 Threat Analysis"
        )

        if predictable:

            st.warning(
                "Predictable/common credential patterns were detected. "
                "Use a unique passphrase or a high-entropy password."
            )

        else:

            st.success(
                "No listed common-pattern indicator was detected. "
                "Continue to prefer long, unique credentials and MFA."
            )


# ============================================================
# REPORT GENERATION
# ============================================================
elif page == "📑 Report Generation":

    section_header(
        "📑",
        "Report Generation",
        "Original project security assessment report.",
    )

    module_card(
        "📑",
        "Security Assessment & Audit Report",
        "The original PDF is kept unchanged for project "
        "documentation and HR review.",
    )

    if REPORT_FILE:

        st.success(
            "Original PDF found."
        )

        report_bytes = REPORT_FILE.read_bytes()

        st.markdown(
            "### 📄 Assessment Report Preview"
        )

        if hasattr(st, "pdf"):

            st.pdf(
                report_bytes
            )

        else:

            st.info(
                "Your Streamlit version does not support the "
                "embedded PDF preview yet. Use the download "
                "button below."
            )

        st.download_button(
            "⬇️ Download Original Project Report",
            data=report_bytes,
            file_name=REPORT_FILE.name,
            mime="application/pdf",
            use_container_width=True,
        )

    else:

        st.warning(
            "The original assessment PDF is not currently inside "
            "the GitHub repository. Upload the original project "
            "PDF into the repository, for example inside "
            "Report Generation/reports/, and the preview + "
            "download will appear automatically."
        )

        st.markdown(
            "### 📋 Assessment Report Overview"
        )

        st.info(
            "The report page is ready for the original PDF. "
            "It covers the documented Directory Generation, "
            "Linux and Windows Hash Extraction, controlled "
            "Brute-Force testing, Password Strength Analysis "
            "and project evidence. No replacement report is "
            "generated here; the original project report "
            "remains unchanged when you upload it."
        )

    st.markdown(
        """
        <div class="footer-note">
            Controlled Cybersecurity Testing •
            Authorized Laboratory Environment
        </div>
        """,
        unsafe_allow_html=True,
    )
