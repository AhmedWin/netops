"""Unit tests for health checker module."""
import sys
sys.path.insert(0, "scripts")
from health_checker import evaluate_health, HealthStatus


def test_healthy_device():
    result = evaluate_health("TEST-SW", "10.0.0.1", 30.0, 40.0, 100, 5)
    assert result.status == "healthy"
    assert len(result.alerts) == 0


def test_cpu_warning():
    result = evaluate_health("TEST-SW", "10.0.0.1", 75.0, 40.0, 100, 5)
    assert result.status == "warning"
    assert any("CPU" in a for a in result.alerts)


def test_critical_memory():
    result = evaluate_health("TEST-SW", "10.0.0.1", 30.0, 95.0, 100, 5)
    assert result.status == "critical"


def test_interface_errors():
    result = evaluate_health("TEST-SW", "10.0.0.1", 30.0, 40.0, 100, 200)
    assert result.status == "warning"
    assert any("interface" in a for a in result.alerts)


def test_multiple_issues():
    result = evaluate_health("TEST-SW", "10.0.0.1", 92.0, 91.0, 10, 500)
    assert result.status == "critical"
    assert len(result.alerts) >= 2
