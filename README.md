# NestJS API Microservices with RabbitMQ

API for managing queues and services using a microservices architecture with NestJS, RabbitMQ, and TypeORM.

## Description

Modular system for managing organizations, establishments, users, turns, and waiting areas. It uses RabbitMQ for inter-service communication and MariaDB as the database. It includes a full monitoring stack with Prometheus, Grafana, Loki, and Promtail.

![Description](docs/images/readme-description.png)

## Architecture

### Microservices

- **Gateway** - API Gateway with Swagger at `/document` (port 3000)
- **Auth** - Authentication and authorization (queue: `auth_queue`)
- **Users** - User management (queue: `users_queue`)
- **Establishments** - Establishment management (queue: `establishments_queue`)
- **Organizations** - Organization management (queue: `organizations_queue`)
- **Kiosks** - Kiosk management (queue: `kiosks_queue`)
- **Queues** - Queue management (queue: `services_queue`)
- **Screens** - Screen management
- **Services** - Service management
- **Turns** - Turn management
- **Waiting Areas** - Waiting area management
- **Workspaces** - Workspace management
- **Notifications** - Notifications (queue: `notifications_queue`)

### Shared Libraries

- **@app/common** - Common utilities, filters, exceptions
- **@app/rabbit** - RabbitMQ configuration and helpers
- **@app/database** - TypeORM configuration and migrations
- **@app/language** - Internationalization (i18n)
- **@app/token** - JWT token handling

### Monitoring Stack

- **Prometheus** - Metrics collection (port 9090)
- **Grafana** - Dashboards (port 3001)
- **Loki** - Log aggregation (port 3100)
- **Promtail** - Log collector agent
- **Node Exporter** - System metrics (port 9100)
- **cAdvisor** - Docker container metrics (port 8080)

![Architecture](docs/images/readme-architecture.png)

## Requirements

- Node.js v20.10.0+
- Docker and Docker Compose
- npm

## Installation

```bash
npm install
```

## Configuration

Configure environment variables in `libs/common/src/env/.env`:

```env
# Gateway
GATEWAY_PORT=3000

# RabbitMQ
RABBIT_MQ_URI=amqp://admin:passw123@localhost:5672

# Database
DB_HOST=localhost
DB_PORT=3306

# JWT
JWT_SECRET=your-secret-key

# Clerk (Auth)
CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Grafana (Monitoring)
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin123
```

## Running

### Local Development (Recommended)

Start infrastructure (RabbitMQ + MariaDB + monitoring stack) and services in debug mode:

```bash
# Grant execute permission to the script
chmod +x scripts/local-dev.sh

# Run with default services (gateway, auth, users, establishments, organizations)
./scripts/local-dev.sh

# Or specify custom services
./scripts/local-dev.sh gateway auth users

# Or via environment variable
SERVICES="gateway auth" ./scripts/local-dev.sh
```

The script:
- Starts `docker-compose-local.yml` with RabbitMQ, MariaDB, and monitoring services
- Boots each microservice in debug mode
- Prints the Swagger URL when the gateway is ready: http://localhost:3000/document
- Prints the monitoring dashboard URLs

### Docker Compose

```bash
# Development (with monitoring)
docker-compose -f docker-compose-local.yml up -d

# Production
docker-compose up --build
```

### Individual Microservices

```bash
# Gateway (with Swagger)
npm run start:gateway_debug

# Auth
npm run start:auth_debug

# Users
npm run start:users_debug

# Establishments
npm run start:establishments_debug

# Other services
npm run start:<service>_debug
```

## Monitoring

### Dashboards and Tools

| Component | URL | User | Password |
|-----------|-----|------|----------|
| **Grafana** | http://localhost:3001 | admin | admin123 |
| **Prometheus** | http://localhost:9090 | - | - |
| **Loki** | http://localhost:3100 | - | - |
| **cAdvisor** | http://localhost:8080 | - | - |
| **RabbitMQ** | http://localhost:15672 | admin | passw123 |

For more details, see [MONITORING.md](MONITORING.md).

![Monitoring](docs/images/readme-monitoring.png)

## Testing

```bash
# Unit tests
npm run test

# Tests for a specific module
npm run test:module <path>

# Tests with coverage
npm run test:cov

# E2E tests
npm run test:e2e

# Tests in watch mode
npm run test:watch
```

![Testing](docs/images/readme-testing.png)

## Database

### Migrations

```bash
# Run migrations
npm run migration:run

# Generate a new migration
npm run migration:generate --name=MigrationName

# Create an empty migration
npm run migration:create --name=MigrationName

# Revert last migration
npm run migration:revert
```

![Database](docs/images/readme-database.png)

## API Documentation

With the gateway running, access:

- **Swagger UI**: http://localhost:3000/document
- **JSON Spec**: http://localhost:3000/document.json

![API Documentation](docs/images/readme-api-docs.png)

## Project Structure

```
apps/
├── gateway/          # API Gateway with Swagger
├── auth/             # Authentication microservice
├── users/            # Users microservice
├── establishments/   # Establishments microservice
├── organizations/    # Organizations microservice
└── ...               # Other microservices

libs/
├── common/           # Shared code
├── rabbit/           # RabbitMQ configuration
├── database/         # TypeORM and migrations
├── language/         # i18n
└── token/            # JWT

observability/
├── prometheus/       # Prometheus configuration
├── grafana/          # Dashboards and provisioning
├── loki/             # Loki configuration
└── promtail/         # Promtail configuration

scripts/
└── local-dev.sh      # Local development script

static/
└── i18n/
    ├── en/           # English translations
    └── fa/           # Persian translations
```

![Project Structure](docs/images/readme-project-structure.png)

## Ports

| Service | Port | Description |
|---------|------|-------------|
| Gateway | 3000 | REST API with Swagger |
| Grafana | 3001 | Monitoring dashboards |
| Prometheus | 9090 | Metrics and queries |
| Loki | 3100 | Log aggregation |
| cAdvisor | 8080 | Container metrics |
| Node Exporter | 9100 | System metrics |
| RabbitMQ AMQP | 5672 | Message broker |
| RabbitMQ Management | 15672 | Admin console |
| MariaDB | 3306 | Database |

![Ports](docs/images/readme-ports.png)

## Technology Stack

- **Framework**: NestJS 10
- **Language**: TypeScript 5
- **Message Broker**: RabbitMQ 3.11
- **ORM**: TypeORM 0.3
- **Database**: MariaDB 11.3
- **Authentication**: Passport JWT + Clerk
- **Documentation**: Swagger/OpenAPI
- **Monitoring**: Prometheus, Grafana, Loki
- **Security**: Helmet
- **Testing**: Jest

![Technology Stack](docs/images/readme-tech-stack.png)

## Useful Scripts

```bash
# Format code
npm run format

# Lint
npm run lint

# Build
npm run build

# Run TypeORM CLI
npm run typeorm -- <command>
```

![Useful Scripts](docs/images/readme-scripts.png)

## Security

- JWT authentication
- Helmet security headers
- Validation with class-validator
- CORS enabled
- Audit logs with Loki

![Security](docs/images/readme-security.png)

## License

UNLICENSED
