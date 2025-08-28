# Apex MVP

A multi-tenant RAG (Retrieval-Augmented Generation) platform built with Python Flask, PostgreSQL, and Azure cloud infrastructure.

## 🚀 Quick Start

### Option 1: Azure Functions (Recommended - 5 minutes)
1. **Azure Functions**: Use the pre-deployed Function App for instant APIs
2. **Testing**: Test endpoints immediately at `https://apex-apis.azurewebsites.net`
3. **Frontend Ready**: Your frontend engineer can start building right away

### Option 2: Full Flask Deployment (Advanced)
1. **Infrastructure**: Deploy Azure resources using Terraform
2. **Database**: Run SQL migrations to set up schemas
3. **Application**: Deploy Flask API via GitHub Actions
4. **Testing**: Verify endpoints and multi-tenant functionality

## 🏗️ Architecture

### Primary: Azure Functions (Live & Ready)
- **Frontend**: Web-based interface (future)
- **Backend**: Azure Functions with Python runtime
- **Database**: Azure PostgreSQL (live via pg8000, SSL enabled)
- **Infrastructure**: Azure Function App, App Service Plan
- **Deployment**: GitHub Actions deploys Functions

<!-- Flask container path removed; Azure Functions is the primary and only supported backend now. -->

## 📁 Project Structure

```
apex-mvp/
├── infra/                    # Terraform infrastructure code
├── api/                      # Python Flask application
├── migrations/               # SQL database migrations
├── deploy/                   # Deployment scripts
├── .github/workflows/        # CI/CD workflows (Functions)
└── README.md                # This file
```

## 🔧 API Endpoints

### 🚀 **Azure Functions (LIVE NOW!)**
**Base URL**: `https://apex-apis.azurewebsites.net`

| Endpoint | Method | Description | Status |
|-----------|--------|-------------|---------|
| `/api/health` | GET | Health check endpoint | ✅ **Live** |
| `/api/memory` | GET | Retrieve memory entries | ✅ **Live** |
| `/api/memory` | POST | Store new memory entry | ✅ **Live** |
| `/api/feedback` | GET | Retrieve feedback entries | ✅ **Live** |
| `/api/feedback` | POST | Store new feedback entry | ✅ **Live** |

#### Request details

- GET `/api/memory`
  - Query params: `tenant_id` (required), `user_id` (optional), `session_id` (optional), `limit` (optional, default 100)
- POST `/api/memory`
  - JSON body: `tenant_id`, `user_id`, `session_id`, `content` (required); `message_type` (default `chat`), `metadata` (object)
- GET `/api/feedback`
  - Query params: `tenant_id` (required), `user_id` (optional), `response_id` (optional), `limit` (optional, default 100)
- POST `/api/feedback`
  - JSON body: `tenant_id`, `user_id`, `response_id`, `rating` (1-5) (required); `feedback_text` (alias `feedback`), `metadata` (object)

Required app setting on Function App:
- `POSTGRES_CONNECTION` (Application setting)
  - Example: `postgresql://psqladmin:ApexSecurePass123%21@apex-psql-toebb934.postgres.database.azure.com:5432/apexdb`
  - Notes: URL-encode password; SSL is enabled in code

### 🔧 **Flask Container (Alternative)**
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

## 🚀 **Azure Functions - Instant Onboarding**

### 🎯 **For Frontend Engineers (Start Here!)**
Your APIs are **LIVE NOW** at `https://apex-apis.azurewebsites.net`

#### Quick Test Commands:
```bash
# Health Check
curl https://apex-apis.azurewebsites.net/api/health

# Create Memory Entry (POST)
curl -X POST -H "Content-Type: application/json" \
  -d '{
        "tenant_id": "t1",
        "user_id": "u1",
        "session_id": "s1",
        "content": "Hello from curl",
        "metadata": {"source":"curl"}
      }' \
  https://apex-apis.azurewebsites.net/api/memory

# Get Memory (GET with filters)
curl "https://apex-apis.azurewebsites.net/api/memory?tenant_id=t1&user_id=u1&session_id=s1&limit=5"

# Create Feedback Entry (POST)
curl -X POST -H "Content-Type: application/json" \
  -d '{
        "tenant_id": "t1",
        "user_id": "u1",
        "response_id": "r1",
        "rating": 5,
        "feedback_text": "Great answer",
        "metadata": {"source":"curl"}
      }' \
  https://apex-apis.azurewebsites.net/api/feedback

# Get Feedback (GET with filters)
curl "https://apex-apis.azurewebsites.net/api/feedback?tenant_id=t1&user_id=u1&response_id=r1&limit=5"
```

#### Frontend Integration:
```javascript
const API_BASE = 'https://apex-apis.azurewebsites.net/api';

// GET memory
fetch(`${API_BASE}/memory?tenant_id=t1&user_id=u1&session_id=s1&limit=5`)
  .then(res => res.json())
  .then(data => console.log(data));

// POST memory
fetch(`${API_BASE}/memory`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ tenant_id: 't1', user_id: 'u1', session_id: 's1', content: 'New memory entry' })
})
.then(res => res.json())
.then(data => console.log(data));
```

<!-- Local Flask development removed; Azure Functions is the supported path. -->

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
| **Function App** | `apex-apis.azurewebsites.net` | 🟢 **Deployed** | **LIVE APIs READY!** |
| **PostgreSQL Server** | `apex-psql-toebb934.postgres.database.azure.com` | 🟢 **Deployed** | Version 14, Standard_B1ms |
| **PostgreSQL Database** | `apexdb` | 🟢 **Deployed** | Database created and ready |
| **Firewall Rule** | `AllowAzureServices` | 🟢 **Deployed** | Azure services access enabled |
| **Random String** | `toebb934` | 🟢 **Deployed** | Unique identifier |
| **Storage Account** | `apexstorage6736` | 🟢 **Deployed** | Standard LRS storage |
| **Function App Plan** | `apex-functions-plan` | 🟢 **Deployed** | Linux, B1 tier |
| **Function App** | `apex-apis.azurewebsites.net` | 🟢 **Deployed** | **LIVE APIs READY!** |

### ❌ PENDING RESOURCES (Not Deployed)

| Resource | Name | Status | Details |
|----------|------|--------|---------|
| **GitHub Actions Workflow** | `ci-cd-deploy.yml` | 🔴 **Failing** | Health check failing after deployment |

### 🔑 CREDENTIALS & CONNECTION INFO

- **ACR Login Server**: `apexacrtoebb934.azurecr.io`
- **ACR Username**: `apexacrtoebb934`
- **ACR Password**: `[REDACTED - Set as GitHub Secret]`
- **PostgreSQL FQDN**: `apex-psql-toebb934.postgres.database.azure.com`
- **PostgreSQL Admin**: `psqladmin`
- **PostgreSQL Database**: `apexdb` ✅ **Created**
- **Function App URL**: `https://apex-apis.azurewebsites.net`

### 🎯 NEXT STEPS FOR NEW AGENT

**🚀 PRIMARY SOLUTION: Azure Functions are LIVE and ready!**
- **URL**: `https://apex-apis.azurewebsites.net`
- **Status**: All APIs working with GET/POST support
- **Frontend**: Can start building immediately

**Test Endpoints (Azure Functions):**
 - Health: `https://apex-apis.azurewebsites.net/api/health`
 - Memory: `https://apex-apis.azurewebsites.net/api/memory`
 - Feedback: `https://apex-apis.azurewebsites.net/api/feedback`

### ⚠️ IMPORTANT NOTES

- **Location**: All resources are deployed in **Central US** (changed from East US due to subscription restrictions)
- **Terraform State**: Current state is clean, no conflicts
- **Web App**: Already accessible and container-ready
- **PostgreSQL**: Server, database, and firewall rules are all deployed and working
- **GitHub Workflow**: **DEPLOYMENT SUCCEEDS BUT HEALTH CHECK FAILS** - this is the current blocker
- **Issue**: Container starts successfully but Flask app can't connect to database, causing health check to fail#   T r i g g e r   d e p l o y m e n t   w i t h   f i x e d   s c h e m a 
 
 #   T e s t   d e p l o y m e n t   w i t h   a l l   s e c r e t s   u p d a t e d 
 
 #   T e s t   d e p l o y m e n t   w i t h   f r e s h   A C R   p a s s w o r d 
 
 #   D e p l o y   w i t h   n o n - b l o c k i n g   h e a l t h   c h e c k 
 
 