# Import EKS Cluster
data "aws_eks_cluster" "eks" {
  name = var.cluster_name
}
# Incase Argocd is installed in a different EKS Cluster
data "aws_eks_cluster" "argocd_eks" {
  name = var.cluster_name
}

## Import EKS VPC
#data "aws_vpc" "eks_vpc" {
#  id = var.vpc_id
#}

## Import EKS Subnet id's - Used to create Fargate Profile
#data "aws_subnets" "eks_private_subnet_ids" {
#filter {
#    name   = "vpc-id"
#    values = [var.vpc_id]
#  }
#
#  tags = {
#    "aws-cdk:subnet-type" = "Private"
#  }
#}

#data "aws_subnet" "eks_example" {
#  for_each = toset(data.aws_subnets.eks_private_subnet_ids.ids)
#  id       = each.value
#}

# Print out cidr blocks doe each subnet
#output "subnet_cidr_blocks" {
#  value = [for s in data.aws_subnet.eks_example : s.cidr_block]
#}


## Print out private subnet ids's with tags "aws-cdk:subnet-type" = "Private"
#output "private_subnet_ids" {
#  value = data.aws_subnets.eks_private_subnet_ids.ids
#}

# Retrieve grafana secret object
data "kubernetes_resource" "uat_redis_secret" {
  provider = kubernetes.main
  depends_on = [ kubectl_manifest.argocd_uat_redis]
  api_version = "v1"
  kind        = "Secret"

  metadata {
    name      = "uat-redis"
    namespace = "uat-redis"
  } 
}

# Retrieve grafana secret object
data "kubernetes_resource" "prod_redis_secret" {
  provider = kubernetes.main
  depends_on = [ kubectl_manifest.argocd_prod_redis]
  api_version = "v1"
  kind        = "Secret"

  metadata {
    name      = "prod-redis"
    namespace = "prod-redis"
  } 
}


## Retrieve prometheus service object
#data "kubernetes_resource" "prometheus_service" {
#  provider = kubernetes.main
#  depends_on = [ kubectl_manifest.argocd_prometheus ]
#  api_version = "v1"
#  kind        = "Service"
#
#  metadata {
#    name      = "prometheus-server"
#    namespace = "monitoring"
#  } 
#}
#
## Retrieve prometheus ingress object
#data "kubernetes_resource" "prometheus_ingress" {
#  provider = kubernetes.main
#  depends_on = [ kubectl_manifest.argocd_prometheus ]
#  api_version = "networking.k8s.io/v1"
#  kind        = "Ingress"
#
#  metadata {
#    name      = "prometheus-server"
#    namespace = "monitoring"
#  } 
#}
#
## Retrieve prometheus ingress object
#data "kubernetes_resource" "grafana_ingress" {
#  provider = kubernetes.main
#  depends_on = [ kubectl_manifest.argocd_grafana ]
#  api_version = "networking.k8s.io/v1"
#  kind        = "Ingress"
#
#  metadata {
#    name      = "grafana"
#    namespace = "monitoring"
#  } 
#}