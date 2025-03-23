import pytest
import subprocess
import time

def run_command(command):
    """Executes a shell command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def test_containers_running():
    """Tests if all required containers are running."""
    containers = ["grafana", "prometheus", "loki", "promtail"]
    running_containers = run_command("docker ps --format '{{.Names}}'").split("\n")

    for container in containers:
        found = any(container in name for name in running_containers)
        assert found, f"Container {container} is not running!"

def test_loki_ready():
    """Tests if Loki is ready."""
    for _ in range(10):  # Retry for up to 20 seconds
        response = run_command("curl -s http://localhost:3100/ready")
        if response == "ready":
            break
        time.sleep(2)
    assert response == "ready", f"Loki is not ready! Got: {response}"

def test_prometheus_ready():
    """Tests if Prometheus is ready."""
    response = run_command("curl -s http://localhost:9090/-/ready")
    assert "Prometheus" in response and "Ready" in response, "Prometheus is not ready!"

def test_grafana_ready():
    """Tests if Grafana is ready."""
    response = run_command("curl -s http://localhost:3000/api/health")
    assert '"database": "ok"' in response, "Grafana is not ready!"