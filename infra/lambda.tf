resource "aws_lambda_function" "lambda_fastapi_function" {
    function_name = local.lambda_function_name

    role = aws_iam_role.iam_for_lambda.arn

    image_uri    = "${aws_ecr_repository.lambda_fastapi_repository.repository_url}:${local.image_version}"
    package_type = "Image"

    # architectures = ["x86_64"]
}


resource "aws_iam_role" "iam_for_lambda" {
    name = "fastapi_iam_for_lambda"

    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "lambda_fastapi_policy_attachement" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_fastapi_policy.arn
}

resource "aws_iam_policy" "lambda_fastapi_policy" {
  name = "my-lambda-fastapi-policy"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    }
  ]
}
EOF
}
