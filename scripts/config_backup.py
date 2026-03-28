"""
Config Backup Module — Automated Network Configuration Backup

Connects to network devices via SSH, retrieves running configurations,
and stores them with timestamps for version tracking and disaster recovery.
"""

import os
import yaml
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
except ImportError:
    ConnectHandler = None

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class DeviceConfig:
    hostname: str
    ip: str
    device_type: str
    username: str
    password: str
    enable_secret: Optional[str] = None


def load_inventory(inventory_path: str) -> list[DeviceConfig]:
    """Load device inventory from YAML configuration file."""
    with open(inventory_path, "r") as f:
        data = yaml.safe_load(f)

    devices = []
    for device in data.get("devices", []):
        devices.append(DeviceConfig(
            hostname=device["hostname"],
            ip=device["ip"],
            device_type=device.get("device_type", "cisco_ios"),
            username=os.getenv("NET_USERNAME", device.get("username", "admin")),
            password=os.getenv("NET_PASSWORD", device.get("password", "")),
            enable_secret=os.getenv("NET_ENABLE", device.get("enable_secret")),
        ))
    return devices


def backup_device_config(device: DeviceConfig, backup_dir: str = "backups") -> dict:
    """
    Connect to a device and backup its running configuration.
    
    Returns:
        dict with keys: hostname, status, filepath, timestamp, error
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result = {
        "hostname": device.hostname,
        "status": "pending",
        "filepath": None,
        "timestamp": timestamp,
        "error": None,
    }

    # Create backup directory
    device_dir = Path(backup_dir) / device.hostname
    device_dir.mkdir(parents=True, exist_ok=True)

    if ConnectHandler is None:
        # Demo mode — simulate backup for portfolio demonstration
        logger.info(f"[DEMO] Simulating backup for {device.hostname} ({device.ip})")
        demo_config = f"""! Configuration for {device.hostname}
! Backed up: {timestamp}
! Device: {device.ip}
!
hostname {device.hostname}
!
interface GigabitEthernet0/0
 ip address {device.ip} 255.255.255.0
 no shutdown
!
line vty 0 4
 transport input ssh
 login local
!
end
"""
        filepath = device_dir / f"{device.hostname}_{timestamp}.cfg"
        filepath.write_text(demo_config)
        result["status"] = "success"
        result["filepath"] = str(filepath)
        logger.info(f"[DEMO] Config saved: {filepath}")
        return result

    try:
        logger.info(f"Connecting to {device.hostname} ({device.ip})...")
        connection_params = {
            "device_type": device.device_type,
            "host": device.ip,
            "username": device.username,
            "password": device.password,
            "timeout": 30,
        }
        if device.enable_secret:
            connection_params["secret"] = device.enable_secret

        with ConnectHandler(**connection_params) as conn:
            if device.enable_secret:
                conn.enable()

            config = conn.send_command("show running-config")
            filepath = device_dir / f"{device.hostname}_{timestamp}.cfg"
            filepath.write_text(config)

            result["status"] = "success"
            result["filepath"] = str(filepath)
            logger.info(f"✅ Backup saved: {filepath}")

    except NetmikoTimeoutException:
        result["status"] = "failed"
        result["error"] = "Connection timed out"
        logger.error(f"❌ Timeout: {device.hostname}")
    except NetmikoAuthenticationException:
        result["status"] = "failed"
        result["error"] = "Authentication failed"
        logger.error(f"❌ Auth failed: {device.hostname}")
    except Exception as e:
        result["status"] = "failed"
        result["error"] = str(e)
        logger.error(f"❌ Error on {device.hostname}: {e}")

    return result


def run_backup(inventory_path: str, backup_dir: str = "backups") -> list[dict]:
    """Run backup across all devices in inventory."""
    devices = load_inventory(inventory_path)
    logger.info(f"Starting backup for {len(devices)} devices...")

    results = []
    for device in devices:
        result = backup_device_config(device, backup_dir)
        results.append(result)

    # Summary
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    logger.info(f"\n{'='*50}")
    logger.info(f"Backup Complete: {success} success, {failed} failed, {len(results)} total")
    logger.info(f"{'='*50}")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Network Configuration Backup Tool")
    parser.add_argument("--inventory", default="configs/devices.yaml", help="Device inventory file")
    parser.add_argument("--output", default="backups", help="Backup output directory")
    args = parser.parse_args()

    run_backup(args.inventory, args.output)
