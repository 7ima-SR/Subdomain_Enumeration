"""
Simple Subdomain Enumeration tool
- passive: crt.sh (Certificate Transparency)
- optional: brute-force from wordlist
- resolves found names to A records
"""

import requests
import argparse
import json
import dns.resolver
import concurrent.futures
import time
from typing import List, Set
import termcolor
import pyfiglet


print(termcolor.colored(pyfiglet.figlet_format("Subdomain Enumeration"), "red"))
print(termcolor.colored("Powered by Hima", "yellow"))

# ---------- crt.sh passive enumeration ----------
def fetch_subdomains_form_crtsh(domain:str, timeout=30)-> List[str]:
    """
    Query crt.sh for subdomains.
    Uses: https://crt.sh/?q=%.example.com&output=json
    """

    url = "https://crt.sh/"
    params = {
        "q": f"%.{domain}",
        "output": "json"
    }

    try:
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] crt.sh fetch error: {e}")
        return []
    
    subs = set()
    for entry in data:
        name = entry.get("name_value", "")
        for n in name.splitlines():
            n = n.strip()
            if not n:
                continue
            if n.startswith("*."):
                n = n[2:]
            if n.endswith(domain) or n == domain:
                subs.add(n)
    
    return sorted(subs)

# ---------- DNS resolver ----------
resolver = dns.resolver.Resolver()
resolver.timeout = 5
resolver.lifetime = 5

def resolve_subdomain(host: str) -> List[str]:
    """Resolve A records for a given host. Returns list of IPs or empty."""
    try:
        answers = resolver.resolve(host, "A")
        return [rdata.to_text() for rdata in answers]
    except Exception:
        return []

# ---------- Brute-force enumeration ----------
def brute_force_subdomains(domain: str, words: List[str], threads: int = 20) -> Set[str]:
    """
    Try words as prefixes (word.domain) and return those that resolve.
    """

    candidates = [f"{w.strip()}.{domain}" for w in words if w.strip()]
    found = set()

    def check(host):
        ips = resolve_subdomain(host)
        if ips:
            return host
        return None
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(check, h): h for h in candidates}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                found.add(res)
    return found


# ---------- Utilities ----------
def save_list(filename: str, items: List[str]):
    """Save a list of items to a file, one per line."""

    with open(filename, "w") as f:
        for item in items:
            f.write(f"{item}\n")

# ---------- CLI ----------
def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration Tool")
    parser.add_argument("domain", help="Domain to enumerate subdomains for")
    parser.add_argument("-w", "--wordlist", help="Path to wordlist for brute-force")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Threads for brute-force/resolution")
    parser.add_argument("-o", "--output", help="Output file to save results" , default="subdomains.txt")
    parser.add_argument("--save-resolved", default="resolved.json", help="Save resolved JSON (host -> [ips])")
    args = parser.parse_args()

    domain = args.domain.strip().lower()
    print(f"[+] Enumerating subdomains for: {domain}")

    print("[*] Querying crt.sh ...")
    crt_subs = fetch_subdomains_form_crtsh(domain)
    print(f"[+] crt.sh returned {len(crt_subs)} unique names")

    brutefound = set()
    if args.wordlist:
        print("[*] Running brute-force using wordlist:", args.wordlist)
        try:
            with open(args.wordlist, "r") as f:
                words = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        except Exception as e:
            print(f"[!] Could not read wordlist: {e}")
            words = []
        
        if words:
            brutefound = brute_force_subdomains(domain, words, threads=args.threads)
            print(f"[+] Brute-force discovered {len(brutefound)} resolving names")
        
    
    all_subs = sorted(set(crt_subs) | brutefound)
    print(f"[*] Total candidate subdomains: {len(all_subs)}")
    print("[*] Resolving A records (parallel)...")
    resolved = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(resolve_subdomain, s): s for s in all_subs}
        print("[*] Waiting for resolution results...")
        for future in concurrent.futures.as_completed(futures):
            host = futures[future]
            ips = future.result()
            if ips:
                resolved[host] = ips
                print(f"    [+] {host} -> {', '.join(ips)}")

    print(f"[+] {len(resolved)} hosts resolved to A records")

    # Save outputs
    save_list(args.output, sorted(all_subs))
    with open(args.save_resolved, "w") as f:
        json.dump(resolved, f, indent=2)

    print(f"[+] Saved candidates to {args.output}")
    print(f"[+] Saved resolved results to {args.save_resolved}")
    print("[+] Done.")


if __name__ == "__main__":
    main()
