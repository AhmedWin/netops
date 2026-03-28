"""
Compliance Scanner — Network Security Baseline Checker

Validates network device configurations against security baselines
aligned with CIS Cisco IOS Benchmarks and banking regulatory requirements.
"""

import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ComplianceRule:
    rule_id: str
    category: str
    description: str
    check_command: str
    expected_pattern: str
    severity: str  # critical, high, medium, low


@dataclass
class ComplianceResult:
    rule_id: str
    device: str
    description: str
    status: str  # pass, fail, error
    severity: str
    details: str


# Security baseline rules
BASELINE_RULES = [
    ComplianceRule("SEC-001", "Authentication", "SSH version 2 enabled", "show ip ssh", "version 2", "critical"),
    ComplianceRule("SEC-002", "Authentication", "Telnet disabled on VTY lines", "show run | section vty", "transport input ssh", "critical"),
    ComplianceRule("SEC-003", "Authentication", "Enable secret configured (not enable password)", "show run | include enable", "enable secret", "critical"),
    ComplianceRule("SEC-004", "Logging", "NTP server configured", "show run | include ntp server", "ntp server", "high"),
    ComplianceRule("SEC-005", "Logging", "Syslog server configured", "show run | include logging host", "logging host", "high"),
    ComplianceRule("SEC-006", "Logging", "Timestamps enabled for logging", "show run | include timestamps", "service timestamps log datetime", "medium"),
    ComplianceRule("SEC-007", "Access Control", "Standard ACL on VTY lines", "show run | section vty", "access-class", "high"),
    ComplianceRule("SEC-008", "Services", "CDP disabled on external interfaces", "show cdp", "CDP is not enabled", "medium"),
    ComplianceRule("SEC-009", "Services", "HTTP server disabled", "show run | include ip http server", "no ip http server", "high"),
    ComplianceRule("SEC-010", "Banner", "Login banner configured", "show run | include banner", "banner login", "medium"),
    ComplianceRule("SEC-011", "Encryption", "Password encryption enabled", "show run | include service password", "service password-encryption", "high"),
    ComplianceRule("SEC-012", "SNMP", "SNMPv3 configured (not v1/v2)", "show run | include snmp-server", "snmp-server group.*v3", "high"),
]


def run_demo_scan() -> list[ComplianceResult]:
    """Run demo compliance scan with simulated results."""
    demo_results = {
        "CORE-SW-01": {
            "SEC-001": ("pass", "SSH v2.0 enabled"),
            "SEC-002": ("pass", "Only SSH transport configured"),
            "SEC-003": ("pass", "Enable secret 5 configured"),
            "SEC-004": ("pass", "NTP server 10.0.1.100"),
            "SEC-005": ("pass", "Logging to 10.0.1.200"),
            "SEC-006": ("pass", "Timestamps enabled"),
            "SEC-007": ("pass", "ACL 10 applied to VTY"),
            "SEC-008": ("pass", "CDP disabled on Gi0/0"),
            "SEC-009": ("fail", "HTTP server still enabled"),
            "SEC-010": ("pass", "Login banner present"),
            "SEC-011": ("pass", "Password encryption on"),
            "SEC-012": ("fail", "SNMPv2c community 'public' found"),
        },
        "DIST-SW-BR01": {
            "SEC-001": ("pass", "SSH v2.0 enabled"),
            "SEC-002": ("fail", "Telnet still allowed on VTY 0 4"),
            "SEC-003": ("pass", "Enable secret configured"),
            "SEC-004": ("fail", "No NTP server configured"),
            "SEC-005": ("pass", "Logging to 10.0.1.200"),
            "SEC-006": ("fail", "Timestamps not configured"),
            "SEC-007": ("fail", "No ACL on VTY lines"),
            "SEC-008": ("pass", "CDP disabled"),
            "SEC-009": ("pass", "HTTP server disabled"),
            "SEC-010": ("fail", "No login banner"),
            "SEC-011": ("pass", "Password encryption on"),
            "SEC-012": ("pass", "SNMPv3 auth configured"),
        },
    }

    results = []
    for device, checks in demo_results.items():
        for rule in BASELINE_RULES:
            if rule.rule_id in checks:
                status, details = checks[rule.rule_id]
                results.append(ComplianceResult(
                    rule_id=rule.rule_id,
                    device=device,
                    description=rule.description,
                    status=status,
                    severity=rule.severity,
                    details=details,
                ))
    return results


def print_compliance_report(results: list[ComplianceResult]) -> None:
    """Print formatted compliance report."""
    print("\n" + "=" * 75)
    print(f"{'SECURITY COMPLIANCE REPORT':^75}")
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M'):^75}")
    print("=" * 75)

    devices = set(r.device for r in results)
    for device in sorted(devices):
        device_results = [r for r in results if r.device == device]
        passed = sum(1 for r in device_results if r.status == "pass")
        failed = sum(1 for r in device_results if r.status == "fail")
        score = (passed / len(device_results)) * 100 if device_results else 0

        print(f"\n📋 {device} — Score: {score:.0f}% ({passed}/{len(device_results)} passed)")
        print("-" * 75)

        for r in device_results:
            icon = "✅" if r.status == "pass" else "❌"
            sev = f"[{r.severity.upper()}]"
            print(f"  {icon} {r.rule_id} {sev:<10} {r.description}")
            if r.status == "fail":
                print(f"     └─ {r.details}")

    # Overall summary
    total_pass = sum(1 for r in results if r.status == "pass")
    total_fail = sum(1 for r in results if r.status == "fail")
    critical_fails = sum(1 for r in results if r.status == "fail" and r.severity == "critical")

    print(f"\n{'='*75}")
    print(f"SUMMARY: {total_pass} passed | {total_fail} failed | {critical_fails} critical failures")
    print(f"{'='*75}\n")


if __name__ == "__main__":
    results = run_demo_scan()
    print_compliance_report(results)
