#  NetOps Toolkit — Network Automation & Monitoring Suite

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Cisco](https://img.shields.io/badge/Cisco-IOS%20%7C%20NX--OS-1BA0D7?logo=cisco&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A Python-based network automation toolkit for enterprise environments. Built for network engineers managing Cisco infrastructure at scale — automates configuration backups, health checks, VLAN audits, and compliance reporting.

## Why This Project?

Managing 100+ network devices manually is error-prone and time-consuming. This toolkit automates repetitive tasks, reduces human error, and provides real-time visibility into network health — critical in banking and financial environments where uptime is non-negotiable.

## 📁 Project Structure

```
netops-toolkit/
├── scripts/
│   ├── config_backup.py        # Automated config backup via SSH
│   ├── health_checker.py       # Device health & interface monitor
│   ├── vlan_auditor.py         # VLAN consistency checker
│   ├── compliance_scanner.py   # Security baseline compliance
│   └── report_generator.py     # HTML/PDF report builder
├── configs/
│   ├── devices.yaml            # Device inventory
│   └── compliance_rules.yaml   # Security baselines
├── tests/
│   └── test_health_checker.py  # Unit tests
├── docs/
│   └── architecture.md         # System design overview
├── requirements.txt
├── .env.example
└── README.md
```

##  Features

| Feature | Description |
|---------|------------|
| **Config Backup** | SSH into devices, pull running configs, store with timestamps |
| **Health Monitor** | Check CPU, memory, interface errors, uptime across all devices |
| **VLAN Auditor** | Compare VLAN configs across switches, flag inconsistencies |
| **Compliance Scanner** | Verify devices meet security baselines (NTP, ACLs, SSH settings) |
| **Report Generator** | Generate HTML reports with charts for management review |

##  Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/netops-toolkit.git
cd netops-toolkit

# Install dependencies
pip install -r requirements.txt

# Configure your device inventory
cp .env.example .env
nano configs/devices.yaml

# Run a health check
python scripts/health_checker.py --inventory configs/devices.yaml

# Run VLAN audit
python scripts/vlan_auditor.py --output reports/

# Generate compliance report
python scripts/compliance_scanner.py --rules configs/compliance_rules.yaml
```

##  Tech Stack

- **Python 3.10+** — Core language
- **Netmiko** — SSH connections to network devices
- **Paramiko** — Low-level SSH transport
- **PyYAML** — Configuration management
- **Jinja2** — Report templating
- **Rich** — Terminal output formatting
- **Pytest** — Testing framework

##  Sample Output

```
╔══════════════════════════════════════════════════════════════╗
║                   NETWORK HEALTH REPORT                     ║
║                   2026-03-28 14:30 AST                      ║
╠══════════════════════════════════════════════════════════════╣
║ Device          │ CPU  │ Memory │ Uptime    │ Status        ║
║─────────────────┼──────┼────────┼───────────┼───────────────║
║ CORE-SW-01      │ 23%  │ 45%    │ 142 days  │ ✅ Healthy    ║
║ CORE-SW-02      │ 31%  │ 52%    │ 142 days  │ ✅ Healthy    ║
║ DIST-SW-BR01    │ 67%  │ 78%    │ 89 days   │ ⚠️  Warning   ║
║ ACC-SW-FL3-01   │ 12%  │ 33%    │ 201 days  │ ✅ Healthy    ║
║ FW-EDGE-01      │ 45%  │ 61%    │ 365 days  │ ✅ Healthy    ║
╚══════════════════════════════════════════════════════════════╝
  Total: 48 devices | Healthy: 45 | Warning: 2 | Critical: 1
```

##  Security Notes

- Credentials are stored in `.env` (never committed)
- All SSH connections use key-based auth when possible
- Compliance rules align with CIS Cisco IOS Benchmarks
- Designed for enterprise environments with RBAC considerations

##  License

feel free to use, modify, and distribute.

##  Contributing

Pull requests welcome! Please open an issue first to discuss proposed changes.

---

**Built with  by Ahmed Alghamdi** | [LinkedIn](https://linkedin.com/in/ahmed-alghamdi-w) | [GitHub](https://github.com/AhmedWin))
