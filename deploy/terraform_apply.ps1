# Terraform deployment script for Apex MVP (PowerShell)
# This script initializes, plans, and applies Terraform configuration

param(
    [switch]$Force,
    [switch]$Help
)

# Show help if requested
if ($Help) {
    Write-Host @"
Terraform deployment script for Apex MVP

Usage: .\terraform_apply.ps1 [-Force] [-Help]

Parameters:
    -Force    Skip confirmation prompt
    -Help     Show this help message

Environment Variables Required:
    TF_VAR_prefix         - Prefix for resource names
    TF_VAR_pg_password   - PostgreSQL administrator password

Example:
    .\terraform_apply.ps1
    .\terraform_apply.ps1 -Force
"@
    exit 0
}

# Function to write colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Check if required environment variables are set
function Test-EnvironmentVariables {
    Write-Status "Checking environment variables..."
    
    if (-not $env:TF_VAR_prefix) {
        Write-Error "TF_VAR_prefix is not set"
        Write-Status "Please set: `$env:TF_VAR_prefix = 'apex'"
        exit 1
    }
    
    if (-not $env:TF_VAR_pg_password) {
        Write-Error "TF_VAR_pg_password is not set"
        Write-Status "Please set: `$env:TF_VAR_pg_password = 'your-secure-password'"
        exit 1
    }
    
    Write-Success "Environment variables are set"
}

# Check if Terraform is installed
function Test-Terraform {
    Write-Status "Checking Terraform installation..."
    
    try {
        $terraformVersion = terraform version -json | ConvertFrom-Json | Select-Object -ExpandProperty terraform_version
        Write-Success "Terraform $terraformVersion is installed"
    }
    catch {
        Write-Error "Terraform is not installed or not in PATH"
        Write-Status "Please install Terraform from: https://www.terraform.io/downloads.html"
        exit 1
    }
}

# Check if Azure CLI is installed and authenticated
function Test-AzureCLI {
    Write-Status "Checking Azure CLI installation and authentication..."
    
    try {
        $azVersion = az version --output json | ConvertFrom-Json | Select-Object -ExpandProperty "azure-cli"
        Write-Success "Azure CLI $azVersion is installed"
    }
    catch {
        Write-Error "Azure CLI is not installed"
        Write-Status "Please install Azure CLI from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    }
    
    # Check if logged in
    try {
        $account = az account show --output json | ConvertFrom-Json
        $userName = $account.user.name
        $subscriptionName = $account.name
        Write-Success "Logged in as: $userName"
        Write-Success "Subscription: $subscriptionName"
    }
    catch {
        Write-Error "Not logged into Azure CLI"
        Write-Status "Please run: az login"
        exit 1
    }
}

# Initialize Terraform
function Initialize-Terraform {
    Write-Status "Initializing Terraform..."
    
    Set-Location infra
    
    if (-not (Test-Path ".terraform")) {
        terraform init
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Terraform initialized"
        } else {
            Write-Error "Terraform init failed"
            exit 1
        }
    } else {
        Write-Status "Terraform already initialized, skipping..."
    }
}

# Plan Terraform changes
function Plan-Terraform {
    Write-Status "Planning Terraform changes..."
    
    terraform plan -out=tfplan
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Terraform plan completed successfully"
    } else {
        Write-Error "Terraform plan failed"
        exit 1
    }
}

# Apply Terraform changes
function Apply-Terraform {
    Write-Status "Applying Terraform changes..."
    
    # Ask for confirmation unless -Force is specified
    if (-not $Force) {
        Write-Warning "This will create/modify Azure resources. Are you sure? (y/N)"
        $response = Read-Host
        
        if ($response -notmatch '^([yY][eE][sS]|[yY])$') {
            Write-Status "Deployment cancelled by user"
            exit 0
        }
    }
    
    terraform apply tfplan
    
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Terraform apply completed successfully!"
        
        # Show outputs
        Write-Host ""
        Write-Status "Infrastructure outputs:"
        terraform output
        
        # Save outputs to file for reference
        terraform output -json | Out-File -FilePath "../deploy_outputs.json" -Encoding UTF8
        Write-Success "Outputs saved to deploy_outputs.json"
        
    } else {
        Write-Error "Terraform apply failed"
        exit 1
    }
}

# Cleanup
function Remove-TemporaryFiles {
    Write-Status "Cleaning up..."
    
    if (Test-Path "tfplan") {
        Remove-Item "tfplan" -Force
    }
    
    Set-Location ..
}

# Main execution
function Main {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "    Apex MVP - Terraform Deployment" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    
    # Run checks
    Test-EnvironmentVariables
    Test-Terraform
    Test-AzureCLI
    
    Write-Host ""
    
    # Deploy infrastructure
    Initialize-Terraform
    Plan-Terraform
    Apply-Terraform
    
    Write-Host ""
    Write-Success "Deployment completed successfully!"
    Write-Status "Next steps:"
    Write-Status "1. Add the required secrets to GitHub repository"
    Write-Status "2. Push your code to trigger the CI/CD pipeline"
    Write-Status "3. Run the database migration: psql -h <postgres_fqdn> -U psqladmin -d apexdb -f migrations/001_create_schemas.sql"
    
    Remove-TemporaryFiles
}

# Run main function
try {
    Main
}
catch {
    Write-Error "An error occurred: $($_.Exception.Message)"
    exit 1
}
