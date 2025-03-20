
# 🕵️‍♂️ Watch Your Visitors  

### 👀 Who’s Watching You?  

At home, you carefully decide who to let in.  
On your computer? Not so much. Even on Linux, connections to servers you’ve never heard of are constantly being established. On other systems, things look even worse.  

It’s like walking through Caracas **1,000 times a day** – completely naked – just to peek into random windows. Except on a PC, no one even notices.  

And we’re not even talking about pros masking their tracks. This is just **regular internet browsing** – the **baby-shark pool** of cybersecurity.  

This affects **every** device. With tablets and smartphones, you’re basically at the mercy of whoever controls the servers.  
Search engines could warn their users and block shady servers… but that’s kinda hard when they’re hosted on compromised servers themselves.  


![Screenshot Watch-Your-Visitors](/doc/screenshot.png "Watch Your Visitors")

## 🚀 What Does *Watch Your Visitors* Do?  

This tool helps you **see who your computer is talking to** and checks if those connections are suspicious:  

✅ **Lists all active network connections**  
✅ **Checks IPs against [AbuseIPDB](https://www.abuseipdb.com/) for malicious activity**  
✅ **Shows country of origin and blacklist status**  
✅ **Runs in real-time with a live console view**  

## 🛠️ Installation  

### 1️⃣ Requirements  

- Python 3  
- Install dependencies:  

  ```bash
  pip install -r requirements.txt
  ```

  (Includes `psutil`, `rich`, `requests`)  

- **Optional:** Get an API key from [AbuseIPDB](https://www.abuseipdb.com/) for enhanced threat detection  

> Note: Watch the number of requests to AbuseIPDB, currently not optimized, could easily exhaust a free account

### 2️⃣ Run  

```bash
python watch_your_visitors.py --api YOUR_ABUSEIPDB_API_KEY
```

You can run it **without** an API key, but it will only display connections, without checking blacklists.  

## 🔒 How to Block Suspicious Connections  

### **1. Block an IP with `iptables`**  

To manually block an outgoing IP:  

```bash
sudo iptables -A OUTPUT -d 34.107.243.93 -j DROP
```

To list current firewall rules:  
```bash
sudo iptables -L -v -n --line-numbers
```

### **2. Use `ufw` (Simpler Alternative)**  

If you're using **`ufw` (Uncomplicated Firewall)**:  

```bash
sudo ufw deny out to 34.107.243.93
```

To remove the rule:  
```bash
sudo ufw delete deny out to 34.107.243.93
```

### **3. Automate Protection with `crowdsec`**  

`crowdsec` is a modern intrusion prevention system that can **detect and automatically block** suspicious IPs.  

Install on Debian/Ubuntu:  

```bash
curl -s https://packagecloud.io/install/repositories/crowdsec/crowdsec/script.deb.sh | sudo bash
sudo apt install crowdsec
```

CrowdSec pulls threat intelligence from a global network of users and applies **automatic countermeasures**.  

---

## 🎭 Final Thoughts  

We can’t stop the internet from being a shady back alley…  
But at least we can **turn on the lights**.  

This tool helps you **see** who your computer is chatting with. Whether you slam the door shut or invite them in for tea? That’s up to you. 🚪💭  

---

If you have suggestions or ideas, feel free to open an issue or a pull request! 🚀

---

## Legal Information

- This tool uses different libraries. Refer to their respective licenses for compliance.
- Ensure your use case complies with data protection regulations, particularly when handling sensitive or personal information.
- The authors provide no warranty and assume no liability for any issues arising from the use of this tool.

---
