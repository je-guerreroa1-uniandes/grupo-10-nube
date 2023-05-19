# Esta variable es para la configuración del proyecto donde se va a desplegar la infraestructura.
# Se les asigna valor en el archivo de variables de Terraform, que no se sube a GitHub (terraform.tfvars)
# Y debe incluir las siguiente linea:
# project = ""

variable "project" {
  type        = string
  description = "El proyecto en gcloud al que se van a asociar todos los recursos"
  sensitive   = false
}

variable "credentials_file" {
  type        = string
  description = "El archivo de credenciales del usuario con el que se realiza la configuración"
  default     = "../../../../secure/service-account-key.json"
  sensitive   = true
}

variable "ssh_pub_key_file" {
  type        = string
  description = "Llave publica que se instala en las maquinas de la flota para poder ingresarlas por ssh."
  default     = "../../../../secure/key_prod_rsa.pub"
  sensitive   = true
}

variable "region" {
  type        = string
  description = "La región donde queda la vpc"
  default     = "us-central1"
  sensitive   = false
}

variable "zone" {
  type        = string
  description = "La zona donde queda la vpc"
  default     = "us-central1-a"
  sensitive   = false
}
