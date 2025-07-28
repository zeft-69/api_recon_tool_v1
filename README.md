# api_recon_tool_v1
# 🔍 API Recon Tool v1

A powerful Python-based tool for automating the reconnaissance and testing of insecure REST APIs.  
It supports multi-threading, endpoint wordlists, proxy/Tor routing, HTML reporting, and basic sensitive data exposure detection.

---

## 🧰 Tool Overview

This tool is designed to help penetration testers and bug bounty hunters identify misconfigured or vulnerable API endpoints by:

- Automating requests to known and discovered endpoints
- Detecting signs of sensitive data exposure (e.g., `password`, `token`)
- Generating structured reports and logging results clearly

### 🔑 Key Features

- 🔁 Multi-threaded endpoint scanning
- 📂 Wordlist-based endpoint fuzzing
- 🧪 Sensitive data exposure detection
- 💾 JSON response saving per endpoint
- 🧾 HTML reporting for clean output
- 📓 Logging with status codes and errors
- 🌐 Proxy and Tor routing support
- 📣 Verbose response preview option

---

## 🖥️ Usage

### 🧪 Basic scan with known endpoints

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -e listUsers listVehicles
```

### 📂 Use wordlist to fuzz endpoints

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -w endpoints.txt
```

### 🔁 Set number of concurrent threads

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -w endpoints.txt -t 10
```

### 🌐 Use with a proxy (e.g., Burp Suite)

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -w endpoints.txt --proxy http://127.0.0.1:8080
```

### 🧅 Route requests through Tor

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -w endpoints.txt --tor
```

### 📣 Enable verbose output

```bash
python api_recon_tool_v1.py -k YOUR_AUTH_KEY -e listUsers listVehicles -v
```

---

## 📁 Output Structure

- `output/`: JSON responses for each endpoint
- `scan_logs/`: Logs with status codes, errors, and timing
- `reports/report.html`: Interactive HTML report showing endpoint responses

---

## 🧠 Detection Logic

The tool flags potential vulnerabilities like:
- IDOR (Insecure Direct Object Reference)
- Authentication bypass
- Sensitive data returned without proper access control

Triggers include:
- Presence of `password`, `token`, `username`, `plate`, etc.

---

## ⚙️ Requirements

- Python 3.7+
- Required library:
  ```bash
  pip install requests
  ```

---

## 📦 Deliverables

- `api_recon_tool_v1.py`: Main script
- `README.md`: Tool documentation
- `endpoints.txt`: (optional) Wordlist for endpoint discovery

---



## 👨‍💻 Author

**Zeyad Am Elden**  
Junior Penetration Tester & Cybersecurity Researcher  
📫 [zeyadibrahemalmelden@gmail.com](mailto:zeyadibrahemalmelden@gmail.com)
