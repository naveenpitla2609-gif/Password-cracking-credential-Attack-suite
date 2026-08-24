# ============================================================
# PASSWORD SECURITY AUDIT - PDF REPORT GENERATOR
# ============================================================
#
# Requirements:
#   - Terminal based module selection
#   - Select All
#   - Folder path for every module
#   - Professional PDF report
#   - Screenshots with Figure number + explanation
#   - Python source shown compactly
#   - Wordlists + logs
#   - Windows + Linux hash extraction
#   - Brute-Force Simulator
#   - Metric / Threat / Complex engines
#   - Report Generator as Module 5
#
# Install once:
#   pip install reportlab
#
# Run:
#   python report_generator.py
# ============================================================

from pathlib import Path
from datetime import datetime
import os
import textwrap

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
    Preformatted,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"

MODULES = {
    "1": "Directory Generation",
    "2": "Hash Extraction",
    "3": "Brute-Force Simulator",
    "4": "Password Strength Analyzer",
    "5": "Report Generator",
}

IMAGE_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".webp", ".bmp"
}

WORDLIST_EXTENSIONS = {
    ".txt", ".lst", ".dict", ".wordlist"
}

LOG_EXTENSIONS = {
    ".log"
}

IGNORED_FOLDERS = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "venv",
    ".venv",
    "env",
    "myenv",
    "reports",
}


# ============================================================
# PROFESSIONAL COLORS
# ============================================================

NAVY = colors.HexColor("#17202A")
CYAN = colors.HexColor("#00A6C7")
LIGHT_CYAN = colors.HexColor("#EAF8FB")
LIGHT_GREY = colors.HexColor("#F4F6F8")
MID_GREY = colors.HexColor("#D9DEE3")
DARK_GREY = colors.HexColor("#444444")
WHITE = colors.white
BLACK = colors.black


# ============================================================
# HELPERS
# ============================================================

def safe_read(path):
    try:
        return Path(path).read_text(
            encoding="utf-8",
            errors="replace"
        )
    except Exception as error:
        return f"[Unable to read file: {error}]"


def classify_file(path):
    suffix = path.suffix.lower()
    name = path.name.lower()

    if suffix in IMAGE_EXTENSIONS:
        return "screenshot"

    if suffix in WORDLIST_EXTENSIONS:
        return "wordlist"

    if suffix in LOG_EXTENSIONS or "log" in name:
        return "log"

    if suffix == ".py":
        return "python"

    return "other"


def scan_folder(folder):
    folder = Path(folder)

    result = {
        "screenshots": [],
        "python": [],
        "wordlists": [],
        "logs": [],
        "other": [],
    }

    for root, dirs, files in os.walk(folder):

        dirs[:] = [
            d for d in dirs
            if d.lower() not in IGNORED_FOLDERS
        ]

        root = Path(root)

        for filename in files:

            path = root / filename

            item = {
                "path": path,
                "name": path.name,
                "relative": path.relative_to(folder),
                "parent": root.name,
            }

            file_type = classify_file(path)

            if file_type == "screenshot":
                result["screenshots"].append(item)

            elif file_type == "python":
                result["python"].append(item)

            elif file_type == "wordlist":
                result["wordlists"].append(item)

            elif file_type == "log":
                result["logs"].append(item)

            else:
                result["other"].append(item)

    return result


def get_image_size(path):
    try:
        from PIL import Image as PILImage

        img = PILImage.open(path)

        return img.size

    except Exception:
        return None


# ============================================================
# PDF STYLES
# ============================================================

styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=25,
    leading=31,
    textColor=WHITE,
    alignment=TA_LEFT,
    spaceAfter=10,
)

SUBTITLE = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=12,
    leading=18,
    textColor=WHITE,
)

H1 = ParagraphStyle(
    "H1",
    parent=styles["Heading1"],
    fontName="Helvetica-Bold",
    fontSize=19,
    leading=24,
    textColor=NAVY,
    spaceBefore=12,
    spaceAfter=10,
)

H2 = ParagraphStyle(
    "H2",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=19,
    textColor=NAVY,
    spaceBefore=10,
    spaceAfter=7,
)

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10.5,
    leading=17,
    textColor=DARK_GREY,
    spaceAfter=8,
)

SMALL = ParagraphStyle(
    "Small",
    parent=BODY,
    fontSize=8.5,
    leading=12,
)

CAPTION = ParagraphStyle(
    "Caption",
    parent=BODY,
    fontName="Helvetica-Oblique",
    fontSize=9,
    leading=13,
    alignment=TA_CENTER,
    textColor=DARK_GREY,
)

CODE = ParagraphStyle(
    "Code",
    parent=BODY,
    fontName="Courier",
    fontSize=7.3,
    leading=9.5,
    textColor=BLACK,
)


# ============================================================
# PAGE HEADER / FOOTER
# ============================================================

def draw_header_footer(canvas, doc):

    canvas.saveState()

    width, height = A4

    # Header line
    if doc.page > 1:

        canvas.setStrokeColor(CYAN)
        canvas.setLineWidth(1)

        canvas.line(
            18 * mm,
            height - 14 * mm,
            width - 18 * mm,
            height - 14 * mm
        )

        canvas.setFont(
            "Helvetica-Bold",
            8
        )

        canvas.setFillColor(NAVY)

        canvas.drawString(
            18 * mm,
            height - 11 * mm,
            "PASSWORD SECURITY AUDIT REPORT"
        )

    # Footer
    canvas.setStrokeColor(MID_GREY)

    canvas.line(
        18 * mm,
        13 * mm,
        width - 18 * mm,
        13 * mm
    )

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.setFillColor(DARK_GREY)

    canvas.drawString(
        18 * mm,
        8 * mm,
        "Security Assessment • Controlled Testing Environment"
    )

    canvas.drawRightString(
        width - 18 * mm,
        8 * mm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ============================================================
# COVER PAGE
# ============================================================

def cover_page(story):

    width, height = A4

    data = [
        [
            Paragraph(
                "PASSWORD CRACKING &amp;<br/>"
                "CREDENTIAL ATTACK SUITE",
                TITLE
            )
        ],
        [
            Paragraph(
                "SECURITY ASSESSMENT &amp; AUDIT REPORT",
                SUBTITLE
            )
        ],
        [
            Paragraph(
                datetime.now().strftime(
                    "Generated: %d %B %Y"
                ),
                SUBTITLE
            )
        ],
    ]

    table = Table(
        data,
        colWidths=[170 * mm],
        rowHeights=[
            58 * mm,
            25 * mm,
            20 * mm,
        ],
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                NAVY
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                18 * mm
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                18 * mm
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                10 * mm
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8 * mm
            ),
        ])
    )

    story.append(Spacer(1, 42 * mm))
    story.append(table)

    story.append(Spacer(1, 18 * mm))

    project_box = Table(
        [[
            Paragraph(
                "<b>Assessment Type</b><br/>"
                "Controlled Cybersecurity Testing",
                BODY
            ),
            Paragraph(
                "<b>Environment</b><br/>"
                "Authorized Laboratory / Test Environment",
                BODY
            ),
        ]],
        colWidths=[
            82 * mm,
            82 * mm
        ],
    )

    project_box.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.6, MID_GREY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, MID_GREY),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    story.append(project_box)

    story.append(PageBreak())


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(number, title):

    return [
        Paragraph(
            f"{number}. {title}",
            H1
        ),
        HRFlowable(
            width="100%",
            thickness=1,
            color=CYAN,
            spaceAfter=12
        ),
    ]


# ============================================================
# MODULE OVERVIEW
# ============================================================

def module_overview_table(module_results):

    rows = [
        [
            Paragraph("<b>Module</b>", SMALL),
            Paragraph("<b>Evidence</b>", SMALL),
            Paragraph("<b>Python</b>", SMALL),
            Paragraph("<b>Wordlists</b>", SMALL),
            Paragraph("<b>Logs</b>", SMALL),
        ]
    ]

    for module_name, result in module_results.items():

        data = result["data"]

        rows.append([
            Paragraph(
                module_name,
                SMALL
            ),
            Paragraph(
                str(len(data["screenshots"])),
                SMALL
            ),
            Paragraph(
                str(len(data["python"])),
                SMALL
            ),
            Paragraph(
                str(len(data["wordlists"])),
                SMALL
            ),
            Paragraph(
                str(len(data["logs"])),
                SMALL
            ),
        ])

    table = Table(
        rows,
        colWidths=[
            75 * mm,
            23 * mm,
            23 * mm,
            25 * mm,
            23 * mm,
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                NAVY
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                WHITE
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                MID_GREY
            ),
            (
                "ROWBACKGROUNDS",
                (0, 1),
                (-1, -1),
                [WHITE, LIGHT_GREY]
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
        ])
    )

    return table


# ============================================================
# SCREENSHOT FIGURE
# ============================================================

def create_figure(
    image_path,
    figure_number,
    module_name
):

    try:

        img = Image(
            str(image_path)
        )

        max_width = 155 * mm
        max_height = 90 * mm

        width = img.imageWidth
        height = img.imageHeight

        ratio = min(
            max_width / width,
            max_height / height,
            1
        )

        img.drawWidth = width * ratio
        img.drawHeight = height * ratio

        caption = (
            f"<b>Figure {figure_number}.</b> "
            f"{module_name} — Evidence showing the "
            f"observed execution result / testing activity."
        )

        return KeepTogether([
            img,
            Spacer(1, 3 * mm),
            Paragraph(caption, CAPTION),
            Spacer(1, 7 * mm),
        ])

    except Exception as error:

        return Paragraph(
            f"Figure {figure_number}: "
            f"Unable to load image — {error}",
            BODY
        )


# ============================================================
# EVIDENCE SECTION
# ============================================================

def add_evidence(
    story,
    module_name,
    screenshots,
    start_number
):

    if not screenshots:

        story.append(
            Paragraph(
                "No screenshots were detected for this module.",
                BODY
            )
        )

        return start_number

    story.append(
        Paragraph(
            "Evidence",
            H2
        )
    )

    story.append(
        Paragraph(
            "The following figures document the actual "
            "execution, testing activity and observed results "
            "for this module.",
            BODY
        )
    )

    figure_number = start_number

    for item in screenshots:

        story.append(
            create_figure(
                item["path"],
                figure_number,
                module_name
            )
        )

        figure_number += 1

    return figure_number


# ============================================================
# PYTHON SOURCE SUMMARY
# ============================================================

def add_python_sources(
    story,
    module_name,
    python_files
):

    if not python_files:
        return

    story.append(
        Paragraph(
            "Python Source Evidence",
            H2
        )
    )

    story.append(
        Paragraph(
            "Complete source files are preserved in the project "
            "directory. The report presents a compact source "
            "summary rather than placing thousands of lines of "
            "code into the final document.",
            BODY
        )
    )

    for item in python_files:

        source = safe_read(item["path"])

        lines = source.splitlines()

        preview_lines = lines[:18]

        preview = "\n".join(
            preview_lines
        )

        if len(lines) > 18:

            preview += (
                "\n\n"
                "[Source continues in the original project file]"
            )

        block = [
            Paragraph(
                f"<b>{item['name']}</b>",
                H2
            ),
            Paragraph(
                f"Module: {module_name}<br/>"
                f"Path: {item['relative']}<br/>"
                f"Lines: {len(lines)}",
                SMALL
            ),
            Spacer(1, 2 * mm),
            Preformatted(
                preview,
                CODE
            ),
            Spacer(1, 5 * mm),
        ]

        story.append(
            KeepTogether(block)
        )


# ============================================================
# WORDLIST SUMMARY
# ============================================================

def add_wordlists(
    story,
    wordlists
):

    if not wordlists:
        return

    story.append(
        Paragraph(
            "Generated Wordlists",
            H2
        )
    )

    for item in wordlists:

        text = safe_read(item["path"])

        entries = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        preview = entries[:12]

        if len(entries) > 12:
            preview.append(
                "[Additional entries stored in original wordlist]"
            )

        story.append(
            Paragraph(
                f"<b>{item['name']}</b> — "
                f"{len(entries)} entries",
                BODY
            )
        )

        if preview:

            story.append(
                Preformatted(
                    "\n".join(preview),
                    CODE
                )
            )

        story.append(
            Spacer(1, 4 * mm)
        )


# ============================================================
# LOG SUMMARY
# ============================================================

def add_logs(
    story,
    logs
):

    if not logs:
        return

    story.append(
        Paragraph(
            "Generated Logs",
            H2
        )
    )

    for item in logs:

        text = safe_read(item["path"])

        lines = text.splitlines()

        preview = lines[:15]

        if len(lines) > 15:
            preview.append(
                "[Additional log entries stored in original log file]"
            )

        story.append(
            Paragraph(
                f"<b>{item['name']}</b> — "
                f"{len(lines)} log lines",
                BODY
            )
        )

        story.append(
            Preformatted(
                "\n".join(preview),
                CODE
            )
        )

        story.append(
            Spacer(1, 4 * mm)
        )


# ============================================================
# MODULE-SPECIFIC EXPLANATIONS
# ============================================================

MODULE_EXPLANATIONS = {

    "Directory Generation": {
        "purpose": (
            "Creates the required project directory structure "
            "and organizes generated security-testing artifacts."
        ),
        "process": (
            "The module was executed to create and validate the "
            "required directories used by the password security "
            "testing workflow."
        ),
        "observation": (
            "The generated directory structure was verified "
            "before subsequent modules were executed."
        ),
    },

    "Hash Extraction": {
        "purpose": (
            "Extracts password hashes from controlled Windows "
            "and Linux test environments for subsequent analysis."
        ),
        "process": (
            "Hash extraction was performed separately against "
            "Windows and Linux test environments. The extracted "
            "hash artifacts were then used for controlled "
            "password-recovery testing."
        ),
        "observation": (
            "Hashes were successfully obtained from the two "
            "controlled environments and password recovery was "
            "demonstrated within the authorized lab environment."
        ),
    },

    "Brute-Force Simulator": {
        "purpose": (
            "Demonstrates a controlled credential attack workflow "
            "using a Python-based simulator and an intentionally "
            "vulnerable web application."
        ),
        "process": (
            "A Python-based login interface was created for the "
            "simulation. Controlled authentication testing was "
            "also performed against OWASP Juice Shop using "
            "Burp Suite in an authorized environment."
        ),
        "observation": (
            "The simulator records request number, payload, "
            "status code and response timing. Successful "
            "authentication is identified within the controlled "
            "test sequence."
        ),
    },

    "Password Strength Analyzer": {
        "purpose": (
            "Evaluates password security characteristics and "
            "identifies weak or predictable password patterns."
        ),
        "process": (
            "Password analysis is performed using the Metric "
            "Engine, Threat Engine and Complex Engine."
        ),
        "observation": (
            "The three analysis engines provide complementary "
            "measurements covering password metrics, identified "
            "threat patterns and overall complexity."
        ),
    },

    "Report Generator": {
        "purpose": (
            "Consolidates project execution information, "
            "observations, source evidence and screenshots into "
            "a professional security assessment report."
        ),
        "process": (
            "The report generator scans the selected module "
            "directories, identifies supporting artifacts, "
            "organizes evidence and produces the final PDF."
        ),
        "observation": (
            "The resulting report provides a structured record "
            "of the testing methodology, module activities, "
            "observations and supporting evidence."
        ),
    },
}


# ============================================================
# MODULE SECTION
# ============================================================

def add_module(
    story,
    module_number,
    module_name,
    result,
    figure_number
):

    data = result["data"]

    story.extend(
        section_header(
            f"6.{module_number}",
            module_name
        )
    )

    explanation = MODULE_EXPLANATIONS.get(
        module_name,
        {}
    )

    # Module summary box
    summary = Table(
        [[
            Paragraph(
                f"<b>Module Purpose</b><br/>"
                f"{explanation.get('purpose', '')}",
                BODY
            )
        ]],
        colWidths=[165 * mm]
    )

    summary.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_CYAN),
            ("BOX", (0, 0), (-1, -1), 0.8, CYAN),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(summary)
    story.append(Spacer(1, 5 * mm))

    story.append(
        Paragraph(
            "Module Path",
            H2
        )
    )

    story.append(
        Paragraph(
            str(result["path"]),
            SMALL
        )
    )

    story.append(
        Paragraph(
            "Process / Commands / Observation",
            H2
        )
    )

    story.append(
        Paragraph(
            explanation.get("process", ""),
            BODY
        )
    )

    story.append(
        Paragraph(
            "<b>Observation:</b> "
            + explanation.get("observation", ""),
            BODY
        )
    )

    # Statistics
    stats = Table(
        [[
            Paragraph(
                f"<b>{len(data['screenshots'])}</b><br/>"
                "Screenshots",
                SMALL
            ),
            Paragraph(
                f"<b>{len(data['python'])}</b><br/>"
                "Python Files",
                SMALL
            ),
            Paragraph(
                f"<b>{len(data['wordlists'])}</b><br/>"
                "Wordlists",
                SMALL
            ),
            Paragraph(
                f"<b>{len(data['logs'])}</b><br/>"
                "Log Files",
                SMALL
            ),
        ]],
        colWidths=[
            40 * mm,
            40 * mm,
            40 * mm,
            40 * mm,
        ]
    )

    stats.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("BOX", (0, 0), (-1, -1), 0.5, MID_GREY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, MID_GREY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 9),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
        ])
    )

    story.append(stats)

    story.append(Spacer(1, 7 * mm))

    # Python
    add_python_sources(
        story,
        module_name,
        data["python"]
    )

    # Wordlists
    add_wordlists(
        story,
        data["wordlists"]
    )

    # Logs
    add_logs(
        story,
        data["logs"]
    )

    # Screenshots
    figure_number = add_evidence(
        story,
        module_name,
        data["screenshots"],
        figure_number
    )

    return figure_number


# ============================================================
# FINAL REPORT
# ============================================================

def generate_pdf(module_results):

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    pdf_path = (
        REPORT_DIR /
        f"Password_Security_Audit_Report_{timestamp}.pdf"
    )

    document = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        title="Password Security Audit Report",
        author="Security Assessment Project",
    )

    story = []

    # --------------------------------------------------------
    # COVER
    # --------------------------------------------------------

    cover_page(story)

    # --------------------------------------------------------
    # EXECUTIVE SUMMARY
    # --------------------------------------------------------

    story.extend(
        section_header(
            "1",
            "Executive Summary"
        )
    )

    story.append(
        Paragraph(
            "This report documents a controlled password "
            "security assessment performed using a modular "
            "Password Cracking & Credential Attack Suite.",
            BODY
        )
    )

    story.append(
        Paragraph(
            "The assessment covers directory generation, "
            "hash extraction, controlled brute-force simulation, "
            "password strength analysis and security report "
            "generation. Testing activities were performed "
            "against authorized laboratory environments.",
            BODY
        )
    )

    # --------------------------------------------------------
    # OBJECTIVES
    # --------------------------------------------------------

    story.extend(
        section_header(
            "2",
            "Project Objectives"
        )
    )

    objectives = [
        "Generate and organize password-security testing artifacts.",
        "Extract hashes from controlled Windows and Linux environments.",
        "Demonstrate controlled credential attack simulation.",
        "Evaluate password strength using multiple analysis engines.",
        "Collect screenshots, logs, wordlists and source evidence.",
        "Produce a professional security assessment report.",
    ]

    for item in objectives:

        story.append(
            Paragraph(
                "• " + item,
                BODY
            )
        )

    # --------------------------------------------------------
    # METHODOLOGY
    # --------------------------------------------------------

    story.extend(
        section_header(
            "3",
            "Assessment Methodology"
        )
    )

    methodology = Table(
        [[
            "01",
            "Directory\nGeneration"
        ], [
            "02",
            "Hash\nExtraction"
        ], [
            "03",
            "Brute-Force\nSimulator"
        ], [
            "04",
            "Password Strength\nAnalyzer"
        ], [
            "05",
            "Report\nGenerator"
        ]],
        colWidths=[
            32 * mm,
            32 * mm,
            32 * mm,
            32 * mm,
            32 * mm,
        ]
    )

    methodology.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GREY),
            ("TEXTCOLOR", (0, 0), (-1, -1), NAVY),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOX", (0, 0), (-1, -1), 0.6, MID_GREY),
            ("INNERGRID", (0, 0), (-1, -1), 0.4, MID_GREY),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    story.append(methodology)

    story.append(Spacer(1, 7 * mm))

    story.append(
        Paragraph(
            "Testing flow: Directory Generation → Hash Extraction "
            "→ Brute-Force Simulation → Password Strength Analysis "
            "→ Report Generation.",
            BODY
        )
    )

    # --------------------------------------------------------
    # SELECTED MODULES
    # --------------------------------------------------------

    story.extend(
        section_header(
            "4",
            "Selected Modules"
        )
    )

    story.append(
        module_overview_table(
            module_results
        )
    )

    # --------------------------------------------------------
    # PROJECT STRUCTURE
    # --------------------------------------------------------

    story.extend(
        section_header(
            "5",
            "Detected Project Structure"
        )
    )

    for module_name, result in module_results.items():

        story.append(
            Paragraph(
                f"<b>{module_name}</b>",
                H2
            )
        )

        story.append(
            Paragraph(
                str(result["path"]),
                SMALL
            )
        )

    # --------------------------------------------------------
    # MODULES
    # --------------------------------------------------------

    figure_number = 1

    for number, (module_name, result) in enumerate(
        module_results.items(),
        start=1
    ):

        figure_number = add_module(
            story,
            number,
            module_name,
            result,
            figure_number
        )

        story.append(
            PageBreak()
        )

    # --------------------------------------------------------
    # SECURITY RECOMMENDATIONS
    # --------------------------------------------------------

    story.extend(
        section_header(
            "7",
            "Security Recommendations"
        )
    )

    recommendations = [
        "Use strong and unique passwords.",
        "Implement authentication rate limiting.",
        "Use progressive delays after repeated failures.",
        "Enable multi-factor authentication.",
        "Use modern password hashing algorithms.",
        "Monitor repeated authentication failures.",
        "Avoid predictable password patterns.",
        "Perform security testing only with explicit authorization.",
    ]

    for item in recommendations:

        story.append(
            Paragraph(
                "• " + item,
                BODY
            )
        )

    # --------------------------------------------------------
    # CONCLUSION
    # --------------------------------------------------------

    story.extend(
        section_header(
            "8",
            "Conclusion"
        )
    )

    story.append(
        Paragraph(
            "The project demonstrates a structured approach to "
            "password and credential security assessment through "
            "controlled testing, evidence collection, analysis "
            "and professional reporting.",
            BODY
        )
    )

    story.append(
        Paragraph(
            "The collected evidence and observations provide a "
            "traceable record of the activities performed across "
            "the five project modules.",
            BODY
        )
    )

    # --------------------------------------------------------
    # FINAL NOTICE
    # --------------------------------------------------------

    story.append(Spacer(1, 10 * mm))

    notice = Table(
        [[
            Paragraph(
                "<b>Authorization Notice</b><br/>"
                "All testing activities documented in this report "
                "should be performed only against systems for "
                "which explicit authorization has been provided.",
                SMALL
            )
        ]],
        colWidths=[165 * mm]
    )

    notice.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_CYAN),
            ("BOX", (0, 0), (-1, -1), 0.7, CYAN),
            ("LEFTPADDING", (0, 0), (-1, -1), 10),
            ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ])
    )

    story.append(notice)

    # --------------------------------------------------------
    # BUILD
    # --------------------------------------------------------

    document.build(
        story,
        onFirstPage=draw_header_footer,
        onLaterPages=draw_header_footer
    )

    return pdf_path


# ============================================================
# TERMINAL MENU
# ============================================================

def show_menu():

    print()
    print("=" * 65)
    print("       PASSWORD SECURITY AUDIT REPORT GENERATOR")
    print("=" * 65)

    for key, name in MODULES.items():

        print(
            f"[{key}] {name}"
        )

    print("[A] Select All")
    print("[0] Exit")

    print("=" * 65)


def select_modules():

    show_menu()

    choice = input(
        "Enter module numbers (example: 1,2,3,4,5): "
    ).strip().lower()

    if choice == "0":
        return None

    if choice == "a":
        return list(MODULES.values())

    selected = []

    for number in choice.split(","):

        number = number.strip()

        if number in MODULES:

            selected.append(
                MODULES[number]
            )

    return selected


# ============================================================
# MAIN
# ============================================================

def main():

    selected_modules = select_modules()

    if not selected_modules:

        print(
            "\nNo modules selected."
        )

        return

    module_results = {}

    print()
    print("=" * 65)
    print("ENTER MODULE FOLDER PATHS")
    print("=" * 65)

    for module_name in selected_modules:

        print()
        print("-" * 65)
        print(f"MODULE: {module_name}")
        print("-" * 65)

        raw_path = input(
            "Enter module folder path: "
        ).strip()

        raw_path = (
            raw_path
            .strip('"')
            .strip("'")
        )

        module_path = Path(
            raw_path
        ).expanduser()

        if not module_path.exists():

            print(
                "✗ Folder not found. Module skipped."
            )

            continue

        if not module_path.is_dir():

            print(
                "✗ Path is not a folder. Module skipped."
            )

            continue

        print(
            "\nScanning..."
        )

        scan_data = scan_folder(
            module_path
        )

        print(
            f"  Screenshots : "
            f"{len(scan_data['screenshots'])}"
        )

        print(
            f"  Python      : "
            f"{len(scan_data['python'])}"
        )

        print(
            f"  Wordlists   : "
            f"{len(scan_data['wordlists'])}"
        )

        print(
            f"  Logs        : "
            f"{len(scan_data['logs'])}"
        )

        module_results[
            module_name
        ] = {
            "path": module_path,
            "data": scan_data,
        }

    if not module_results:

        print(
            "\nNo valid module folders were collected."
        )

        return

    print()
    print("=" * 65)
    print("GENERATING PROFESSIONAL PDF")
    print("=" * 65)

    try:

        pdf_path = generate_pdf(
            module_results
        )

    except Exception as error:

        print()
        print("✗ PDF GENERATION FAILED")
        print()
        print(error)

        return

    print()
    print("✓ PDF GENERATED SUCCESSFULLY")
    print()
    print("PDF:")
    print(pdf_path)
    print()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()