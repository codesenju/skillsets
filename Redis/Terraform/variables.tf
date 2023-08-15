# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

variable "cluster_name" {
  description = "The name of the EKS cluster"
  type        = string
}

variable "argocd_cluster_name" {
  description = "The name of the cluster where argocd is installed incase is not installed on the same cluster"
  type        = string
}

variable "argocd_dest_server" {
  description = "Destination EKS server managed by argocd"
  type        = string
  default     = "https://kubernetes.default.svc"
}

variable "vpc_id" {
  description = "The VPC ID where EKS resides"
  type        = string
}

variable "argocd_url" {
  type = string
}
variable "argocd_username" {
  type = string
}
variable "argocd_password" {
  type = string
  sensitive = true
}

variable "uat_redis_password" {
  type = string
  sensitive = true
}

variable "prod_redis_password" {
  type = string
  sensitive = true
}