"""
Health Checker Module — Network Device Health Monitoring
"""

import sys
import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

# Fix Unicode output on Windows terminals (Git Bash, CMD, PowerShell)
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class DeviceHealth:
    hostname: str
    ip: str
    cpu_percent: float
    memory_percent: float
    uptime_days: int
    interface_errors: int
    status: str
    checked_at: str
    alerts: list


CPU_WARNING = 70
CPU_CRITICAL = 90
MEM_WARNING = 75
MEM_CRITICAL = 90
INTF_ERROR_THRESHOLD = 100


def evaluate_health(hostname: str, ip: str, cpu: float, memory: float,
                    uptime: int, intf_errors: int) -> DeviceHealth:
    alerts = []
    status = HealthStatus.HEALTHY

    if cpu >= CPU_CRITICAL:
        alerts.append(f"CRITICAL: CPU at {cpu}%")
        status = HealthStatus.CRITICAL
    elif cpu >= CPU_WARNING:
        alerts.append(f"WARNING: CPU at {cpu}%")
        if status != HealthStatus.CRITICAL:
            status = HealthStatus.WARNING

    if memory >= MEM_CRITICAL:
        alerts.append(f"CRITICAL: Memory at {memory}%")
        status = HealthStatus.CRITICAL
    elif memory >= MEM_WARNING:
        alerts.append(f"WARNING: Memory at {memory}%")
        if status != HealthStatus.CRITICAL:
            status = HealthStatus.WARNING

    if intf_errors > INTF_ERROR_THRESHOLD:
        alerts.append(f"WARNING: {intf_errors} interface errors detected")
        if status == HealthStatus.HEALTHY:
            status = HealthStatus.WARNING

    return DeviceHealth(
        hostname=hostname, ip=ip, cpu_percent=cpu, memory_percent=memory,
        uptime_days=uptime, interface_errors=intf_errors,
        status=status.value, checked_at=datetime.now().isoformat(), alerts=alerts,
    )


def run_health_check_demo() -> list:
    demo_devices = [
        ("CORE-SW-01", "10.0.1.1", 23.4, 45.2, 142, 3),
        ("CORE-SW-02", "10.0.1.2", 31.0, 52.1, 142, 12),
        ("DIST-SW-BR01", "10.0.2.1", 67.8, 78.3, 89, 45),
        ("DIST-SW-BR02", "10.0.2.2", 42.1, 55.7, 89, 8),
        ("ACC-SW-FL1-01", "10.0.3.1", 12.3, 33.4, 201, 0),
        ("ACC-SW-FL2-01", "10.0.3.2", 15.7, 38.9, 201, 2),
        ("ACC-SW-FL3-01", "10.0.3.3", 88.2, 82.1, 45, 156),
        ("FW-EDGE-01", "10.0.0.1", 45.6, 61.3, 365, 22),
        ("FW-EDGE-02", "10.0.0.2", 43.2, 59.8, 365, 18),
        ("WLC-01", "10.0.4.1", 55.1, 67.4, 120, 5),
    ]
    return [evaluate_health(*d) for d in demo_devices]


def print_report(results: list) -> None:
    # ASCII fallback icons for Windows terminals that don't support Unicode emojis
    icons = {"healthy": "[OK]     ", "warning": "[WARN]   ", "critical": "[CRIT]   ", "unknown": "[???]    "}
    print("\n" + "=" * 72)
    print(f"{'NETWORK HEALTH REPORT':^72}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M AST'):^72}")
    print("=" * 72)
    print(f"{'Device':<18} {'CPU':>5} {'Mem':>5} {'Uptime':>10} {'Errors':>7} {'Status':<10}")
    print("-" * 72)
    for r in results:
        icon = icons.get(r.status, "❓")
        print(f"{r.hostname:<18} {r.cpu_percent:>4.0f}% {r.memory_percent:>4.0f}%"
              f" {r.uptime_days:>7}d   {r.interface_errors:>5}  {icon} {r.status}")
    print("-" * 72)
    h = sum(1 for r in results if r.status == "healthy")
    w = sum(1 for r in results if r.status == "warning")
    c = sum(1 for r in results if r.status == "critical")
    print(f"Total: {len(results)} devices | [OK] {h} Healthy | [WARN] {w} Warning | [CRIT] {c} Critical")
    print("=" * 72)
    alerts = [(r.hostname, a) for r in results for a in r.alerts]
    if alerts:
        print(f"\n{'ALERTS':^72}")
        print("-" * 72)
        for hostname, alert in alerts:
            print(f"  [{hostname}] {alert}")
        print()


def export_json(results: list, filepath: str = "reports/health_report.json") -> None:
    from pathlib import Path
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    data = {
        "report_time": datetime.now().isoformat(),
        "total_devices": len(results),
        "summary": {
            "healthy": sum(1 for r in results if r.status == "healthy"),
            "warning": sum(1 for r in results if r.status == "warning"),
            "critical": sum(1 for r in results if r.status == "critical"),
        },
        "devices": [asdict(r) for r in results],
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Report exported: {filepath}")


if __name__ == "__main__":
    results = run_health_check_demo()
    print_report(results)
    export_json(results)
