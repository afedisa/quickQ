from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path("/Volumes/TOSHIBA EXT/Desarrollo/quickQ/docs/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1600, 900
BG = "#F7F9FC"
BLUE = "#2F6FED"
GREEN = "#2BB673"
GRAY = "#5B6770"
LIGHT_GRAY = "#D7DEE6"
DARK = "#1F2A37"


def load_font(size: int):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def new_canvas(title: str):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    title_font = load_font(36)
    draw.text((60, 40), title, fill=DARK, font=title_font)
    draw.line((60, 90, W - 60, 90), fill=LIGHT_GRAY, width=2)
    return img, draw


def box(draw, xy, label, fill="#FFFFFF", outline=LIGHT_GRAY, text_fill=DARK, radius=16):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=2)
    font = load_font(22)
    bbox = draw.textbbox((0, 0), label, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((x1 + (x2 - x1 - w) / 2, y1 + (y2 - y1 - h) / 2), label, fill=text_fill, font=font)


def arrow(draw, start, end, color=GRAY, width=3):
    draw.line([start, end], fill=color, width=width)
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    size = 10
    left = (ex - ux * size - uy * size / 2, ey - uy * size + ux * size / 2)
    right = (ex - ux * size + uy * size / 2, ey - uy * size - ux * size / 2)
    draw.polygon([end, left, right], fill=color)


def label(draw, pos, text, color=GRAY, size=18):
    font = load_font(size)
    draw.text(pos, text, fill=color, font=font)


def generate_description():
    img, draw = new_canvas("System Overview")
    box(draw, (80, 170, 360, 260), "Web App")
    box(draw, (80, 300, 360, 390), "Kiosk")
    box(draw, (80, 430, 360, 520), "Screen Display")
    box(draw, (520, 290, 820, 390), "API Gateway", fill="#E8F0FF", outline=BLUE)
    box(draw, (980, 190, 1280, 270), "Auth")
    box(draw, (980, 290, 1280, 370), "Users")
    box(draw, (980, 390, 1280, 470), "Queues")
    box(draw, (980, 490, 1280, 570), "Turns")
    box(draw, (980, 590, 1280, 670), "Notifications")
    box(draw, (520, 520, 820, 610), "RabbitMQ", fill="#EAF7F1", outline=GREEN)
    box(draw, (520, 670, 820, 760), "MariaDB", fill="#F0F3F7")
    box(draw, (1240, 700, 1520, 780), "Prometheus")
    box(draw, (1240, 790, 1520, 870), "Grafana & Loki")

    for y in (215, 345, 475):
        arrow(draw, (360, y), (520, 340))

    arrow(draw, (670, 390), (670, 520))
    arrow(draw, (670, 610), (670, 670))
    for y in (230, 330, 430, 530, 630):
        arrow(draw, (820, 340), (980, y))
    arrow(draw, (1140, 570), (1240, 740))
    arrow(draw, (1140, 570), (1240, 830))

    img.save(OUT_DIR / "readme-description.png")


def generate_architecture():
    img, draw = new_canvas("Microservices Architecture")
    box(draw, (630, 220, 970, 320), "API Gateway", fill="#E8F0FF", outline=BLUE)
    box(draw, (630, 520, 970, 600), "RabbitMQ", fill="#EAF7F1", outline=GREEN)
    box(draw, (630, 680, 970, 760), "MariaDB", fill="#F0F3F7")
    services = ["Auth", "Users", "Organizations", "Establishments", "Queues", "Turns", "Notifications"]
    positions = [
        (120, 160, 420, 240),
        (120, 270, 420, 350),
        (120, 380, 420, 460),
        (1180, 160, 1480, 240),
        (1180, 270, 1480, 350),
        (1180, 380, 1480, 460),
        (1180, 490, 1480, 570),
    ]
    for svc, pos in zip(services, positions):
        box(draw, pos, svc)

    for pos in positions:
        if pos[0] < 600:
            arrow(draw, (pos[2], (pos[1] + pos[3]) / 2), (630, 270))
        else:
            arrow(draw, (970, 270), (pos[0], (pos[1] + pos[3]) / 2))
        arrow(draw, (pos[0] + (pos[2] - pos[0]) / 2, pos[3]), (800, 520))

    arrow(draw, (800, 600), (800, 680))
    box(draw, (1180, 650, 1480, 730), "Prometheus")
    box(draw, (1180, 740, 1480, 820), "Grafana")
    box(draw, (1180, 830, 1480, 910), "Loki")
    arrow(draw, (970, 560), (1180, 690))
    arrow(draw, (970, 560), (1180, 780))
    arrow(draw, (970, 560), (1180, 870))

    img.save(OUT_DIR / "readme-architecture.png")


def generate_monitoring():
    img, draw = new_canvas("Monitoring & Observability")
    box(draw, (90, 220, 380, 300), "NestJS Services")
    box(draw, (90, 330, 380, 410), "Node Exporter")
    box(draw, (90, 440, 380, 520), "cAdvisor")
    box(draw, (540, 240, 860, 320), "Prometheus", fill="#E8F0FF", outline=BLUE)
    box(draw, (540, 430, 860, 510), "Promtail", fill="#EAF7F1", outline=GREEN)
    box(draw, (1020, 430, 1340, 510), "Loki")
    box(draw, (1020, 240, 1340, 320), "Grafana", fill="#E8F0FF", outline=BLUE)

    for y in (260, 370, 480):
        arrow(draw, (380, y), (540, 280))

    arrow(draw, (380, 480), (540, 470))
    arrow(draw, (860, 470), (1020, 470))
    arrow(draw, (860, 280), (1020, 280))
    arrow(draw, (1340, 280), (1340, 470))
    label(draw, (1360, 360), "Dashboards")

    img.save(OUT_DIR / "readme-monitoring.png")


def generate_testing():
    img, draw = new_canvas("Testing Workflow")
    steps = ["Unit Tests", "Integration Tests", "E2E Tests", "Coverage", "Report"]
    start_x = 120
    for i, step in enumerate(steps):
        x1 = start_x + i * 270
        box(draw, (x1, 350, x1 + 220, 450), step, fill="#FFFFFF")
        if i < len(steps) - 1:
            arrow(draw, (x1 + 220, 400), (x1 + 270, 400))

    label(draw, (120, 520), "CI-friendly pipeline for NestJS microservices", size=20)
    img.save(OUT_DIR / "readme-testing.png")


def generate_database():
    img, draw = new_canvas("Database ER Diagram")
    entities = {
        "Organizations": (120, 220, 420, 320),
        "Establishments": (520, 220, 860, 320),
        "Services": (1020, 220, 1360, 320),
        "Queues": (520, 380, 860, 480),
        "Turns": (520, 540, 860, 640),
        "Users": (120, 540, 420, 640),
    }
    for name, pos in entities.items():
        box(draw, pos, name)

    arrow(draw, (420, 270), (520, 270))
    arrow(draw, (860, 270), (1020, 270))
    arrow(draw, (690, 320), (690, 380))
    arrow(draw, (690, 480), (690, 540))
    arrow(draw, (420, 590), (520, 590))
    label(draw, (690, 345), "1..N")
    label(draw, (690, 505), "1..N")

    img.save(OUT_DIR / "readme-database.png")


def generate_api_docs():
    img, draw = new_canvas("API Documentation")
    box(draw, (120, 220, 460, 320), "API Gateway", fill="#E8F0FF", outline=BLUE)
    box(draw, (620, 180, 980, 260), "Swagger / OpenAPI")
    box(draw, (620, 290, 980, 370), "Auth Endpoints")
    box(draw, (620, 400, 980, 480), "Users Endpoints")
    box(draw, (620, 510, 980, 590), "Queues Endpoints")
    box(draw, (620, 620, 980, 700), "Turns Endpoints")
    arrow(draw, (460, 270), (620, 220))
    arrow(draw, (460, 270), (620, 330))
    arrow(draw, (460, 270), (620, 440))
    arrow(draw, (460, 270), (620, 550))
    arrow(draw, (460, 270), (620, 660))

    img.save(OUT_DIR / "readme-api-docs.png")


def generate_project_structure():
    img, draw = new_canvas("Project Structure")
    font = load_font(22)
    lines = [
        "apps/",
        "  gateway/",
        "  auth/",
        "  users/",
        "  establishments/",
        "  organizations/",
        "libs/",
        "  common/",
        "  rabbit/",
        "  database/",
        "  language/",
        "  token/",
        "observability/",
        "  prometheus/",
        "  grafana/",
        "  loki/",
        "  promtail/",
        "scripts/",
        "  local-dev.sh",
    ]
    start_y = 170
    for i, line in enumerate(lines):
        draw.text((140, start_y + i * 32), line, fill=DARK, font=font)

    img.save(OUT_DIR / "readme-project-structure.png")


def generate_ports():
    img, draw = new_canvas("Ports Overview")
    ports = [
        ("API Gateway", "3000"),
        ("Grafana", "3001"),
        ("Prometheus", "9090"),
        ("Loki", "3100"),
        ("RabbitMQ AMQP", "5672"),
        ("RabbitMQ Mgmt", "15672"),
        ("MariaDB", "3306"),
    ]
    for i, (name, port) in enumerate(ports):
        y1 = 180 + i * 90
        box(draw, (140, y1, 820, y1 + 70), name)
        box(draw, (880, y1, 1160, y1 + 70), f"Port {port}", fill="#EAF7F1", outline=GREEN)
        arrow(draw, (820, y1 + 35), (880, y1 + 35))

    img.save(OUT_DIR / "readme-ports.png")


def generate_tech_stack():
    img, draw = new_canvas("Technology Stack")
    tech = ["NestJS", "TypeScript", "RabbitMQ", "TypeORM", "MariaDB", "Docker", "Prometheus", "Grafana"]
    cols = 4
    for i, name in enumerate(tech):
        r = i // cols
        c = i % cols
        x1 = 140 + c * 340
        y1 = 220 + r * 180
        box(draw, (x1, y1, x1 + 280, y1 + 110), name)

    img.save(OUT_DIR / "readme-tech-stack.png")


def generate_scripts():
    img, draw = new_canvas("Developer Scripts")
    script_steps = ["format", "lint", "build", "run", "debug", "migrations"]
    for i, name in enumerate(script_steps):
        x1 = 140 + (i % 3) * 470
        y1 = 240 + (i // 3) * 200
        box(draw, (x1, y1, x1 + 360, y1 + 110), f"npm run {name}")

    img.save(OUT_DIR / "readme-scripts.png")


def generate_security():
    img, draw = new_canvas("Security Architecture")
    box(draw, (100, 300, 380, 400), "Client")
    box(draw, (460, 220, 760, 320), "Auth Service")
    box(draw, (460, 360, 760, 460), "JWT Token")
    box(draw, (840, 260, 1160, 360), "Protected APIs", fill="#E8F0FF", outline=BLUE)
    box(draw, (840, 400, 1160, 500), "Validation & Headers")
    box(draw, (1240, 320, 1500, 420), "Audit Logs", fill="#F0F3F7")
    arrow(draw, (380, 350), (460, 270))
    arrow(draw, (380, 350), (460, 410))
    arrow(draw, (760, 270), (840, 310))
    arrow(draw, (760, 410), (840, 450))
    arrow(draw, (1160, 310), (1240, 360))

    img.save(OUT_DIR / "readme-security.png")


def generate_license():
    img, draw = new_canvas("License Status")
    draw.rounded_rectangle((640, 320, 960, 640), radius=24, fill="#FFFFFF", outline=LIGHT_GRAY, width=2)
    draw.arc((700, 220, 900, 420), start=0, end=180, fill=GRAY, width=6)
    draw.ellipse((780, 440, 820, 480), fill=GRAY)
    box(draw, (560, 680, 1040, 760), "UNLICENSED", fill="#EAF7F1", outline=GREEN)

    img.save(OUT_DIR / "readme-license.png")


def generate_metrics_installation():
    img, draw = new_canvas("Metrics Installation")
    box(draw, (140, 260, 520, 380), "NestJS Service")
    box(draw, (620, 220, 1040, 320), "@nestjs/terminus", fill="#E8F0FF", outline=BLUE)
    box(draw, (620, 360, 1040, 460), "prom-client", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (520, 320), (620, 270))
    arrow(draw, (520, 320), (620, 410))
    label(draw, (140, 430), "Add monitoring dependencies to enable metrics", size=20)
    img.save(OUT_DIR / "metrics-installation.png")


def generate_metrics_microservice_setup():
    img, draw = new_canvas("Per-Microservice Metrics Setup")
    box(draw, (120, 220, 520, 320), "/health endpoint")
    box(draw, (120, 360, 520, 460), "/metrics endpoint")
    box(draw, (720, 250, 1120, 350), "Custom Counters")
    box(draw, (720, 390, 1120, 490), "Custom Histograms")
    box(draw, (520, 520, 900, 620), "Prometheus Scrape", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 270), (720, 300))
    arrow(draw, (520, 410), (720, 430))
    arrow(draw, (320, 460), (680, 520))
    img.save(OUT_DIR / "metrics-microservice-setup.png")


def generate_metrics_endpoints():
    img, draw = new_canvas("Metrics Endpoints")
    box(draw, (180, 260, 540, 360), "NestJS Service")
    box(draw, (720, 220, 1200, 300), "GET /health")
    box(draw, (720, 360, 1200, 440), "GET /metrics")
    arrow(draw, (540, 310), (720, 260))
    arrow(draw, (540, 310), (720, 400))
    label(draw, (720, 470), "Prometheus scrapes /metrics", size=20)
    img.save(OUT_DIR / "metrics-endpoints.png")


def generate_metrics_default():
    img, draw = new_canvas("Default Metrics")
    box(draw, (120, 220, 520, 320), "Memory Usage")
    box(draw, (120, 360, 520, 460), "CPU Usage")
    box(draw, (120, 500, 520, 600), "Event Loop Lag")
    box(draw, (720, 280, 1200, 380), "Process Stats")
    box(draw, (720, 420, 1200, 520), "Heap Size")
    arrow(draw, (520, 270), (720, 330))
    arrow(draw, (520, 410), (720, 470))
    img.save(OUT_DIR / "metrics-default.png")


def generate_metrics_verification():
    img, draw = new_canvas("Prometheus Verification")
    box(draw, (140, 260, 500, 360), "Prometheus")
    box(draw, (660, 220, 1200, 320), "Graph View")
    box(draw, (660, 360, 1200, 460), "Query: auth_login_attempts_total")
    box(draw, (660, 500, 1200, 600), "Timeseries Result")
    arrow(draw, (500, 310), (660, 270))
    arrow(draw, (500, 310), (660, 410))
    arrow(draw, (500, 310), (660, 550))
    img.save(OUT_DIR / "metrics-verification.png")


def generate_metrics_full_example():
    img, draw = new_canvas("Auth Metrics Example")
    box(draw, (120, 240, 520, 340), "login_attempts_total")
    box(draw, (120, 380, 520, 480), "token_validations_total")
    box(draw, (120, 520, 520, 620), "operation_duration_seconds")
    box(draw, (720, 320, 1200, 420), "Auth Service")
    arrow(draw, (520, 290), (720, 360))
    arrow(draw, (520, 430), (720, 360))
    arrow(draw, (520, 570), (720, 360))
    img.save(OUT_DIR / "metrics-full-example.png")


def generate_metrics_docker():
    img, draw = new_canvas("Docker + Prometheus")
    box(draw, (140, 260, 520, 360), "Prometheus")
    box(draw, (720, 220, 1200, 320), "auth:3000")
    box(draw, (720, 360, 1200, 460), "users:3000")
    box(draw, (720, 500, 1200, 600), "queues:3000")
    arrow(draw, (520, 310), (720, 270))
    arrow(draw, (520, 310), (720, 410))
    arrow(draw, (520, 310), (720, 550))
    label(draw, (140, 420), "Docker network scraping", size=20)
    img.save(OUT_DIR / "metrics-docker.png")


def generate_metrics_grafana_queries():
    img, draw = new_canvas("Grafana Queries")
    box(draw, (120, 240, 520, 320), "Login Rate")
    box(draw, (120, 360, 520, 440), "Error Rate")
    box(draw, (120, 480, 520, 560), "Latency p95")
    box(draw, (720, 300, 1200, 460), "Grafana Dashboards", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 280), (720, 340))
    arrow(draw, (520, 400), (720, 380))
    arrow(draw, (520, 520), (720, 420))
    img.save(OUT_DIR / "metrics-grafana-queries.png")


def generate_metrics_next_steps():
    img, draw = new_canvas("Next Steps")
    steps = ["Rollout to Services", "Build Dashboards", "Configure Alerts", "RabbitMQ Monitoring"]
    start_x = 120
    for i, step in enumerate(steps):
        x1 = start_x + i * 340
        box(draw, (x1, 360, x1 + 280, 460), step)
        if i < len(steps) - 1:
            arrow(draw, (x1 + 280, 410), (x1 + 340, 410))
    img.save(OUT_DIR / "metrics-next-steps.png")


def generate_metrics_references():
    img, draw = new_canvas("References")
    box(draw, (160, 260, 520, 340), "NestJS Terminus")
    box(draw, (160, 380, 520, 460), "prom-client")
    box(draw, (160, 500, 520, 580), "Prometheus Practices")
    box(draw, (720, 320, 1200, 500), "Documentation Links")
    arrow(draw, (520, 300), (720, 380))
    arrow(draw, (520, 420), (720, 420))
    arrow(draw, (520, 540), (720, 460))
    img.save(OUT_DIR / "metrics-references.png")


def generate_monitoring_components():
    img, draw = new_canvas("Monitoring Stack Components")
    box(draw, (100, 180, 400, 260), "Prometheus", fill="#E8F0FF", outline=BLUE)
    box(draw, (100, 290, 400, 370), "Grafana", fill="#E8F0FF", outline=BLUE)
    box(draw, (100, 400, 400, 480), "Loki")
    box(draw, (540, 180, 840, 260), "Promtail", fill="#EAF7F1", outline=GREEN)
    box(draw, (540, 290, 840, 370), "Node Exporter")
    box(draw, (540, 400, 840, 480), "cAdvisor")
    box(draw, (1020, 280, 1400, 380), "Full Observability", fill="#F0F3F7")
    arrow(draw, (400, 220), (1020, 330))
    arrow(draw, (400, 330), (1020, 330))
    arrow(draw, (400, 440), (1020, 330))
    arrow(draw, (840, 220), (1020, 330))
    arrow(draw, (840, 330), (1020, 330))
    arrow(draw, (840, 440), (1020, 330))
    img.save(OUT_DIR / "monitoring-components.png")


def generate_monitoring_services():
    img, draw = new_canvas("Monitored Services")
    services_left = ["Gateway", "Auth", "Users", "Establishments", "Organizations", "Kiosks"]
    services_right = ["Queues", "Screens", "Services", "Turns", "Waiting Areas", "Workspaces"]
    
    for i, svc in enumerate(services_left):
        y1 = 180 + i * 100
        box(draw, (100, y1, 380, y1 + 70), svc)
    
    for i, svc in enumerate(services_right):
        y1 = 180 + i * 100
        box(draw, (1220, y1, 1500, y1 + 70), svc)
    
    box(draw, (580, 280, 1020, 380), "Monitoring Stack", fill="#E8F0FF", outline=BLUE)
    box(draw, (580, 450, 1020, 550), "RabbitMQ + MariaDB", fill="#EAF7F1", outline=GREEN)
    
    arrow(draw, (380, 350), (580, 330))
    arrow(draw, (1020, 330), (1220, 350))
    img.save(OUT_DIR / "monitoring-services.png")


def generate_monitoring_usage():
    img, draw = new_canvas("Monitoring Usage")
    box(draw, (140, 240, 520, 340), "docker-compose up", fill="#E8F0FF", outline=BLUE)
    box(draw, (720, 180, 1200, 260), "Grafana :3001")
    box(draw, (720, 290, 1200, 370), "Prometheus :9090")
    box(draw, (720, 400, 1200, 480), "Loki :3100")
    box(draw, (720, 510, 1200, 590), "cAdvisor :8080")
    arrow(draw, (520, 290), (720, 220))
    arrow(draw, (520, 290), (720, 330))
    arrow(draw, (520, 290), (720, 440))
    arrow(draw, (520, 290), (720, 550))
    label(draw, (140, 400), "Access dashboards via browser", size=20)
    img.save(OUT_DIR / "monitoring-usage.png")


def generate_monitoring_configuration():
    img, draw = new_canvas("Monitoring Configuration")
    box(draw, (120, 200, 480, 280), "Prometheus Config")
    box(draw, (120, 320, 480, 400), "Promtail Config")
    box(draw, (120, 440, 480, 520), "Grafana Provisioning")
    box(draw, (120, 560, 480, 640), "Loki Config")
    box(draw, (640, 340, 1200, 480), "Scrape, Collect, Store", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (480, 240), (640, 390))
    arrow(draw, (480, 360), (640, 400))
    arrow(draw, (480, 480), (640, 430))
    arrow(draw, (480, 600), (640, 450))
    img.save(OUT_DIR / "monitoring-configuration.png")


def generate_monitoring_queries():
    img, draw = new_canvas("Query Examples")
    box(draw, (120, 240, 520, 320), "Prometheus PromQL")
    box(draw, (120, 360, 520, 440), "CPU & Memory")
    box(draw, (120, 480, 520, 560), "Request Rates")
    box(draw, (720, 240, 1200, 320), "Loki LogQL")
    box(draw, (720, 360, 1200, 440), "Logs & Errors")
    box(draw, (720, 480, 1200, 560), "Search Patterns")
    arrow(draw, (520, 280), (720, 280))
    arrow(draw, (520, 400), (720, 400))
    arrow(draw, (520, 520), (720, 520))
    img.save(OUT_DIR / "monitoring-queries.png")


def generate_monitoring_security():
    img, draw = new_canvas("Monitoring Security")
    box(draw, (140, 260, 520, 360), "Grafana Login", fill="#E8F0FF", outline=BLUE)
    box(draw, (140, 420, 520, 520), "Internal Network")
    box(draw, (720, 300, 1200, 440), "Isolated Services", fill="#F0F3F7")
    arrow(draw, (520, 310), (720, 350))
    arrow(draw, (520, 470), (720, 390))
    label(draw, (140, 580), "Secured monitoring stack", size=20)
    img.save(OUT_DIR / "monitoring-security.png")


def generate_monitoring_env():
    img, draw = new_canvas("Environment Variables")
    box(draw, (180, 280, 620, 360), "GRAFANA_ADMIN_USER")
    box(draw, (180, 400, 620, 480), "GRAFANA_ADMIN_PASSWORD")
    box(draw, (820, 320, 1300, 440), "Grafana Configuration", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (620, 320), (820, 360))
    arrow(draw, (620, 440), (820, 400))
    label(draw, (180, 540), "Configure via environment variables", size=20)
    img.save(OUT_DIR / "monitoring-env.png")


def generate_monitoring_cleanup():
    img, draw = new_canvas("Monitoring Cleanup")
    box(draw, (160, 260, 540, 340), "docker-compose down")
    box(draw, (160, 380, 540, 460), "Remove volumes")
    box(draw, (720, 280, 1200, 400), "Clean Stack", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (540, 300), (720, 320))
    arrow(draw, (540, 420), (720, 360))
    label(draw, (160, 520), "Stop and clean monitoring services", size=20)
    img.save(OUT_DIR / "monitoring-cleanup.png")


def generate_monitoring_more_info():
    img, draw = new_canvas("More Information")
    box(draw, (160, 240, 520, 320), "Prometheus Docs")
    box(draw, (160, 360, 520, 440), "Grafana Docs")
    box(draw, (160, 480, 520, 560), "Loki Docs")
    box(draw, (720, 300, 1200, 500), "Official Documentation")
    arrow(draw, (520, 280), (720, 370))
    arrow(draw, (520, 400), (720, 400))
    arrow(draw, (520, 520), (720, 430))
    img.save(OUT_DIR / "monitoring-more-info.png")


def generate_quickstart_setup():
    img, draw = new_canvas("Initial Setup")
    box(draw, (140, 240, 520, 320), "Clone Repository")
    box(draw, (140, 360, 520, 440), "npm install")
    box(draw, (140, 480, 520, 560), "chmod +x scripts")
    box(draw, (720, 320, 1200, 480), "Ready to Start", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (520, 280), (720, 380))
    arrow(draw, (520, 400), (720, 400))
    arrow(draw, (520, 520), (720, 420))
    img.save(OUT_DIR / "quickstart-setup.png")


def generate_quickstart_start():
    img, draw = new_canvas("Start the Project")
    box(draw, (100, 200, 480, 280), "./local-dev.sh")
    box(draw, (100, 320, 480, 400), "Custom Services")
    box(draw, (100, 440, 480, 520), "Env Variable")
    box(draw, (100, 560, 480, 640), "docker-compose")
    box(draw, (640, 340, 1200, 480), "System Running", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (480, 240), (640, 390))
    arrow(draw, (480, 360), (640, 400))
    arrow(draw, (480, 480), (640, 420))
    arrow(draw, (480, 600), (640, 440))
    img.save(OUT_DIR / "quickstart-start.png")


def generate_quickstart_access():
    img, draw = new_canvas("Access Services")
    services = [
        ("Swagger :3000", 200),
        ("Grafana :3001", 290),
        ("Prometheus :9090", 380),
        ("Loki :3100", 470),
        ("cAdvisor :8080", 560),
        ("RabbitMQ :15672", 650)
    ]
    for name, y in services:
        box(draw, (140, y, 620, y + 70), name)
    box(draw, (820, 380, 1300, 540), "Service URLs", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (620, 450), (820, 460))
    img.save(OUT_DIR / "quickstart-access.png")


def generate_quickstart_verify():
    img, draw = new_canvas("Verify Services")
    box(draw, (140, 260, 540, 340), "./verify-monitoring.sh")
    box(draw, (140, 390, 540, 470), "curl Swagger")
    box(draw, (140, 510, 540, 590), "curl Prometheus")
    box(draw, (720, 340, 1200, 480), "All Healthy", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (540, 300), (720, 390))
    arrow(draw, (540, 430), (720, 410))
    arrow(draw, (540, 550), (720, 430))
    img.save(OUT_DIR / "quickstart-verify.png")


def generate_quickstart_grafana():
    img, draw = new_canvas("First Steps in Grafana")
    box(draw, (140, 240, 520, 320), "Login Grafana")
    box(draw, (140, 360, 520, 440), "Data Sources")
    box(draw, (140, 480, 520, 560), "Dashboards")
    box(draw, (720, 320, 1200, 480), "Grafana Ready", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 280), (720, 380))
    arrow(draw, (520, 400), (720, 400))
    arrow(draw, (520, 520), (720, 420))
    img.save(OUT_DIR / "quickstart-grafana.png")


def generate_quickstart_logs():
    img, draw = new_canvas("View Logs")
    box(draw, (140, 260, 520, 360), "Grafana Loki Explore")
    box(draw, (140, 420, 520, 520), "docker-compose logs")
    box(draw, (720, 320, 1200, 460), "Log Aggregation", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 310), (720, 370))
    arrow(draw, (520, 470), (720, 410))
    label(draw, (140, 580), "Access logs via Grafana or CLI", size=20)
    img.save(OUT_DIR / "quickstart-logs.png")


def generate_quickstart_metrics():
    img, draw = new_canvas("View Metrics")
    box(draw, (140, 260, 520, 360), "Prometheus Graph")
    box(draw, (140, 420, 520, 520), "cAdvisor Containers")
    box(draw, (720, 320, 1200, 460), "Metrics Dashboard", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 310), (720, 370))
    arrow(draw, (520, 470), (720, 410))
    label(draw, (140, 580), "Explore system and app metrics", size=20)
    img.save(OUT_DIR / "quickstart-metrics.png")


def generate_quickstart_stop():
    img, draw = new_canvas("Stop the Project")
    box(draw, (140, 260, 520, 340), "Stop Script (Ctrl+C)")
    box(draw, (140, 390, 520, 470), "docker-compose down")
    box(draw, (140, 510, 520, 590), "Remove volumes")
    box(draw, (720, 340, 1200, 480), "Clean Shutdown", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (520, 300), (720, 390))
    arrow(draw, (520, 430), (720, 410))
    arrow(draw, (520, 550), (720, 430))
    img.save(OUT_DIR / "quickstart-stop.png")


def generate_quickstart_config():
    img, draw = new_canvas("Configuration")
    box(draw, (120, 220, 480, 300), "GATEWAY_PORT")
    box(draw, (120, 330, 480, 410), "RABBIT_MQ_URI")
    box(draw, (120, 440, 480, 520), "JWT_SECRET")
    box(draw, (120, 550, 480, 630), "GRAFANA_ADMIN_PASSWORD")
    box(draw, (640, 360, 1200, 500), "Environment Variables", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (480, 260), (640, 410))
    arrow(draw, (480, 370), (640, 420))
    arrow(draw, (480, 480), (640, 440))
    arrow(draw, (480, 590), (640, 460))
    img.save(OUT_DIR / "quickstart-config.png")


def generate_quickstart_troubleshooting():
    img, draw = new_canvas("Troubleshooting")
    issues = [
        ("Ports in Use", 200),
        ("Containers Not Starting", 300),
        ("Prometheus Not Scraping", 400),
        ("Loki No Logs", 500)
    ]
    for name, y in issues:
        box(draw, (120, y, 520, y + 70), name)
    box(draw, (720, 300, 1200, 460), "Check & Fix", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (520, 350), (720, 360))
    arrow(draw, (520, 450), (720, 390))
    img.save(OUT_DIR / "quickstart-troubleshooting.png")


def generate_quickstart_docs():
    img, draw = new_canvas("Documentation")
    box(draw, (140, 240, 520, 320), "README.md")
    box(draw, (140, 360, 520, 440), "MONITORING.md")
    box(draw, (140, 480, 520, 560), "METRICS.md")
    box(draw, (720, 320, 1200, 480), "Full Documentation", fill="#E8F0FF", outline=BLUE)
    arrow(draw, (520, 280), (720, 380))
    arrow(draw, (520, 400), (720, 400))
    arrow(draw, (520, 520), (720, 420))
    img.save(OUT_DIR / "quickstart-docs.png")


def generate_quickstart_next_steps():
    img, draw = new_canvas("Next Steps")
    steps = ["Implement Metrics", "Build Dashboards", "Configure Alerts", "Add Notifications"]
    start_x = 100
    for i, step in enumerate(steps):
        x1 = start_x + i * 360
        box(draw, (x1, 360, x1 + 300, 460), step)
        if i < len(steps) - 1:
            arrow(draw, (x1 + 300, 410), (x1 + 360, 410))
    img.save(OUT_DIR / "quickstart-next-steps.png")


def generate_quickstart_tips():
    img, draw = new_canvas("Tips & Best Practices")
    box(draw, (120, 220, 520, 300), "Development Shortcuts")
    box(draw, (120, 340, 520, 420), "Monitoring Usage")
    box(draw, (120, 460, 520, 540), "Logging Best Practices")
    box(draw, (120, 580, 520, 660), "Dashboard Versioning")
    box(draw, (720, 360, 1200, 520), "Pro Tips", fill="#EAF7F1", outline=GREEN)
    arrow(draw, (520, 260), (720, 420))
    arrow(draw, (520, 380), (720, 430))
    arrow(draw, (520, 500), (720, 450))
    arrow(draw, (520, 620), (720, 480))
    img.save(OUT_DIR / "quickstart-tips.png")


if __name__ == "__main__":
    generate_description()
    generate_architecture()
    generate_monitoring()
    generate_testing()
    generate_database()
    generate_api_docs()
    generate_project_structure()
    generate_ports()
    generate_tech_stack()
    generate_scripts()
    generate_security()
    generate_license()
    generate_metrics_installation()
    generate_metrics_microservice_setup()
    generate_metrics_endpoints()
    generate_metrics_default()
    generate_metrics_verification()
    generate_metrics_full_example()
    generate_metrics_docker()
    generate_metrics_grafana_queries()
    generate_metrics_next_steps()
    generate_metrics_references()
    generate_monitoring_components()
    generate_monitoring_services()
    generate_monitoring_usage()
    generate_monitoring_configuration()
    generate_monitoring_queries()
    generate_monitoring_security()
    generate_monitoring_env()
    generate_monitoring_cleanup()
    generate_monitoring_more_info()
    generate_quickstart_setup()
    generate_quickstart_start()
    generate_quickstart_access()
    generate_quickstart_verify()
    generate_quickstart_grafana()
    generate_quickstart_logs()
    generate_quickstart_metrics()
    generate_quickstart_stop()
    generate_quickstart_config()
    generate_quickstart_troubleshooting()
    generate_quickstart_docs()
    generate_quickstart_next_steps()
    generate_quickstart_tips()
    print("Generated images in", OUT_DIR)
