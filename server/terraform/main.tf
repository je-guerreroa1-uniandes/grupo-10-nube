provider "aws" {
  region     = "us-west-2"
  access_key = var.the-access-key
  secret_key = var.the-secret-key
}

data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "la_maquina" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.micro" # 1vCPU, 1GB RAM, Low to Moderate Network Performance, EBS-Only Storage

  user_data = file("user_data.sh")

  tags = {
    Name = "🚀 producción"
  }
}
