variable aws_profile {
    type = string
    default = "fastapi_lambda"
}


locals {
    image_name = "lambda_fastapi_image"
    image_version = "latest"

    lambda_function_name = "lambda_fastapi_function"

    api_name = "lambda_fastapi"
}
