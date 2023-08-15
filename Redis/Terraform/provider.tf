
terraform {
  required_providers {
    kubectl = {
      source = "gavinbunney/kubectl"
      version = "~> 1.14.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.8.0"
    }

    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "~> 2.21.1"
    }
  }

  required_version = "~> 1.4"
}


####################################
### Create EKS Cluster providers ###
####################################
# Argocd EKS Cluster
provider "kubectl" {
  apply_retry_count      = 5
  host                   = data.aws_eks_cluster.argocd_eks.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.argocd_eks.certificate_authority[0].data)
  load_config_file       = false
  alias = "argocd_cluster"
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    # This requires the awscli to be installed locally where Terraform is executed
    args = ["eks", "get-token", "--cluster-name", var.argocd_cluster_name]
  }
}
# Main EKS Cluster
provider "kubernetes"  {
    host                   = data.aws_eks_cluster.eks.endpoint
    cluster_ca_certificate = base64decode(data.aws_eks_cluster.eks.certificate_authority[0].data)
    exec {
      api_version = "client.authentication.k8s.io/v1beta1"
      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.eks.name]
      command     = "aws"
    }
    alias = "main"
}

#provider "kubernetes"  {
#    host                   = data.aws_eks_cluster.eks.endpoint
#    cluster_ca_certificate = base64decode(data.aws_eks_cluster.eks_uat.certificate_authority[0].data)
#    exec {
#      api_version = "client.authentication.k8s.io/v1beta1"
#      args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.eks.name]
#      command     = "aws"
#    }
#    alias = "uat"
#}
#####################################
