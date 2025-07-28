import requests
import json
import argparse
import os
import threading
import time
from datetime import datetime

def save_response(endpoint, response):
    os.makedirs("output", exist_ok=True)
    filename = f"output/{endpoint}_output.json"
    try:
        with open(filename, "w") as f:
            f.write(json.dumps(response.json(), indent=2))
    except:
        with open(filename, "w") as f:
            f.write(response.text)

def append_to_html_report(endpoint, status_code, content):
    os.makedirs("reports", exist_ok=True)
    html_file = "reports/report.html"
    with open(html_file, "a") as f:
        f.write(f"<h3>Endpoint: {endpoint}</h3>")
        f.write(f"<p>Status: {status_code}</p>")
        f.write("<pre>")
        f.write(content.replace("<", "&lt;").replace(">", "&gt;"))
        f.write("</pre><hr>")

def scan_endpoint(auth_key, endpoint, headers, log_file, proxies, verbose=False):
    url = f"http://206.189.237.118/unsafe-script.php?action={endpoint}&authKey={auth_key}"
    start_time = time.time()
    try:
        r = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        duration = round(time.time() - start_time, 2)
        status = r.status_code
        response_preview = r.text[:200].replace("\n", " ")

        msg = f"[+] {endpoint}: {status} ({duration}s)"
        if verbose:
            msg += f" | Preview: {response_preview}"

        print(msg)
        with open(log_file, "a") as log:
            log.write(msg + "\n")

        save_response(endpoint, r)
        append_to_html_report(endpoint, status, r.text)

        if status == 200 and "password" in r.text.lower():
            with open(log_file, "a") as log:
                log.write(f"[!] Potential sensitive data leak on: {endpoint}\n")

    except requests.exceptions.RequestException as e:
        err_msg = f"[!] {endpoint} failed: {str(e)}"
        print(err_msg)
        with open(log_file, "a") as log:
            log.write(err_msg + "\n")

def main():
    parser = argparse.ArgumentParser(description="Zeyad's API Recon Tool v1")
    parser.add_argument("-k", "--authKey", required=True, help="Authorization key")
    parser.add_argument("-e", "--endpoints", nargs="+", help="List of endpoints to test")
    parser.add_argument("-w", "--wordlist", help="File with endpoint wordlist")
    parser.add_argument("-t", "--threads", type=int, default=5, help="Number of threads")
    parser.add_argument("--proxy", help="Proxy (http://127.0.0.1:8080)")
    parser.add_argument("--tor", action="store_true", help="Use Tor (SOCKS5)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    endpoints = args.endpoints or []
    if args.wordlist:
        with open(args.wordlist) as f:
            endpoints += [line.strip() for line in f if line.strip()]

    if not endpoints:
        print("[!] Provide endpoints with -e or -w.")
        return

    headers = {'User-Agent': 'ZReconBot/3.0'}
    proxies = {}
    if args.proxy:
        proxies = {"http": args.proxy, "https": args.proxy}
    elif args.tor:
        proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}

    os.makedirs("scan_logs", exist_ok=True)
    log_file = f"scan_logs/api_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

    with open("reports/report.html", "w") as html:
        html.write("<html><body><h1>API Recon Report</h1><hr>")

    threads = []
    for ep in endpoints:
        t = threading.Thread(target=scan_endpoint, args=(args.authKey, ep, headers, log_file, proxies, args.verbose))
        threads.append(t)
        t.start()
        if len(threads) >= args.threads:
            for t in threads:
                t.join()
            threads = []

    for t in threads:
        t.join()

    with open("reports/report.html", "a") as html:
        html.write("</body></html>")

    print(f"[✓] Scan finished. Logs: {log_file}, Report: reports/report.html")

if __name__ == "__main__":
    main()
