import pytest
import subprocess

def run_command(command):
    """Executes a shell command and returns the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def test_containers_running():
    """Tests if all required containers are running."""
    containers = ["grafana", "prometheus", "loki", "promtail"]
    running_containers = run_command("docker ps --format '{{.Names}}'").split("\n")

    for container in containers:
        assert container in running_containers, f"Container {container} is not running!"

def test_loki_ready():
    """Tests if Loki is ready."""
    response = run_command("curl -s http://localhost:3100/ready")
    assert response == "ready", "Loki is not ready!"

def test_prometheus_ready():
    """Tests if Prometheus is ready."""
    response = run_command("curl -s http://localhost:9090/-/ready")
    assert response == "Prometheus Server is Ready.", "Prometheus is not ready!"

def test_grafana_ready():
    """Tests if Grafana is ready."""
    response = run_command("curl -s http://localhost:3000/api/health")
    assert '"database": "ok"' in response, "Grafana is not ready!"
