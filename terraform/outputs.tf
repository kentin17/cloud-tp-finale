output "bucket_source_name" {
  value = module.bucket_source.bucket_name
}

output "bucket_destination_name" {
  value = module.bucket_destination.bucket_name
}

output "lambda_function_name" {
  value = module.lambda.function_name
}

output "lambda_function_arn" {
  value = module.lambda.function_arn
}
