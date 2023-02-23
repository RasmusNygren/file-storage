resource "aws_ecr_repository" "lambda_fastapi_repository" {
    name = local.image_name
    image_tag_mutability = "MUTABLE"
}
