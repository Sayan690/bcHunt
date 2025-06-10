# bcHunt - An Autonomous Badchar Finder

**bcHunt** is a Python tool that automates the process of detecting bad characters in exploit development. Given a memory dump (usually from the ESP register after a stack overflow), it compares the memory content against a standard byte sequence and flags any discrepancies. It then regenerates the payload with the bad character(s) removed, helping streamline shellcode development.

---

## 🚀 Features

- Detects the exact byte where the payload breaks.
- Flags the bad character causing the interruption.
- Regenerates a new payload excluding the bad characters.
- Supports excluding custom known bad characters with the `-b` flag.

---

## 🧠 How It Works

After triggering a buffer overflow, the content of the ESP register is dumped into a binary file (e.g., `seq.bin`). This file contains the byte sequence injected into the process. `bcHunt` compares this with a complete byte sequence (`\x01` to `\xff`) and detects where the sequence diverges, indicating a bad character.

---

## 📦 Installation

Just clone the repository:

```bash
git clone https://github.com/Sayan690/bcHunt
cd bcHunt
```

Python 3 is required to run this tool.

---
## ⚙️ Usage

```bash
bcHunt.py <sequence file> -b [badchars]
```

- `<sequence file>`: Binary file (e.g., `seq.bin`) containing the memory dump of the ESP register.
    
- `-b <badchars>` _(optional)_: A string of known bad characters to exclude (e.g., `"\x00\x0a"`).

---
## 🧪 Example

Input:
```bash
python3 bcHunt.py seq.bin
```

Output:
```
[*] Badchar found: \x0a
[*] Removing it ...
[+] New payload :
\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d ... \xff
```

Run it again with the badchar excluded:

```bash
python3 bcHunt.py a.bin -b "\x0a"
```

Output:
```
[+] No Badchars found!!
```

---
## 🔄 Workflow

- Generate a payload of all possible combinations of characters from '\x01' to '\xff'.
    
- Inject it via buffer overflow.
    
- Dump the ESP register to a binary file.
    
- Run `bcHunt.py` on the dump.
    
- Get the filtered payload without bad characters.
    
- Repeat until no badchars are found.

---
## 🧰 Use Case

Ideal for penetration testers, exploit developers, or CTF players looking to quickly and reliably identify bad characters during shellcode crafting.

---
## 📄 License

This project is licensed under the MIT License. See [LICENSE](https://github.com/Sayan690/bcHunt/blob/main/LICENSE) for more info.
