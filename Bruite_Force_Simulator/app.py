from flask import Flask, request, render_template_string
from datetime import datetime
from pathlib import Path
import time

app = Flask(__name__)

USERNAME = "admin"
PASSWORD = "Hacker123!"

# Server-side investigation log directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "authentication.log"


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Security Lab | Login</title>

    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            min-height: 100vh;
            background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }

        .login-container {
            width: 390px;
            padding: 35px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(15px);
        }

        .logo {
            width: 55px;
            height: 55px;
            margin: 0 auto 18px;
            border-radius: 14px;
            background: #2563eb;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 25px;
            font-weight: bold;
        }

        h1 {
            text-align: center;
            font-size: 25px;
            margin-bottom: 8px;
        }

        .subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 28px;
        }

        label {
            display: block;
            font-size: 13px;
            color: #cbd5e1;
            margin-bottom: 7px;
        }

        input {
            width: 100%;
            padding: 13px;
            margin-bottom: 18px;
            border-radius: 9px;
            border: 1px solid #334155;
            background: #0f172a;
            color: white;
            outline: none;
            font-size: 14px;
        }

        input:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.15);
        }

        button {
            width: 100%;
            padding: 13px;
            border: none;
            border-radius: 9px;
            background: #2563eb;
            color: white;
            font-size: 15px;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }

        .footer {
            text-align: center;
            margin-top: 22px;
            color: #64748b;
            font-size: 12px;
        }

        .toast {
            position: fixed;
            top: 25px;
            right: 25px;
            min-width: 300px;
            padding: 15px 18px;
            border-radius: 10px;
            background: #111827;
            border: 1px solid #334155;
            box-shadow: 0 10px 30px rgba(0,0,0,0.35);
            display: flex;
            align-items: center;
            gap: 12px;
            animation: slideIn 0.35s ease;
        }

        .toast.success {
            border-left: 4px solid #22c55e;
        }

        .toast.failed {
            border-left: 4px solid #ef4444;
        }

        .icon {
            font-size: 20px;
        }

        .toast-title {
            font-size: 14px;
            font-weight: bold;
        }

        .toast-message {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 3px;
        }

        @keyframes slideIn {
            from {
                transform: translateX(120%);
                opacity: 0;
            }

            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    </style>
</head>

<body>

    <div class="login-container">

        <div class="logo">S</div>

        <h1>Security Lab</h1>

        <p class="subtitle">
            Secure Authentication Portal
        </p>

        <form method="POST">

            <label>Username</label>

            <input
                type="text"
                name="username"
                placeholder="Enter username"
                required
            >

            <label>Password</label>

            <input
                type="password"
                name="password"
                placeholder="Enter password"
                required
            >

            <button type="submit">
                Sign In
            </button>

        </form>

        <div class="footer">
            Brute Force Simulator • Local Security Lab
        </div>

    </div>

    {% if status == "success" %}

    <div class="toast success" id="toast">

        <div class="icon">✓</div>

        <div>
            <div class="toast-title">
                Login Successful
            </div>

            <div class="toast-message">
                You have successfully logged in.
            </div>
        </div>

    </div>

    {% elif status == "failed" %}

    <div class="toast failed" id="toast">

        <div class="icon">✕</div>

        <div>
            <div class="toast-title">
                Login Failed
            </div>

            <div class="toast-message">
                Invalid username or password.
            </div>
        </div>

    </div>

    {% endif %}

    <script>
        const toast = document.getElementById("toast");

        if (toast) {
            setTimeout(() => {
                toast.style.transition = "0.4s";
                toast.style.transform = "translateX(120%)";
                toast.style.opacity = "0";

                setTimeout(() => {
                    toast.remove();
                }, 400);

            }, 3000);
        }
    </script>

</body>
</html>
"""


def write_authentication_log(
    username,
    status_code,
    response_time
):
    """
    Creates a server-side authentication event.
    Password values are intentionally NOT stored.
    """

    now = datetime.now()

    date = now.strftime("%Y-%m-%d")
    time_value = now.strftime("%H:%M:%S.%f")[:-3]

    source_ip = request.remote_addr or "UNKNOWN"
    method = request.method
    endpoint = request.path

    log_entry = (
        f"{date} {time_value} | "
        f"IP={source_ip} | "
        f"METHOD={method} | "
        f"ENDPOINT={endpoint} | "
        f"USERNAME={username} | "
        f"STATUS={status_code} | "
        f"RESPONSE_TIME={response_time:.3f}s\n"
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as log:
        log.write(log_entry)


@app.route("/", methods=["GET", "POST"])
def login():

    status = None

    if request.method == "POST":

        request_start = time.perf_counter()

        username = request.form.get("username", "")

        if username == USERNAME and request.form.get("password") == PASSWORD:
            status = "success"
            status_code = 200
        else:
            status = "failed"
            status_code = 401

        response_time = time.perf_counter() - request_start

        # Server-side investigation evidence
        write_authentication_log(
            username=username,
            status_code=status_code,
            response_time=response_time
        )

        return render_template_string(
            HTML,
            status=status
        ), status_code

    return render_template_string(
        HTML,
        status=status
    ), 200


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )