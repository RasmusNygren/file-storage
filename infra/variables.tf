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


# export AWS_REGION=eu-north-1 
# export LAMBDA_FUNCTION_NAME="lambda_fastapi_function"
# export API_NAME="lambda_fastapi"
# export IMAGE_NAME="lambda_fastapi_image"
# export IMAGE_TAG="latest"
