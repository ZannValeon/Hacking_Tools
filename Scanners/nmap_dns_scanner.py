#!/usr/bin/env python3
import subprocess
import nmap
import whois
import socket

def run_nmap(target):
    print(f"\n[*] Running Nmap on {target}...")
    nm = nmap.PortScanner()
    nm.scan(target, arguments='-T4 -F') # Fast scan
    for host in nm.all_hosts():
        print(f"Host: {host} ({nm[host].hostname()})")
        print("State:", nm[host].state())
        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            lport = nm[host][proto].keys()
            for port in sorted(lport):
                print(f"port: {port}\tstate : {nm[host][proto][port]['state']}")

def run_whois(domain):
    print(f"\n[*] WHOIS info for {domain}")
    try:
        w = whois.whois(domain)
        print(w.text)
    except Exception as e:
        print(f"WHOIS failed: {e}")

def run_dns_enum(domain):
    print(f"\n[*] DNS info for {domain}")
    try:
        addrs = socket.gethostbyname_ex(domain)
        print("Addresses:", addrs)
    except Exception as e:
        print(f"DNS lookup failed: {e}")

def main():
    target = input("Enter a domain or IP: ")
    if not target:
        print("No target given.")
        return
    
    run_nmap(target)
    if not target.replace('.', '').isdigit():
        run_whois(target)
        run_dns_enum(target)
    else:
        try:
            domain = socket.gethostbyaddr(target)[0]
            run_whois(domain)
            run_dns_enum(domain)
        except Exception:
            print("No reverse DNS found.")

if __name__ == "__main__":
    main()