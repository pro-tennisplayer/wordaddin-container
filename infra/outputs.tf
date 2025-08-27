output "resource_group" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

output "acr_login_server" {
  description = "ACR login server URL"
  value       = azurerm_container_registry.main.login_server
}

output "acr_admin_username" {
  description = "ACR admin username"
  value       = azurerm_container_registry.main.admin_username
}

output "acr_admin_password" {
  description = "ACR admin password"
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
}

output "web_app_name" {
  description = "Web app name"
  value       = azurerm_linux_web_app.main.name
}

output "web_app_url" {
  description = "Web app URL"
  value       = azurerm_linux_web_app.main.default_hostname
}

output "postgres_fqdn" {
  description = "PostgreSQL server FQDN"
  value       = azurerm_postgresql_flexible_server.main.fqdn
}

output "postgres_admin_username" {
  description = "PostgreSQL admin username"
  value       = azurerm_postgresql_flexible_server.main.administrator_login
}
