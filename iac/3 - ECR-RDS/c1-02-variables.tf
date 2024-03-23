variable "aws_region" {
  description = "Region in which AWS Resources to be created"
  type = string
  default = "us-east-1"
}

variable "nome_repositorio" {
  description = "Repository Name"
  type = string
  default = "my-food"
}

variable "engine" {
  description = "The database engine"
  type = string
  default = "postgres"
}
variable "allocated_storage" {
  description = "The amount of allocated storage."
  type = number
  default = 20
}
variable "storage_type" {
  description = "type of the storage"
  type = string
  default = "gp2"
}
variable "username" {
  description = "Username for the master DB user."
  default = "databaseteste"
  type = string
}
variable "password" {
  description = "password of the database"
  default = "password"
  type = string
}
variable "instance_class" {
  description = "The RDS instance class"
  default = "db.t3.micro"
  type = string
}

variable "engine_version" {
  description = "The engine version"
  default = "15.4"
  type = number
}
variable "skip_final_snapshot" {
  description = "skip snapshot"
  default = "true"
  type = string
}
variable "identifier" {
  description = "The name of the RDS instance"
  default = "terraform-database-test"
  type = string
}
variable "port" {
  description = "The port on which the DB accepts connections"
  default = "5432"
  type = number
}
variable "name" {
  description = "The database name"
  default = "myfood"
  type = string
}

# VPC Public Subnets
variable "vpc_public_subnets" {
  description = "VPC Public Subnets"
  type = list(string)
  default = ["10.0.101.0/24", "10.0.102.0/24"]
}

# VPC Private Subnets
variable "vpc_private_subnets" {
  description = "VPC Private Subnets"
  type = list(string)
  default = ["10.0.1.0/24", "10.0.2.0/24"]
}
