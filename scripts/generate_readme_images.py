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
    print("Generated images in", OUT_DIR)
