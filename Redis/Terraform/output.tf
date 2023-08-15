output "uat_redis_password" {
  value = base64decode(data.kubernetes_resource.uat_redis_secret.object.data.redis-password)
}

output "prod_redis_password" {
  value = base64decode(data.kubernetes_resource.prod_redis_secret.object.data.redis-password)
}