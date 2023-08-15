
# Add oci helm repo to argocd
resource "null_resource" "add_oci_helm_repo" {
  triggers = {
    argocd_url = var.argocd_url
    argocd_username = var.argocd_username
    argocd_password = base64decode(var.argocd_password)
  }
  provisioner "local-exec" {
    on_failure  = fail
    when        = create
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
            argocd login ${self.triggers.argocd_url} --username  ${self.triggers.argocd_username} --password ${self.triggers.argocd_password} && \
            argocd repo add registry-1.docker.io/bitnamicharts --type helm --name bitnami --enable-oci
        EOT
  }

  provisioner "local-exec" {
    on_failure  = fail
    when        = destroy
    interpreter = ["/bin/bash", "-c"]
    command     = <<EOT
             argocd login ${self.triggers.argocd_url} --username   ${self.triggers.argocd_username} --password ${self.triggers.argocd_password}  && \
             argocd repo rm registry-1.docker.io/bitnamicharts
        EOT
  }
}


# Create argocd applicaiton in argocd cluster
resource "kubectl_manifest" "argocd_uat_redis" {
  depends_on = [ null_resource.add_oci_helm_repo ]
  provider = kubectl.argocd_cluster
  yaml_body = <<-YAML
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: uat-redis
  namespace: argocd
  # Add this finalizer ONLY if you want these to cascade delete.
  finalizers:
    - resources-finalizer.argocd.argoproj.io
  labels:
    name: uat-redis
    cluster: ${var.cluster_name}
    tier: database
    iac: terraform
spec:
  project: default
  source:
    repoURL: registry-1.docker.io/bitnamicharts
    targetRevision: 17.15.3
    chart: redis
    helm:
      values: |
        global:
          redis:
            password: ${base64decode("${var.uat_redis_password}")}
        replica:
          replicaCount: 1
  destination:
    name: in-cluster
    namespace: uat-redis
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions: 
    - CreateNamespace=true
  YAML
}




# Create argocd applicaiton in argocd cluster
resource "kubectl_manifest" "argocd_prod_redis" {
  depends_on = [ null_resource.add_oci_helm_repo ]
  provider = kubectl.argocd_cluster
  yaml_body = <<-YAML
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prod-redis
  namespace: argocd
  # Add this finalizer ONLY if you want these to cascade delete.
  finalizers:
    - resources-finalizer.argocd.argoproj.io
  labels:
    name: prod-redis
    cluster: ${var.cluster_name}
    tier: database
    iac: terraform
spec:
  project: default
  source:
    repoURL: registry-1.docker.io/bitnamicharts
    targetRevision: 17.15.3
    chart: redis
    helm:
      values: |
        global:
          redis:
            password: ${base64decode("${var.prod_redis_password}")}
        replica:
          replicaCount: 1
  destination:
    name: in-cluster
    namespace: prod-redis
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions: 
    - CreateNamespace=true
  YAML
}
