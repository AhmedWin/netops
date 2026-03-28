"""
VLAN Auditor — Cross-Switch VLAN Consistency Checker

Compares VLAN configurations across all switches in the inventory,
identifying mismatches, missing VLANs, and naming inconsistencies.
"""

import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class VlanEntry:
    vlan_id: int
    name: str
    status: str
    ports: list


def get_demo_vlan_data() -> dict[str, list[VlanEntry]]:
    """Simulated VLAN data from multiple switches."""
    return {
        "CORE-SW-01": [
            VlanEntry(1, "default", "active", ["Gi0/1"]),
            VlanEntry(10, "MGMT", "active", ["Gi0/2", "Gi0/3"]),
            VlanEntry(20, "SERVERS", "active", ["Gi0/4-8"]),
            VlanEntry(30, "USERS", "active", ["Gi0/9-24"]),
            VlanEntry(40, "VOIP", "active", ["Gi0/25-48"]),
            VlanEntry(100, "DMZ", "active", ["Gi1/1-4"]),
            VlanEntry(999, "NATIVE", "active", []),
        ],
        "CORE-SW-02": [
            VlanEntry(1, "default", "active", ["Gi0/1"]),
            VlanEntry(10, "MGMT", "active", ["Gi0/2", "Gi0/3"]),
            VlanEntry(20, "SERVERS", "active", ["Gi0/4-8"]),
            VlanEntry(30, "USERS", "active", ["Gi0/9-24"]),
            VlanEntry(40, "VOIP", "active", ["Gi0/25-48"]),
            VlanEntry(100, "DMZ", "active", ["Gi1/1-4"]),
            VlanEntry(999, "NATIVE", "active", []),
        ],
        "DIST-SW-BR01": [
            VlanEntry(1, "default", "active", ["Gi0/1"]),
            VlanEntry(10, "MANAGEMENT", "active", ["Gi0/2"]),  # Name mismatch!
            VlanEntry(20, "SERVERS", "active", ["Gi0/4-8"]),
            VlanEntry(30, "USERS", "active", ["Gi0/9-24"]),
            VlanEntry(40, "VOIP", "active", ["Gi0/25-48"]),
            # Missing VLAN 100 (DMZ)
            VlanEntry(999, "NATIVE", "active", []),
        ],
        "ACC-SW-FL3-01": [
            VlanEntry(1, "default", "active", ["Gi0/1"]),
            VlanEntry(10, "MGMT", "active", ["Gi0/2"]),
            VlanEntry(30, "USERS", "active", ["Gi0/9-24"]),
            VlanEntry(40, "VOIP", "active", ["Gi0/25-48"]),
            VlanEntry(50, "GUEST", "active", ["Gi0/3-8"]),  # Extra VLAN!
            # Missing VLAN 20, 100, 999
        ],
    }


def audit_vlans(vlan_data: dict[str, list[VlanEntry]]) -> dict:
    """Audit VLAN consistency across switches."""
    # Build a unified VLAN map
    all_vlans = {}
    for switch, vlans in vlan_data.items():
        for vlan in vlans:
            if vlan.vlan_id not in all_vlans:
                all_vlans[vlan.vlan_id] = {"name": vlan.name, "switches": {}}
            all_vlans[vlan.vlan_id]["switches"][switch] = vlan

    issues = []
    switch_names = list(vlan_data.keys())

    for vlan_id, info in sorted(all_vlans.items()):
        present_switches = set(info["switches"].keys())
        missing_switches = set(switch_names) - present_switches

        # Check for missing VLANs
        if missing_switches and len(present_switches) > 1:
            issues.append({
                "type": "MISSING",
                "severity": "warning",
                "vlan_id": vlan_id,
                "message": f"VLAN {vlan_id} ({info['name']}) missing on: {', '.join(sorted(missing_switches))}",
            })

        # Check for naming inconsistencies
        names = {sw: v.name for sw, v in info["switches"].items()}
        unique_names = set(names.values())
        if len(unique_names) > 1:
            issues.append({
                "type": "NAME_MISMATCH",
                "severity": "info",
                "vlan_id": vlan_id,
                "message": f"VLAN {vlan_id} naming inconsistency: {dict(names)}",
            })

        # Check for VLANs only on one switch (potential rogue)
        if len(present_switches) == 1:
            sw = list(present_switches)[0]
            issues.append({
                "type": "UNIQUE",
                "severity": "info",
                "vlan_id": vlan_id,
                "message": f"VLAN {vlan_id} ({info['name']}) only exists on {sw}",
            })

    return {
        "audit_time": datetime.now().isoformat(),
        "total_switches": len(switch_names),
        "total_vlans": len(all_vlans),
        "issues_found": len(issues),
        "issues": issues,
    }


def print_audit_report(report: dict) -> None:
    """Print formatted VLAN audit report."""
    print("\n" + "=" * 65)
    print(f"{'VLAN CONSISTENCY AUDIT':^65}")
    print(f"{report['audit_time'][:19]:^65}")
    print("=" * 65)
    print(f"Switches audited: {report['total_switches']}")
    print(f"Unique VLANs found: {report['total_vlans']}")
    print(f"Issues found: {report['issues_found']}")
    print("-" * 65)

    severity_icons = {"warning": "⚠️ ", "info": "ℹ️ ", "critical": "🔴"}

    for issue in report["issues"]:
        icon = severity_icons.get(issue["severity"], "❓")
        print(f"  {icon} [{issue['type']}] {issue['message']}")

    print("=" * 65)


if __name__ == "__main__":
    vlan_data = get_demo_vlan_data()
    report = audit_vlans(vlan_data)
    print_audit_report(report)
