# Estas dos variables son para la configuración de la cuenta de AWS.
# Se les asigna valor en el archivo de variables de Terraform, que no se sube a GitHub (terraform.tfvars)
# Y debe incluir las siguientes 2 lineas:
# the-access-key = ""
# the-secret-key = ""

variable "the-access-key" {
  type        = string
  description = "La clave de acceso del usuario con el que se realiza la configuración"
  sensitive   = true
}

variable "the-secret-key" {
  type        = string
  description = "La clave secreta del usuario con el que se realiza la configuración"
  sensitive   = true
}
