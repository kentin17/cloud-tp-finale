resource "random_id" "suffix" {
  byte_length = 4
}

module "bucket_source" {
  source = "./modules/s3_bucket"
  name   = "ynov-iac-2025-source-${random_id.suffix.hex}"
}

module "bucket_destination" {
  source = "./modules/s3_bucket"
  name   = "ynov-iac-2025-dest-${random_id.suffix.hex}"
}

module "iam" {
  source                  = "./modules/iam"
  source_bucket_arn       = module.bucket_source.bucket_arn
  destination_bucket_arn  = module.bucket_destination.bucket_arn
}

module "lambda" {
  source                   = "./modules/lambda"
  function_name            = "ynov-iac-2025-converter"
  runtime                  = var.lambda_runtime
  role_arn                 = module.iam.lambda_role_arn
  source_bucket_name       = module.bucket_source.bucket_name
  source_bucket_arn        = module.bucket_source.bucket_arn
  destination_bucket_name  = module.bucket_destination.bucket_name
}
