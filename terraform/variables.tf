variable "aws_region" {
  type    = string
  default = "eu-west-3"
}

variable "role_arn" {
  type = string
}

variable "lambda_runtime" {
  type    = string
  default = "python3.11"
}

variable "pillow_layer_arn" {
  type = string
}
