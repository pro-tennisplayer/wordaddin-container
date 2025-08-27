terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-rg"
  location = var.location
  tags = {
    Environment = "Production"
    Project     = "Apex-MVP"
  }
}

# Azure Container Registry
resource "azurerm_container_registry" "main" {
  name                = "${var.prefix}acr${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Basic"
  admin_enabled       = true
  tags = {
    Environment = "Production"
    Project     = "Apex-MVP"
  }
}

# Random string for unique naming
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "${var.prefix}-plan"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"
  tags = {
    Environment = "Production"
    Project     = "Apex-MVP"
  }
}

# Linux Web App
resource "azurerm_linux_web_app" "main" {
  name                = "${var.prefix}-app-${random_string.suffix.result}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      docker {
        registry_url = azurerm_container_registry.main.login_server
        image_name   = var.image_name
        image_tag    = var.image_tag
      }
    }
    always_on = true
  }

  app_settings = {
    "WEBSITES_PORT" = "8080"
    "DOCKER_REGISTRY_SERVER_URL" = azurerm_container_registry.main.login_server
    "DOCKER_REGISTRY_SERVER_USERNAME" = azurerm_container_registry.main.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD" = azurerm_container_registry.main.admin_password
  }

  tags = {
    Environment = "Production"
    Project     = "Apex-MVP"
  }
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "main" {
  name                   = "${var.prefix}-psql-${random_string.suffix.result}"
  resource_group_name    = azurerm_resource_group.main.name
  location               = azurerm_resource_group.main.location
  version                = "14"
  administrator_login    = "psqladmin"
  administrator_password = var.pg_password
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
  tags = {
    Environment = "Production"
    Project     = "Apex-MVP"
  }
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "main" {
  name      = "apexdb"
  server_id = azurerm_postgresql_flexible_server.main.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# PostgreSQL Firewall Rule for Azure Services
resource "azurerm_postgresql_flexible_server_firewall_rule" "azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.main.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}
