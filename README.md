# Apex MVP

A multi-tenant RAG (Retrieval-Augmented Generation) platform built with Python Flask, PostgreSQL, and Azure cloud infrastructure.

## 🚀 Quick Start

1. **Infrastructure**: Deploy Azure resources using Terraform
2. **Database**: Run SQL migrations to set up schemas
3. **Application**: Deploy Flask API via GitHub Actions
4. **Testing**: Verify endpoints and multi-tenant functionality

## 🏗️ Architecture

- **Frontend**: Web-based interface (future)
- **Backend**: Python Flask API with SQLAlchemy ORM
- **Database**: Azure PostgreSQL Flexible Server
- **Infrastructure**: Azure Container Registry, App Service, Resource Groups
- **CI/CD**: GitHub Actions for automated deployment

## 📁 Project Structure

```
apex-mvp/
├── infra/                    # Terraform infrastructure code
├── api/                      # Python Flask application
├── migrations/               # SQL database migrations
├── deploy/                   # Deployment scripts
├── .github/workflows/        # CI/CD workflows
├── Dockerfile               # Container configuration
└── README.md                # This file
```

## 🔧 API Endpoints

- `GET /health` - Health check endpoint
- `GET /memory` - Retrieve RAG memory entries
- `POST /memory` - Store new RAG memory entries
- `GET /feedback` - Retrieve feedback entries
- `POST /feedback` - Store new feedback entries

All endpoints support multi-tenant operations via `X-Tenant-ID` header.

## 🏢 Multi-Tenant Support

The platform supports multiple tenants through:
- Header-based tenant identification (`X-Tenant-ID`)
- Tenant-scoped database queries
- Isolated data storage per tenant

## 🚀 Development

### Prerequisites
- Python 3.8+
- Docker
- Azure CLI
- Terraform

### Local Development
```bash
cd api
pip install -r requirements.txt
python app.py
```

## 📄 License

MIT License - see LICENSE file for details.

---

## 🚀 DEPLOYMENT STATUS

**Last Updated**: August 27, 2025  
**Location**: Central US  
**Resource Group**: `apex-rg`

### ✅ DEPLOYED RESOURCES (Online)

| Resource | Name | Status | Details |
|----------|------|--------|---------|
| **Resource Group** | `apex-rg` | 🟢 **Deployed** | Central US location |
| **Container Registry** | `apexacrtoebb934.azurecr.io` | 🟢 **Deployed** | Ready for Docker images |
| **App Service Plan** | `apex-plan` | 🟢 **Deployed** | Linux, B1 tier |
| **Web App** | `apex-app-toebb934.azurewebsites.net` | 🟢 **Deployed** | Container-ready, accessible |
| **PostgreSQL Server** | `apex-psql-toebb934.postgres.database.azure.com` | 🟢 **Deployed** | Version 14, Standard_B1ms |
| **Random String** | `toebb934` | 🟢 **Deployed** | Unique identifier |

### ❌ PENDING RESOURCES (Not Deployed)

| Resource | Name | Status | Details |
|----------|------|--------|---------|
| **PostgreSQL Database** | `apexdb` | 🔴 **Pending** | Schema not created |
| **Firewall Rule** | `AllowAzureServices` | 🔴 **Pending** | Azure services access blocked |

### 🔑 CREDENTIALS & CONNECTION INFO

- **ACR Login Server**: `apexacrtoebb934.azurecr.io`
- **ACR Username**: `apexacrtoebb934`
- **ACR Password**: `ODY2JW7qtRD/G91r6P4G57titBVS/mk/RtP1SJ29I++ACRAv12Zi`
- **PostgreSQL FQDN**: `apex-psql-toebb934.postgres.database.azure.com`
- **PostgreSQL Admin**: `psqladmin`
- **Web App URL**: `https://apex-app-toebb934.azurewebsites.net`

### 🎯 NEXT STEPS FOR NEW AGENT

1. **Complete PostgreSQL Setup**:
   ```bash
   cd infra
   terraform apply -auto-approve
   ```

2. **Run Database Migrations**:
   ```bash
   # Connect to PostgreSQL and run migrations/001_create_schemas.sql
   ```

3. **Set Up GitHub Secrets** for CI/CD:
   - `AZURE_CREDENTIALS`
   - `ACR_USERNAME`
   - `ACR_PASSWORD`

4. **Deploy Application** via GitHub Actions

5. **Test Endpoints**:
   - Health: `https://apex-app-toebb934.azurewebsites.net/health`
   - Memory: `https://apex-app-toebb934.azurewebsites.net/memory`
   - Feedback: `https://apex-app-toebb934.azurewebsites.net/feedback`

### ⚠️ IMPORTANT NOTES

- **Location**: All resources are deployed in **Central US** (changed from East US due to subscription restrictions)
- **Terraform State**: Current state is clean, no conflicts
- **Web App**: Already accessible and container-ready
- **PostgreSQL**: Server is running but database and firewall rules need Terraform deployment
- **GitHub Workflow**: Temporarily removed due to token scope issues - needs `workflow` scope PAT
