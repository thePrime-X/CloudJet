# Prometheus Monitoring Assignment

## 📝 Project Overview
This project sets up a **Prometheus + Grafana monitoring system** to collect and visualize metrics from **Node Exporter** (system metrics) and **Postgres Exporter** (database metrics). Alerts are configured in Grafana for critical conditions.  

**Stack Used:**
- Docker & Docker Compose  
- Prometheus  
- Grafana  
- Node Exporter  
- Postgres Exporter  
- Python (`prometheus_client`) for custom exporters (optional)

---

## 📂 Folder Structure
prometheus_assignment/
├── docker-compose.yml
├── prometheus.yml
├── exporters/
│ └── custom_exporter.py
├── grafana_dashboards/
│ ├── node_exporter_dashboard.json
│ └── database_exporter_dashboard.json
└── README.md

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
docker-compose up -d
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
```
### 3. Access Grafana
Open: ```http://localhost:3000```

