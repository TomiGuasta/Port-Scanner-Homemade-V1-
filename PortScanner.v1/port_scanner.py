#!/usr/bin/env python3
import os
import socket
import argparse
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from tabulate import tabulate
from colorama import Fore, Style, init

init()

# ================= CONFIG ==================

SCAN_MODES = {
    "fast": (1, 1024),
    "inter": (1, 5000),
    "full": (1, 65535)
}

BEHAVIOR_MODES = {
    "stealth": {"threads": 20, "delay": (0.1, 0.3)},
    "aggressive": {"threads": 500, "delay": (0, 0)},
    "audit": {"threads": 100, "delay": (0, 0)}
}

SERVICES = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    25: "SMTP",
    139: "NetBIOS",
    445: "SMB",
    3389: "RDP"
}

# Auto fix
os.system("./tools/auto-fix.sh > /dev/null 2>&1")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================= SCAN FUNCTION ==================

def scan_port(ip, port, delay):
    try:
        time.sleep(random.uniform(*delay))
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((ip, port))
        s.close()
        return port
    except:
        return None

# ================= SECURITY ANALYSIS ==================

def analyze(open_ports):
    alerts = []
    if 445 in open_ports:
        alerts.append("[CRITICAL] SMB exposed (445)")
    if 3389 in open_ports:
        alerts.append("[HIGH] RDP exposed (3389)")
    if 22 in open_ports:
        alerts.append("[MEDIUM] SSH open (22)")
    if 80 in open_ports or 443 in open_ports:
        alerts.append("[LOW] HTTP/HTTPS detected")
    return alerts

# ================= TEXT REPORT ==================

def save_report(filename, target, open_ports, alerts):
    with open(filename, "w") as f:
        f.write(f"PORT SCAN by Guasta\n")
        f.write(f"Target: {target}\n\n")

        f.write("OPEN PORTS:\n")
        for p in sorted(open_ports):
            f.write(f"{p} - {SERVICES.get(p,'UNKNOWN')}\n")

        f.write("\nSECURITY ALERTS:\n")
        if alerts:
            for a in alerts:
                f.write(a + "\n")
        else:
            f.write("No critical exposures detected.\n")

    print(Fore.GREEN + f"[+] TXT Report saved to {filename}" + Style.RESET_ALL)

# ================= HTML REPORT ==================

def generate_html_report(target, mode, open_ports):
    template_path = os.path.join(BASE_DIR, "templates", "report.html")

    if not os.path.exists(template_path):
        print(Fore.RED + "[!] HTML template NOT FOUND: templates/report.html" + Style.RESET_ALL)
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Build results table
    rows = ""
    for port in sorted(open_ports):
        service = SERVICES.get(port, "UNKNOWN")
        severity = "LOW"
        if port == 445:
            severity = "CRITICAL"
        elif port == 3389:
            severity = "HIGH"
        elif port == 22:
            severity = "MEDIUM"

        rows += f"<tr><td>{port}</td><td>OPEN</td><td>{service}</td><td class='{severity}'>{severity}</td></tr>\n"

    template = template.replace("{{TARGET}}", target)
    template = template.replace("{{MODE}}", mode)
    template = template.replace("{{DATE}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    template = template.replace("{{RESULTS}}", rows)

    output_file = os.path.join(BASE_DIR, "scan_report.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(template)

    print(Fore.GREEN + f"[+] HTML report generated: {output_file}" + Style.RESET_ALL)

# ================= MAIN ==================

def main():
    parser = argparse.ArgumentParser(description="Port Scan by Guasta")
    parser.add_argument("target", help="Target IP")
    parser.add_argument("--scan", choices=["fast", "inter", "full"], default="fast")
    parser.add_argument("--mode", choices=["stealth", "aggressive", "audit"], default="aggressive")
    parser.add_argument("--report", help="Save report (txt or html)")
    args = parser.parse_args()

    start, end = SCAN_MODES[args.scan]
    behavior = BEHAVIOR_MODES[args.mode]
    ports = range(start, end + 1)

    banner_color = Fore.CYAN if args.mode == "audit" else Fore.RED

    print(banner_color + """
╔══════════════════════════════════════╗
║        PORT SCAN by Guasta           ║
╚══════════════════════════════════════╝
""" + Style.RESET_ALL)

    print(f"[+] Target: {args.target}")
    print(f"[+] Scan range: {start}-{end}")
    print(f"[+] Mode: {args.mode.upper()}")
    print(f"[+] Threads: {behavior['threads']}")
    print("[+] Starting scan...\n")

    open_ports = []

    with ThreadPoolExecutor(max_workers=behavior["threads"]) as executor:
        futures = {executor.submit(scan_port, args.target, p, behavior["delay"]): p for p in ports}

        for future in tqdm(as_completed(futures), total=len(ports), desc="Scanning"):
            result = future.result()
            if result:
                open_ports.append(result)

    # TABLE OUTPUT
    table = []
    for port in sorted(open_ports):
        service = SERVICES.get(port, "UNKNOWN")
        table.append([port, "OPEN", service])

    print("\nPORT     STATE     SERVICE")
    print(tabulate(table, headers=["Port", "State", "Service"], tablefmt="plain"))

    print(f"\n[+] Open ports: {len(open_ports)}")
    print(f"[+] Closed ports: {len(ports) - len(open_ports)}")

    alerts = []
    if args.mode == "audit":
        print(Fore.YELLOW + "\n=== SECURITY ALERTS (AUDIT MODE) ===" + Style.RESET_ALL)
        alerts = analyze(open_ports)
        for a in alerts:
            print(a)

    # SAVE REPORT
    if args.report:
        if args.report.endswith(".html"):
            generate_html_report(args.target, args.mode, open_ports)
        else:
            save_report(args.report, args.target, open_ports, alerts)

    print(Fore.CYAN + "\nScan completed." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
