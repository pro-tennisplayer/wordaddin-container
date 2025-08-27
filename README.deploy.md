# Apex MVP - Complete Deployment Guide

This guide walks you through deploying the Apex MVP platform from scratch. Follow each step carefully to ensure a successful deployment.

## Prerequisites

Before starting, ensure you have the following installed:

### 1. Required Software

- **Terraform** (>= 1.0): [Download here](https://www.terraform.io/downloads.html)
- **Azure CLI**: [Download here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Docker**: [Download here](https://docs.docker.com/get-docker/)
- **Git**: [Download here](https://git-scm.com/downloads)
- **PostgreSQL Client** (optional, for running migrations): [Download here](https://www.postgresql.org/download/)

### 2. Azure Account

- Active Azure subscription
- Contributor or Owner role on the subscription
- Service Principal with appropriate permissions (for CI/CD)

## Step 1: Initial Setup

### 1.1 Clone and Setup Repository

```bash
# Clone the repository
git clone <your-repo-url>
cd apex-mvp

# Ensure you're on the main branch
git checkout main
```

### 1.2 Azure Authentication

```bash
# Login to Azure
az login

# Set your subscription (if you have multiple)
az account set --subscription "<subscription-id>"

# Verify you're logged in
az account show
```

## Step 2: Deploy Infrastructure

### 2.1 Set Environment Variables

```bash
# Set the prefix for your resources (must be unique)
export TF_VAR_prefix="apex"

# Set a secure PostgreSQL password
export TF_VAR_pg_password="YourSecurePassword123!"

# Optional: Set Azure region (defaults to East US)
export TF_VAR_location="East US"
```

**⚠️ Important**: 
- The `prefix` must be globally unique across Azure
- Use a strong password for PostgreSQL
- Keep these credentials secure

### 2.2 Run Terraform Deployment

```bash
# Make the script executable
chmod +x deploy/terraform_apply.sh

# Run the deployment
./deploy/terraform_apply.sh
```

The script will:
1. Check prerequisites
2. Initialize Terraform
3. Plan the deployment
4. Ask for confirmation
5. Apply the infrastructure
6. Display outputs

### 2.3 Save Infrastructure Outputs

After successful deployment, the script saves outputs to `deploy_outputs.json`. Keep this file secure as it contains sensitive information.

## Step 3: Configure GitHub Secrets

### 3.1 Create Service Principal (if not exists)

```bash
# Create service principal for GitHub Actions
az ad sp create-for-rbac \
  --name "apex-mvp-github-actions" \
  --role contributor \
  --scopes /subscriptions/<subscription-id> \
  --sdk-auth
```

**Save the output JSON** - you'll need it for the `AZURE_CREDENTIALS` secret.

### 3.2 Add Repository Secrets

Go to your GitHub repository → Settings → Secrets and variables → Actions, and add:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `AZURE_CREDENTIALS` | Service principal JSON | Full JSON output from service principal creation |
| `ACR_LOGIN_SERVER` | `apexacr<random>.azurecr.io` | From Terraform output `acr_login_server` |
| `ACR_USERNAME` | `apexacr<random>` | From Terraform output `acr_admin_username` |
| `ACR_PASSWORD` | `<password>` | From Terraform output `acr_admin_password` |
| `APP_NAME` | `apex-app-<random>` | From Terraform output `web_app_name` |
| `RESOURCE_GROUP` | `apex-rg` | From Terraform output `resource_group` |
| `IMAGE_NAME` | `apex-mvp` | Container image name |
| `POSTGRES_CONNECTION` | `postgresql://psqladmin:...` | PostgreSQL connection string |

### 3.3 Build PostgreSQL Connection String

```bash
# Format: postgresql://username:password@host:port/database
POSTGRES_CONNECTION="postgresql://psqladmin:${TF_VAR_pg_password}@$(terraform output -raw postgres_fqdn):5432/apexdb"
```

## Step 4: Deploy Application

### 4.1 Push Code to Trigger CI/CD

```bash
# Add all files
git add .

# Commit changes
git commit -m "Initial deployment setup"

# Push to main branch
git push origin main
```

### 4.2 Monitor GitHub Actions

1. Go to your repository → Actions
2. Monitor the "CI/CD Pipeline - Build and Deploy" workflow
3. Wait for completion (should take 5-10 minutes)

## Step 5: Database Setup

### 5.1 Run Database Migration

```bash
# Connect to PostgreSQL and run migration
psql -h $(terraform output -raw postgres_fqdn) \
     -U psqladmin \
     -d apexdb \
     -f migrations/001_create_schemas.sql
```

**Note**: You'll be prompted for the password you set in `TF_VAR_pg_password`.

### 5.2 Verify Database Schema

```bash
# Connect to database
psql -h $(terraform output -raw postgres_fqdn) -U psqladmin -d apexdb

# List schemas
\dn

# List tables in rag_memory schema
\dt rag_memory.*

# List tables in rag_feedback schema
\dt rag_feedback.*

# Exit
\q
```

## Step 6: Test Deployment

### 6.1 Test Health Endpoint

```bash
# Get your web app URL
WEBAPP_URL=$(terraform output -raw web_app_url)

# Test health endpoint
curl -f "https://$WEBAPP_URL/health"
```

Expected response:
```json
{
  "status": "ok",
  "timestamp": "2024-01-01T00:00:00.000000",
  "database": "connected"
}
```

### 6.2 Test Other Endpoints

```bash
# Test root endpoint
curl "https://$WEBAPP_URL/"

# Test memory endpoint with tenant ID
curl -H "X-Tenant-ID: test-tenant" "https://$WEBAPP_URL/memory"

# Test feedback endpoint with tenant ID
curl -H "X-Tenant-ID: test-tenant" "https://$WEBAPP_URL/feedback"
```

## Step 7: Local Development (Optional)

### 7.1 Run Locally

```bash
# Set environment variables
export POSTGRES_CONNECTION="postgresql://psqladmin:${TF_VAR_pg_password}@$(terraform output -raw postgres_fqdn):5432/apexdb"

# Install Python dependencies
cd api
pip install -r requirements.txt

# Run the application
python app.py
```

### 7.2 Test Locally

```bash
# Test health endpoint
curl http://localhost:8080/health

# Test with tenant ID
curl -H "X-Tenant-ID: local-test" http://localhost:8080/memory
```

## Step 8: Container Testing

### 8.1 Build Container

```bash
# Build the container
docker build -t apex-mvp .

# Run the container
docker run -p 8080:8080 \
  -e POSTGRES_CONNECTION="postgresql://psqladmin:${TF_VAR_pg_password}@$(terraform output -raw postgres_fqdn):5432/apexdb" \
  apex-mvp
```

### 8.2 Test Container

```bash
# Test health endpoint
curl http://localhost:8080/health
```

## Troubleshooting

### Common Issues

1. **Terraform Plan Fails**
   - Check Azure CLI authentication
   - Verify subscription permissions
   - Ensure resource names are unique

2. **GitHub Actions Fail**
   - Verify all secrets are set correctly
   - Check service principal permissions
   - Ensure resource names match outputs

3. **Database Connection Fails**
   - Verify PostgreSQL server is running
   - Check firewall rules
   - Confirm connection string format

4. **Web App Not Accessible**
   - Wait for deployment to complete
   - Check app service logs
   - Verify container image was pushed

### Useful Commands

```bash
# Check Azure resources
az resource list --resource-group apex-rg

# Check web app logs
az webapp log tail --name <app-name> --resource-group apex-rg

# Check container registry
az acr repository list --name <acr-name>

# Check PostgreSQL server status
az postgres flexible-server show --name <server-name> --resource-group apex-rg
```

## Next Steps

After successful deployment:

1. **Monitor**: Set up Azure Monitor and Application Insights
2. **Security**: Configure network security groups and firewall rules
3. **Scaling**: Adjust app service plan based on usage
4. **Backup**: Set up automated database backups
5. **Development**: Start building your RAG application logic

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review Azure portal for resource status
3. Check GitHub Actions logs for detailed error messages
4. Verify all environment variables and secrets are set correctly

## Security Notes

- Never commit sensitive information to version control
- Use strong passwords for all services
- Regularly rotate service principal credentials
- Monitor resource access and usage
- Enable Azure Security Center recommendations
