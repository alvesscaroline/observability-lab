import pytest
import requests

LOKI_URL = "http://localhost:3100"
PROMETHEUS_URL = "http://localhost:9090"
GRAFANA_URL = "http://localhost:3000"

def test_loki_api():
    """Checks if the Loki API responds correctly."""
    response = requests.get(f"{LOKI_URL}/loki/api/v1/labels")
    assert response.status_code == 200, f"Loki API failed! {response.text}"

def test_prometheus_api():
    """Checks if the Prometheus API responds correctly."""
    response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={"query": "up"})
    assert response.status_code == 200, f"Prometheus API failed! {response.text}"
    data = response.json()
    assert data["status"] == "success", "Invalid response from Prometheus!"

def test_grafana_api():
    """Checks if the Grafana API responds correctly."""
    response = requests.get(f"{GRAFANA_URL}/api/health")
    assert response.status_code == 200, f"Grafana API failed! {response.text}"
    assert response.json().get("database") == "ok", "Grafana is not connected to the database!"
