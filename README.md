# Apex MVP

A scalable RAG (Retrieval-Augmented Generation) platform with multi-tenant architecture, built on Azure infrastructure.

## Architecture

- **Infrastructure**: Azure (Terraform)
- **Backend**: Python Flask API
- **Database**: Azure PostgreSQL Flexible Server
- **Container Registry**: Azure Container Registry (ACR)
- **Hosting**: Azure App Service (Linux)
- **CI/CD**: GitHub Actions

## Quick Start

1. **Prerequisites**
   - Terraform >= 1.0
   - Azure CLI
   - Docker
   - Python 3.8+

2. **Deploy Infrastructure**
   ```bash
   cd deploy
   export TF_VAR_prefix="apex"
   export TF_VAR_pg_password="your-secure-password"
   ./terraform_apply.sh
   ```

3. **Set GitHub Secrets**
   - `AZURE_CREDENTIALS`: Service principal credentials
   - `ACR_LOGIN_SERVER`: ACR server URL
   - `ACR_USERNAME`: ACR username
   - `ACR_PASSWORD`: ACR password
   - `APP_NAME`: Web app name
   - `RESOURCE_GROUP`: Resource group name
   - `IMAGE_NAME`: Container image name
   - `POSTGRES_CONNECTION`: PostgreSQL connection string

4. **Deploy Application**
   ```bash
   git push origin main
   ```
   GitHub Actions will automatically build and deploy the container.

5. **Run Database Migrations**
   ```bash
   # Connect to your PostgreSQL instance and run:
   psql -h <postgres_fqdn> -U <username> -d apexdb -f migrations/001_create_schemas.sql
   ```

6. **Test Deployment**
   ```bash
   curl https://<web_app_url>/health
   ```

## Project Structure

```
├── infra/                 # Terraform infrastructure code
├── deploy/                # Deployment helper scripts
├── migrations/            # Database schema migrations
├── .github/workflows/     # CI/CD pipelines
├── api/                   # Backend API code
├── Dockerfile            # Container definition
└── README.deploy.md      # Detailed deployment guide
```

## API Endpoints

- `GET /health` - Health check
- `GET /memory` - Retrieve RAG memory entries
- `POST /memory` - Store RAG memory entries
- `GET /feedback` - Retrieve feedback entries
- `POST /feedback` - Store feedback entries

## Multi-Tenant Support

All endpoints accept `X-Tenant-ID` header for tenant isolation.

## Development

- Local development: `cd api && python app.py`
- Container build: `docker build -t apex-mvp .`
- Container run: `docker run -p 8080:8080 apex-mvp`

## License

MIT
