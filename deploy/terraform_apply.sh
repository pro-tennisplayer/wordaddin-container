#!/bin/bash

# Terraform deployment script for Apex MVP
# This script initializes, plans, and applies Terraform configuration

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required environment variables are set
check_env_vars() {
    print_status "Checking environment variables..."
    
    if [ -z "$TF_VAR_prefix" ]; then
        print_error "TF_VAR_prefix is not set"
        print_status "Please set: export TF_VAR_prefix='apex'"
        exit 1
    fi
    
    if [ -z "$TF_VAR_pg_password" ]; then
        print_error "TF_VAR_pg_password is not set"
        print_status "Please set: export TF_VAR_pg_password='your-secure-password'"
        exit 1
    fi
    
    print_success "Environment variables are set"
}

# Check if Terraform is installed
check_terraform() {
    print_status "Checking Terraform installation..."
    
    if ! command -v terraform &> /dev/null; then
        print_error "Terraform is not installed"
        print_status "Please install Terraform from: https://www.terraform.io/downloads.html"
        exit 1
    fi
    
    TERRAFORM_VERSION=$(terraform version -json | jq -r '.terraform_version')
    print_success "Terraform $TERRAFORM_VERSION is installed"
}

# Check if Azure CLI is installed and authenticated
check_azure_cli() {
    print_status "Checking Azure CLI installation and authentication..."
    
    if ! command -v az &> /dev/null; then
        print_error "Azure CLI is not installed"
        print_status "Please install Azure CLI from: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
        exit 1
    fi
    
    # Check if logged in
    if ! az account show &> /dev/null; then
        print_error "Not logged into Azure CLI"
        print_status "Please run: az login"
        exit 1
    fi
    
    ACCOUNT=$(az account show --query "user.name" -o tsv)
    SUBSCRIPTION=$(az account show --query "name" -o tsv)
    print_success "Logged in as: $ACCOUNT"
    print_success "Subscription: $SUBSCRIPTION"
}

# Initialize Terraform
init_terraform() {
    print_status "Initializing Terraform..."
    
    cd infra
    
    if [ ! -d ".terraform" ]; then
        terraform init
        print_success "Terraform initialized"
    else
        print_status "Terraform already initialized, skipping..."
    fi
}

# Plan Terraform changes
plan_terraform() {
    print_status "Planning Terraform changes..."
    
    terraform plan -out=tfplan
    
    if [ $? -eq 0 ]; then
        print_success "Terraform plan completed successfully"
    else
        print_error "Terraform plan failed"
        exit 1
    fi
}

# Apply Terraform changes
apply_terraform() {
    print_status "Applying Terraform changes..."
    
    # Ask for confirmation
    echo
    print_warning "This will create/modify Azure resources. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        terraform apply tfplan
        
        if [ $? -eq 0 ]; then
            print_success "Terraform apply completed successfully!"
            
            # Show outputs
            echo
            print_status "Infrastructure outputs:"
            terraform output
            
            # Save outputs to file for reference
            terraform output -json > ../deploy_outputs.json
            print_success "Outputs saved to deploy_outputs.json"
            
        else
            print_error "Terraform apply failed"
            exit 1
        fi
    else
        print_status "Deployment cancelled by user"
        exit 0
    fi
}

# Cleanup
cleanup() {
    print_status "Cleaning up..."
    
    if [ -f "tfplan" ]; then
        rm tfplan
    fi
    
    cd ..
}

# Main execution
main() {
    echo "=========================================="
    echo "    Apex MVP - Terraform Deployment"
    echo "=========================================="
    echo
    
    # Run checks
    check_env_vars
    check_terraform
    check_azure_cli
    
    echo
    
    # Deploy infrastructure
    init_terraform
    plan_terraform
    apply_terraform
    
    echo
    print_success "Deployment completed successfully!"
    print_status "Next steps:"
    print_status "1. Add the required secrets to GitHub repository"
    print_status "2. Push your code to trigger the CI/CD pipeline"
    print_status "3. Run the database migration: psql -h <postgres_fqdn> -U psqladmin -d apexdb -f migrations/001_create_schemas.sql"
    
    cleanup
}

# Run main function
main "$@"
