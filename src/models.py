from datetime import datetime

from pydantic import BaseModel


class ServiceStatus(BaseModel):
    """État des principaux services d'infrastructure."""
    database: str
    api_gateway: str
    cache: str


class Metric(BaseModel):
    "Valider les mesures de l'infrastructure."
    timestamp: datetime
    cpu_usage: int
    memory_usage: int
    latency_ms: int
    disk_usage: int
    network_in_kbps: int
    network_out_kbps: int
    io_wait: int
    thread_count: int
    active_connections: int
    error_rate: float
    uptime_seconds: int
    temperature_celsius: int
    power_consumption_watts: int
    service_status: ServiceStatus