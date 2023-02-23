resource "aws_api_gateway_rest_api" "lambda_fastapi" {
  name        = local.api_name
}

resource "aws_api_gateway_resource" "resource" {
    rest_api_id = aws_api_gateway_rest_api.lambda_fastapi.id
    parent_id = aws_api_gateway_rest_api.lambda_fastapi.root_resource_id
    path_part = "{proxy+}"
}

resource "aws_api_gateway_method" "method" {
    rest_api_id = aws_api_gateway_rest_api.lambda_fastapi.id
    resource_id = aws_api_gateway_resource.resource.id
    http_method = "ANY"
    authorization = "NONE"
}

resource "aws_api_gateway_integration" "integration" {
    rest_api_id = aws_api_gateway_rest_api.lambda_fastapi.id
    resource_id = aws_api_gateway_method.method.resource_id
    http_method = aws_api_gateway_method.method.http_method

    integration_http_method = "POST"
    type = "AWS_PROXY"
    uri = aws_lambda_function.lambda_fastapi_function.invoke_arn
}


# Handling root paths
resource "aws_api_gateway_method" "method_root" {
  rest_api_id   = aws_api_gateway_rest_api.lambda_fastapi.id
  resource_id   = aws_api_gateway_rest_api.lambda_fastapi.root_resource_id
  http_method   = "ANY"
  authorization = "NONE"
}


resource "aws_api_gateway_integration" "integration_root" {
  rest_api_id = aws_api_gateway_rest_api.lambda_fastapi.id
  resource_id = aws_api_gateway_method.method_root.resource_id
  http_method = aws_api_gateway_method.method_root.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.lambda_fastapi_function.invoke_arn
}

# Deployment
resource "aws_api_gateway_deployment" "lambda_fastapi_deployment" {
   depends_on = [
     aws_api_gateway_integration.integration,
     aws_api_gateway_integration.integration_root,
   ]

   rest_api_id = aws_api_gateway_rest_api.lambda_fastapi.id
   stage_name  = "fastapi"

   # added to stream changes
   stage_description = "deployed at ${timestamp()}"

   lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_permission" "lambda_fastapi_permission" {
   statement_id  = "AllowAPIGatewayInvoke"
   action        = "lambda:InvokeFunction"
   function_name = aws_lambda_function.lambda_fastapi_function.function_name
   principal     = "apigateway.amazonaws.com"

   # The "/*/*" portion grants access from any method on any resource
   # within the API Gateway REST API.
   source_arn = "${aws_api_gateway_rest_api.lambda_fastapi.execution_arn}/*/*"
}

output "endpoint_url" {
  value = aws_api_gateway_deployment.lambda_fastapi_deployment.invoke_url
}
