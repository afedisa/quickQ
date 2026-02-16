# Quick Start Guide

Quick guide to bring up and use the project with monitoring.

## 1. Initial Setup

```bash
# Clone repo (if not already done)
git clone <your-repo>
cd nest-api-microservices-rbmq

# Install dependencies
npm install

# Grant execute permission to scripts
chmod +x scripts/local-dev.sh
chmod +x scripts/verify-monitoring.sh
```

![Initial Setup](docs/images/quickstart-setup.png)

## 2. Start the Project

```bash
# Option 1: Automatic script (RECOMMENDED)
./scripts/local-dev.sh

# Option 2: Custom services
./scripts/local-dev.sh gateway auth users

# Option 3: Environment variable
SERVICES="gateway auth" ./scripts/local-dev.sh

# Option 4: Infrastructure only
docker-compose -f docker-compose-local.yml up -d
```

![Start Project](docs/images/quickstart-start.png)

## 3. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **API Swagger** | http://localhost:3000/document | - |
| **Grafana** | http://localhost:3001 | admin / admin123 |
| **Prometheus** | http://localhost:9090 | - |
| **Loki** | http://localhost:3100 | - |
| **cAdvisor** | http://localhost:8080 | - |
| **RabbitMQ** | http://localhost:15672 | admin / passw123 |

![Access Services](docs/images/quickstart-access.png)

## 4. Verify Everything Works

```bash
# Run verification script
./scripts/verify-monitoring.sh

# Or verify manually
curl http://localhost:3000/document       # Swagger
curl http://localhost:9090/-/healthy      # Prometheus
curl http://localhost:3001/api/health     # Grafana
curl http://localhost:3100/ready          # Loki
```

![Verification](docs/images/quickstart-verify.png)

## 5. First Steps in Grafana

1. Open http://localhost:3001
2. Login: `admin` / `admin123`
3. Go to "Data Sources"
4. Verify Prometheus and Loki are configured
5. Go to "Dashboards" to see available dashboards

![Grafana First Steps](docs/images/quickstart-grafana.png)

## 6. View Logs

### In Grafana (Recommended)

1. Open Grafana: http://localhost:3001
2. Go to "Explore"
3. Select "Loki" as data source
4. Run queries: `{service="gateway"}` or `{level="error"}`

### In Terminal

```bash
# Prometheus logs
docker-compose -f docker-compose-local.yml logs -f prometheus

# Gateway logs
docker-compose -f docker-compose-local.yml logs -f gateway

# Grafana logs
docker-compose -f docker-compose-local.yml logs -f grafana
```

![View Logs](docs/images/quickstart-logs.png)

## 7. View Metrics

### In Prometheus

1. Open http://localhost:9090
2. In "Graph", run queries:
   - `up{job="prometheus"}` - Service status
   - `container_cpu_usage_seconds_total` - CPU
   - `container_memory_usage_bytes` - Memory

### In cAdvisor

1. Open http://localhost:8080
2. Go to "Docker Containers"
3. Select a container to view metrics

![View Metrics](docs/images/quickstart-metrics.png)

## 8. Stop the Project

```bash
# Option 1: Ctrl+C in the script terminal

# Option 2: Stop containers
docker-compose -f docker-compose-local.yml down

# Option 3: Remove everything (WARNING - deletes data)
docker-compose -f docker-compose-local.yml down -v
```

![Stop Project](docs/images/quickstart-stop.png)

## Important Configuration

### Environment Variables

Edit `libs/common/src/env/.env`:

```env
GATEWAY_PORT=3000
RABBIT_MQ_URI=amqp://admin:passw123@localhost:5672
JWT_SECRET=your-secret
GRAFANA_ADMIN_PASSWORD=admin123
```

### Change Grafana Password

```bash
export GRAFANA_ADMIN_PASSWORD="my_secure_password"
docker-compose -f docker-compose-local.yml up -d grafana
```

![Configuration](docs/images/quickstart-config.png)

## Troubleshooting

### Port already in use

```bash
# Find the process using the port
lsof -i :3000

# Kill the process
kill -9 <PID>

# Or change the port in docker-compose-local.yml
```

### Containers do not start

```bash
# View detailed logs
docker-compose -f docker-compose-local.yml logs

# Rebuild images
docker-compose -f docker-compose-local.yml build --no-cache

# Nuclear option: clean everything
docker compose down -v
docker system prune -a
```

### Prometheus is not scraping services

1. Verify services are on the same network: `queue_network`
2. Check prometheus.yml has correct configurations
3. Open http://localhost:9090/targets to see status

### Loki is not receiving logs

1. Verify Promtail is running: `docker ps | grep promtail`
2. Verify containers have the label: `logging=promtail`
3. Check Promtail logs: `docker logs promtail`

![Troubleshooting](docs/images/quickstart-troubleshooting.png)

## Complete Documentation

- [README.md](README.md) - Project overview
- [MONITORING.md](MONITORING.md) - Monitoring guide
- [METRICS.md](METRICS.md) - Implement metrics in microservices
- [INTEGRATION_SUMMARY.md](INTEGRATION_SUMMARY.md) - Changes made

![Documentation](docs/images/quickstart-docs.png)

## Next Steps

1. Initial setup is complete
2. Implement metrics - see [METRICS.md](METRICS.md)
3. Create dashboards in Grafana
4. Configure alerts in Grafana
5. Integrate notifications (Slack, email, etc.)

![Next Steps](docs/images/quickstart-next-steps.png)

## Tips

- Use `./scripts/local-dev.sh gateway` for quick development
- Open http://localhost:3001 for all metrics
- Use Loki for quick log debugging
- Create per-microservice dashboards in Grafana
- Export dashboards as JSON for versioning

![Tips](docs/images/quickstart-tips.png)

---

Need help? See [MONITORING.md](MONITORING.md) or [METRICS.md](METRICS.md) for more details.
