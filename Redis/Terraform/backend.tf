# AWS_REGION=$(aws configure get region)
# aws s3 mb s3://terraform-state-k8s-iac --region $AWS_REGION
# https://github.com/terraform-aws-modules/terraform-aws-eks/tree/v14.0.0/examples/irsa
terraform {
  backend "s3" {
    bucket         = "terraform-state-k8s-iac"
    key            = "bitnami-redis.tfstate"
    region         = "us-east-1"
    encrypt        = true
    workspace_key_prefix = "bitnami-redis"
  }
}
