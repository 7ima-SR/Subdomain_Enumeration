# 🔍 Subdomain Enumeration Tool

A lightweight and effective Python tool for discovering subdomains of a target domain using:
- ✅ **Passive Enumeration** via [crt.sh](https://crt.sh/)
- ✅ **Optional Brute-force Enumeration** with DNS resolution
- ✅ Parallel DNS resolution for speed
- ✅ Output as plain text and JSO

![Built With](https://img.shields.io/badge/Built%20With-Python-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)
![Author](https://img.shields.io/badge/Author-Hima-red?style=flat-square)

---

## 🚀 Features

- 🔎 Passive subdomain enumeration using Certificate Transparency logs (crt.sh)
- 🧠 Optional brute-force enumeration using custom wordlists
- ⚡ Fast DNS resolution using multi-threading
- 📄 Saves discovered subdomains to text and JSON formats

---

## 📦 Requirements

- Python 3.7+
- Required Libraries
-- requests
-- dnspython
-- pyfiglet
-- termcolor

- Install dependencies via:

```bash
pip install requests dnspython pyfiglet termcolor
```

---

## 🧠 Usage

```bash
python3 subenum.py <domain> [options]
```

- Basic Passive Enumeration

```bash
python3 subenum.py example.com
```

- With Brute-force Wordlist

```bash
python3 subenum.py example.com -w wordlist.tx
```

- Customize Threads and Output

```bash
python3 subenum.py example.com -w wordlist.txt -t 50 -o all_subs.txt --save-resolved results.json

```

---

## ✅ Arguments:

| Option              | Description                                                                 | Example                                 |
|---------------------|-----------------------------------------------------------------------------|-----------------------------------------|
| `domain`            | Target domain to enumerate subdomains (**required**)                        | `example.com`                           |
| `-w, --wordlist`    | Path to wordlist for brute-force subdomain enumeration                      | `-w wordlist.txt`                       |
| `-t, --threads`     | Number of threads for DNS resolution (**default: 20**)                      | `-t 50`                                 |
| `-o, --output`      | File to save all found subdomains (**default: subdomains.txt**)             | `-o found_subs.txt`                     |
| `--save-resolved`   | Output file to save resolved subdomains with IPs (**default: resolved.json**) | `--save-resolved output.json`         |

---

## 🔍 Example

```bash
python3 subenum.py example.com \
  -w wordlist.txt \
  -t 50 \
  -o all_subs.txt \
  --save-resolved resolved.json
```

---

## 📁 Output Files

- subdomains.txt (or custom output) – All discovered subdomains
- resolved.json – Resolved subdomains and their A records

---

## ⚠️ Disclaimer

- This tool is intended for educational purposes and authorized security testing only.
  Do NOT use it on domains you do not own or do not have permission to test.

---

## 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🚀 Advanced Version (For Educational & Testing Purposes Only)

> 🎓 A more powerful and extended version of this tool is available for **educational and experimentation purposes only**. It is not publicly released, but you can request access if you're interested.

### ✨ Key Features of the Advanced Version:

- 🔍 Multi-source **passive subdomain enumeration**: integrates `crt.sh`, `Wayback Machine`, `ThreatCrowd`, `SecurityTrails`, etc.
- 🧠 Basic **intelligence layer** to filter out false positives and duplicates
- 🛠️ Smart **brute-force engine** using domain-based logic and adaptive wordlists
- 🌍 Detection of subdomains behind **CDNs and cloud providers**
- 📡 Support for ASN-based or IP range subdomain targeting
- 📁 Export options: **CSV / JSON / TXT**
- 💬 Interactive CLI for better user control
- 🧪 Designed to be easily integrated into full **penetration testing pipelines**

### 📬 Interested in Access?

Feel free to contact me via GitHub messages or through the email provided in the profile.

> ⚠️ **Legal Notice:** This version is intended strictly for authorized testing, research, or learning purposes. Do not use it against targets without clear permission.

---

## 📧 Contact

- Made with ❤️ by 7ima-SR
- Website:https://ibrahim-elsaied.netlify.app/

