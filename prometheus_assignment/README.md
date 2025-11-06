# Prometheus Monitoring Assignment

## 📝 Project Overview
This project sets up a complete monitoring system using Prometheus and Grafana.
It collects metrics from:
- Node Exporter —> System performance (CPU, memory, disk, etc.)
- Postgres Exporter —> Database performance
- Custom Exporter (Python) -> External API data (OpenWeather)
All metrics are visualized in Grafana dashboards with alerts and filters.

**Stack Used:**
- Docker & Docker Compose  
- Prometheus  
- Grafana  
- Node Exporter  
- Postgres Exporter  
- Python (`prometheus_client`) for custom exporters (optional)

---

## 📂 Folder Structure
```
prometheus_assignment/
├── docker-compose.yml
├── prometheus.yml
├── exporters/
│   ├── custom_exporter.py
│   └── Dockerfile
├── grafana_dashboards/
│   ├── node_exporter_dashboard.json
│   ├── database_exporter_dashboard.json
│   └── custom_exporter_dashboard.json
└── README.md
```
yaml
Copy code

---

## ⚙️ Setup Steps

### 1. Install Requirements
- **Docker & Docker Compose**: Verify with `docker run hello-world`  
- **Python + prometheus_client**: `pip install prometheus_client`  

### 2. Start Services
From project root:
```bash
docker-compose up -d --build
```
Check running containers:
```bash
docker ps
```
You should see:
```scss
Prometheus (9090)
Grafana (3000)
Node Exporter (9100)
Postgres Exporter (9187)
Custom Exporter (8000)
```
## Dashboards
Each dashboard visualizes 10 metrics with filter and alerts:
- **Node Exporter Dashboard** -> System Metrics
- **Database Dashboard** -> PostgreSQL performance
- **Customer Exporter Dashboard** -> Weather API Data
You can import  `.json` file from `dashboards/` into Grafana

## Alerts
Grafana alerts are configured:
- CPU usage > 90% for 5 minutes
- Database connection count too high
- Customer weather alert (high temp)

## How to Stop
```bash
docker-compose down
```



