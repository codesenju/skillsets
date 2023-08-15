
#!/usr/bin/env python3
# Reference:
# - https://ecsworkshop.com/app_mesh/appmesh-implementation/mesh-crystal-app/
# - https://docs.aws.amazon.com/cdk/api/v2/python/index.html

from aws_cdk import (
    CfnParameter,
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_autoscaling as autoscaling,
    aws_iam as iam,
    aws_appmesh as appmesh,
    aws_ecr as ecr,
    aws_ecr_assets as ecr_assets,
    aws_logs as logs,
    aws_servicediscovery as servicediscovery,
    aws_elasticloadbalancingv2 as elbv2,
    aws_ecs_patterns as ecs_patterns,
    aws_efs as efs,
    aws_route53 as route53,
    aws_route53_targets as route54_targets,
    aws_certificatemanager as acm
)
import os
from constructs import Construct
import aws_cdk as cdk
from aws_cdk.aws_ecr_assets import DockerImageAsset
#import  cdk_ecr_deployment  as ecrdeploy

class skillsetsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        skillsets_zone_name = "lmasu.co.za"
        skillsets_fqdn = "ecs-skillsets." + skillsets_zone_name
        # Get environment variable
        account = os.getenv("AWS_ACCOUNT_ID")
        ecs_cluster_name = os.getenv("ECS_CLUSTER_NAME")
        region = os.getenv("AWS_REGION")

        # Import existing VPC
        vpc = ec2.Vpc.from_lookup(
            self, "ImportedVpc",
            vpc_name='VpcInfraStack/ApiProjectVpc'
        )
        # Create security group
        skillsets_sg = ec2.SecurityGroup(self, "skillsets_sg",vpc=vpc,security_group_name="skillsets_sg",allow_all_outbound=False)
        #redis_sg = ec2.SecurityGroup(self, "redis_sg",vpc=vpc,security_group_name="redis_sg",allow_all_outbound=False)
        redis_efs_SGID = ec2.SecurityGroup(self, "redis_efs_SGID",vpc=vpc,security_group_name="redis_efs_SGID",allow_all_outbound=False)
        # Import Security groups
        security_group = ec2.SecurityGroup.from_security_group_id(self,"ImporteDefaultApiClusterSG",security_group_id=cdk.Fn.import_value("DefaultAPIClusterSG"))
        elb_SG = ec2.SecurityGroup.from_security_group_id(self,"importedelbSG",security_group_id=cdk.Fn.import_value("elbSGID")) 

        # Security group rules
        #skillsets_sg.add_egress_rule(redis_sg,ec2.Port.tcp(6379),description="Allow outbound traffic to redis.")
        skillsets_sg.add_egress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(443),description="Allow outbound traffic HTTPS to the world")
        #redis_sg.add_ingress_rule(redis_sg,ec2.Port.tcp(6379),description="Allow inbound traffic from skillsets.")
        elb_SG.add_egress_rule(skillsets_sg,ec2.Port.tcp(5000),description="Allow traffic to skillsets target on port 5000.")
        elb_SG.add_egress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(443),description="Allow outbound traffic HTTPS to the world")
        skillsets_sg.add_ingress_rule(elb_SG,ec2.Port.tcp(5000),description="Allow inbound traffic from ELB.")
        skillsets_sg.add_egress_rule(redis_efs_SGID,ec2.Port.tcp(2049),description="Allow outbond traffic  to EFS on port 2049")
        redis_efs_SGID.add_ingress_rule(ec2.Peer.any_ipv4(),ec2.Port.tcp(2049),description="Allow inbound  traffic NFS from vpc cidr block.")
        
        # Import IAM task execution role
        existing_task_execution_role_name = "ecsTaskExecutionRole" 
        existing_task_execution_role_arn = f'arn:aws:iam::{account}:role/{existing_task_execution_role_name}'
        task_execution_role = iam.Role.from_role_arn(self, 'ImportedTaskExecutionRole', role_arn=existing_task_execution_role_arn)


        # Import IAM task role
        existing_task_role_name = "000A_ecsExecTaskRole"
        existing_task_role_arn = f'arn:aws:iam::{account}:role/{existing_task_role_name}'
        task_role = iam.Role.from_role_arn(self, 'ImportedEcsExecTaskRole', role_arn=existing_task_role_arn)

        ### Adding policies to Task Role ##
        #task_role.add_managed_policy(policy=iam.ManagedPolicy.from_aws_managed_policy_name("AWSAppMeshEnvoyAccess"))
        #task_role.add_managed_policy(policy=iam.ManagedPolicy.from_aws_managed_policy_name("AWSXRayDaemonWriteAccess"))
       
        ## Import Namespace api.local from EcsClusterStack ooutputs
        api_namespace= servicediscovery.PrivateDnsNamespace.from_private_dns_namespace_attributes(self, "ImportedNamespace",
            namespace_arn= cdk.Fn.import_value("ApiNamespaceArn"),
            namespace_id=cdk.Fn.import_value("ApiNamespaceId"),
            namespace_name=cdk.Fn.import_value("ApiNamespaceName"),
        )

        # Import ECS Cluster
        cluster = ecs.Cluster.from_cluster_attributes(self, "ImportedCluster",
            cluster_name=f"{ecs_cluster_name}",
            security_groups=[security_group],
            vpc=vpc,
            default_cloud_map_namespace=api_namespace
            
        )
        
        # Create the EFS file system
        efs_file_system = efs.FileSystem(self, "redis_EFSFileSystem",
        vpc=vpc,
        security_group=redis_efs_SGID,
        vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
        removal_policy=cdk.RemovalPolicy.DESTROY
        )
        
        ###################################
        ## Create the App Mesh resources ##
        ###################################
        ## Redis ##
        # Import mesh
        mesh = appmesh.Mesh.from_mesh_arn(self,"ImportedEcsApiMesh",mesh_arn=cdk.Fn.import_value("EcsApiMeshArn"))
        ## Virtual Node ##
        redis_node = appmesh.VirtualNode(self, "redis",
            mesh=mesh,
            service_discovery=appmesh.ServiceDiscovery.dns("redis.api.local"),
            listeners=[appmesh.VirtualNodeListener.tcp(
                #port=6379,
                #health_check=appmesh.HealthCheck.tcp(
                #    healthy_threshold=3,
                #    interval=cdk.Duration.seconds(12),
                #    timeout=cdk.Duration.seconds(10),
                #    unhealthy_threshold=2
                #),
                #timeout=appmesh.TcpTimeout(
                #    idle=cdk.Duration.seconds(10)
                #)
            )],
            access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
            virtual_node_name="redis-node"
        )
        ## Virtual Service ##
        redis_virtual_service = appmesh.VirtualService(self, "redisVirtualService",
            virtual_service_provider=appmesh.VirtualServiceProvider.virtual_node(redis_node),
            virtual_service_name="redis" + "." + api_namespace.namespace_name
        )

        ## Skillsets ##
        # Import index virtual service
        index_virtual_service = appmesh.VirtualService.from_virtual_service_attributes(self,"ImportedindexVirtualService",mesh=mesh,virtual_service_name="index.api.local")
        ## Virtual Node ##
        skillsets_node = appmesh.VirtualNode(self, "node",
            mesh=mesh,
            service_discovery=appmesh.ServiceDiscovery.dns("skillsets.api.local"),
            listeners=[appmesh.VirtualNodeListener.http(
                port=5000,
                health_check=appmesh.HealthCheck.http(
                    healthy_threshold=3,
                    interval=cdk.Duration.seconds(35),
                    path="/healthz",
                    timeout=cdk.Duration.seconds(30),
                    unhealthy_threshold=2
                ),
                timeout=appmesh.HttpTimeout(
                    idle=cdk.Duration.seconds(30)
                )
            )],
            access_log=appmesh.AccessLog.from_file_path("/dev/stdout"),
            backends=[appmesh.Backend.virtual_service(redis_virtual_service)],
            virtual_node_name="skillsets-node"
        )
        ## Virtual Service ##
        skillsets_virtual_service = appmesh.VirtualService(self, "skillsetsVirtualService",
            virtual_service_provider=appmesh.VirtualServiceProvider.virtual_node(skillsets_node),
            virtual_service_name="skillsets" + "." + api_namespace.namespace_name
        )

#        #######################
#        ## redis SERVICE ##
#        #######################
#        redis_task_definition = ecs.TaskDefinition(self, "redisTaskDef",
#        execution_role=task_execution_role, 
#        task_role=task_role,
#        network_mode=ecs.NetworkMode.AWS_VPC, # I need to investigate why bridge network mode is giving me issues - I keep getting task failed ELB health checks
#        compatibility=ecs.Compatibility.EC2_AND_FARGATE,
#        cpu="1024",
#        memory_mib="2048",
#        # Frgate runtime settings
#        #runtime_platform=ecs.RuntimePlatform(                          # FOR FARGATE
#        #    operating_system_family=ecs.OperatingSystemFamily.LINUX,
#        #    cpu_architecture=ecs.CpuArchitecture.ARM64
#        #    ),
#        #
#        #########################
#        ## appmesh-proxy-start ##
#        proxy_configuration=ecs.AppMeshProxyConfiguration( 
#            container_name="envoy", #App Mesh side card that will proxy the requests 
#            properties=ecs.AppMeshProxyConfigurationProps(
#                app_ports=[6379], # redis application port
#                proxy_ingress_port=15000, # side card default config
#                proxy_egress_port=15001, # side card default config
#                egress_ignored_i_ps=["169.254.170.2","169.254.169.254"], # side card default config
#                ignored_uid=1337 # side card default config
#            )
#        )
#        # appmesh-proxy-end ##
#        #######################
#        )
#
#        ## Image ##
#        # ECR
#        # redis_repo = ecr.Repository.from_repository_name(self,"redisRepo",repository_name="redis.api.local")
#
#        # Create log group for container logs
#        logGroup = logs.LogGroup(self,"redisLogGroup",
#            log_group_name="/ecs/api/redis",
#            retention=logs.RetentionDays.ONE_WEEK,
#            removal_policy=cdk.RemovalPolicy.DESTROY
#        )
#
#        ## Container ##
#        redis_container = redis_task_definition.add_container("redis",
#           image=ecs.ContainerImage.from_registry("redis:7"),
#           # ECR
#           #image=ecs.ContainerImage.from_ecr_repository(redis_repo),
#           logging=ecs.LogDrivers.aws_logs(stream_prefix="redis-container",log_group=logGroup),
#           memory_reservation_mib=512,
#           #cpu=256,
#           container_name="redis", 
#           
#       )
#        
#        ## Port Mapping ##
#        redis_container.add_port_mappings(ecs.PortMapping(container_port=6379,name="redis"))
#        ########################################################
#        ## App Mesh envoy proxy container configuration START ##
#        redis_envoy_container = redis_task_definition.add_container(
#            "redisServiceProxyContDef",
#            image=ecs.ContainerImage.from_registry("public.ecr.aws/appmesh/aws-appmesh-envoy:v1.15.1.0-prod"),
#            #image=ecs.ContainerImage.from_registry("public.ecr.aws/appmesh/aws-appmesh-envoy:arm64-v1.24.1.0-prod"),
#            container_name="envoy",
#            memory_reservation_mib=256,
#            #cpu=256,
#            environment={
#                "AWS_REGION": region,
#                "ENVOY_LOG_LEVEL": "debug",
#                "ENABLE_ENVOY_STATS_TAGS": "1",
#                "ENABLE_ENVOY_XRAY_TRACING": "1",
#                "APPMESH_RESOURCE_ARN": redis_node.virtual_node_arn
#            },
#            essential=True,
#            logging=ecs.LogDriver.aws_logs(
#                stream_prefix='/envoy-container',
#                log_group=logGroup
#            ),
#            health_check=ecs.HealthCheck(
#                interval=cdk.Duration.seconds(12),
#                timeout=cdk.Duration.seconds(10),
#                retries=10,
#                command=["CMD-SHELL","curl -s http://localhost:9901/server_info | grep state | grep -q LIVE"],
#            ),
#            user="1337"
#        )
#        
#        redis_envoy_container.add_ulimits(ecs.Ulimit(
#            hard_limit=1048576, # case replication - 12040857631
#            name=ecs.UlimitName.NOFILE,
#            soft_limit=524288 # case replication - 12040857631
#            )
#        )
#    
#        ### Primary container needs to depend on envoy before it can be reached out
#        redis_container.add_container_dependencies(ecs.ContainerDependency(
#               container=redis_envoy_container,
#               condition=ecs.ContainerDependencyCondition.HEALTHY
#           )
#        )
#        # App Mesh envoy proxy container configuration END ##
#        ######################################################
#
#        # Enable app mesh Xray observability
#        #ammmesh-xray-uncomment
#        redis_xray_container = redis_task_definition.add_container(
#             "redisXrayContainer",
#             image=ecs.ContainerImage.from_registry("amazon/aws-xray-daemon"),
#             logging=ecs.LogDriver.aws_logs(
#                 stream_prefix='/xray-container',
#                 log_group=logGroup
#             ),
#             essential=True,
#             container_name="xray",
#             memory_reservation_mib=512,
#             #cpu=256,
#             user="1337",
#            environment={
#                "AWS_REGION": region,
#            },
#         )
#    
#        redis_envoy_container.add_container_dependencies(ecs.ContainerDependency(
#               container=redis_xray_container,
#               condition=ecs.ContainerDependencyCondition.START
#           )
#         )
#        #ammmesh-xray-uncomment
#
#        ## Otel Container - START ##
#        redis_otel_container = redis_task_definition.add_container(
#             "redisOtelContainer",
#             image=ecs.ContainerImage.from_registry("codesenju/aws-otel-collector:amd"),
#             logging=ecs.LogDriver.aws_logs(
#                 stream_prefix='/otel-container',
#                 log_group=logGroup
#             ),
#             essential=True,
#             container_name="otel",
#             memory_reservation_mib=512,
#             #cpu=256,
#            environment={
#                "AWS_REGION": region,
#                "AWS_PROMETHEUS_ENDPOINT": "https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-5f8b1530-3388-4177-82af-eae1c6d54d57/api/v1/remote_write"
#            },
#            command=["--config=/etc/ecs/otel-config.yaml"]
#         )
#        ## Otel Container - END ##
#        
#        ## Service ##
#        redis_service = ecs.Ec2Service(self, "redisService",
#            cluster=cluster,
#            task_definition=redis_task_definition,
#            security_groups=[redis_sg], # - RuntimeError: vpcSubnets, securityGroup(s) and assignPublicIp can only be used in AwsVpc networking mode
#            enable_execute_command=True,
#            capacity_provider_strategies=[ecs.CapacityProviderStrategy(
#               # capacity_provider="spot-api-capasity-provider", 
#                capacity_provider="amd-spot-api-capasity-provider", 
#                weight=1,
#                
#            )],
#            service_name="redis",
#        )
#        ## Cloud Map
#        redis_service.enable_cloud_map(name="redis")
#
        
        #######################
        ## skillsets SERVICE ##
        #######################
        ## Volume ##
        redis_volume = ecs.Volume(name="REDIS_DATA",efs_volume_configuration={
                   "file_system_id": efs_file_system.file_system_id
        }
        
        )
        ## EFS mount point ##
        redis_efs_mount_point = ecs.MountPoint(source_volume=redis_volume.name, 
                                        container_path="/data",
                                        read_only=False)



        skillsets_task_definition = ecs.TaskDefinition(self, "skillsetsTaskDef",
        execution_role=task_execution_role, 
        task_role=task_role,
        network_mode=ecs.NetworkMode.AWS_VPC, # I need to investigate why bridge network mode is giving me issues - I keep getting task failed ELB health checks
        compatibility=ecs.Compatibility.EC2_AND_FARGATE,
        cpu="1024",
        memory_mib="3072",
        volumes=[redis_volume],
        # Frgate runtime settings
        #runtime_platform=ecs.RuntimePlatform(                          # FOR FARGATE
        #    operating_system_family=ecs.OperatingSystemFamily.LINUX,
        #    cpu_architecture=ecs.CpuArchitecture.ARM64
        #    ),
        #
        #########################
        ## appmesh-proxy-start ##
        proxy_configuration=ecs.AppMeshProxyConfiguration( 
            container_name="envoy", #App Mesh side card that will proxy the requests 
            properties=ecs.AppMeshProxyConfigurationProps(
                app_ports=[5000], # skillsets application port
                proxy_ingress_port=15000, # side card default config
                proxy_egress_port=15001, # side card default config
                egress_ignored_i_ps=["169.254.170.2","169.254.169.254"], # side card default config
                ignored_uid=1337 # side card default config
            )
        )
        # appmesh-proxy-end ##
        #######################
        )

        ## Image ##
        # ECR
        # skillsets_repo = ecr.Repository.from_repository_name(self,"skillsetsRepo",repository_name="skillsets.api.local")

        # Create log group for container logs
        logGroup = logs.LogGroup(self,"skillsetsLogGroup",
            log_group_name="/ecs/api/skillsets",
            retention=logs.RetentionDays.ONE_WEEK,
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        ## Container ##
        skillsets_container = skillsets_task_definition.add_container("skillsets",
           image=ecs.ContainerImage.from_registry("codesenju/skillsets"),
           # ECR
           #image=ecs.ContainerImage.from_ecr_repository(skillsets_repo),
           logging=ecs.LogDrivers.aws_logs(stream_prefix="skillsets-container",log_group=logGroup),
           memory_reservation_mib=512,
           #cpu=256,
           container_name="skillsets", 
            environment={
                "REDIS_HOST": "localhost",
                "REDIS_PORT": "6379"
            },
           
       )

        
        ## Port Mapping ##
        skillsets_container.add_port_mappings(ecs.PortMapping(container_port=5000,name="skillsets",host_port=5000))
        ## Redis container ##
        #
        ## Container ##
        redis_container = skillsets_task_definition.add_container("redis",
           image=ecs.ContainerImage.from_registry("redis:7"),
           # ECR
           #image=ecs.ContainerImage.from_ecr_repository(redis_repo),
           logging=ecs.LogDrivers.aws_logs(stream_prefix="redis-container",log_group=logGroup),
           memory_reservation_mib=512,
           #cpu=256,
           container_name="redis",
           command=["redis-server","--save","60","1","--loglevel","debug"]
           
       )
        # Add mount point
        redis_container.add_mount_points(redis_efs_mount_point)
        
        ## Port Mapping ##
        redis_container.add_port_mappings(ecs.PortMapping(container_port=6379,name="redis"))

        ########################################################
        ## App Mesh envoy proxy container configuration START ##
        skillsets_envoy_container = skillsets_task_definition.add_container(
            "skillsetsServiceProxyContDef",
            image=ecs.ContainerImage.from_registry("public.ecr.aws/appmesh/aws-appmesh-envoy:v1.15.1.0-prod"),
            #image=ecs.ContainerImage.from_registry("public.ecr.aws/appmesh/aws-appmesh-envoy:arm64-v1.24.1.0-prod"),
            container_name="envoy",
            memory_reservation_mib=256,
            #cpu=256,
            environment={
                "AWS_REGION": region,
                "ENVOY_LOG_LEVEL": "debug",
                "ENABLE_ENVOY_STATS_TAGS": "1",
                "ENABLE_ENVOY_XRAY_TRACING": "1",
                "APPMESH_RESOURCE_ARN": skillsets_node.virtual_node_arn,
                "APPMESH_METRIC_EXTENSION_VERSION": "1"
            },
            essential=True,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix='/envoy-container',
                log_group=logGroup
            ),
            health_check=ecs.HealthCheck(
                interval=cdk.Duration.seconds(35),
                timeout=cdk.Duration.seconds(30),
                retries=10,
                command=["CMD-SHELL","curl -s http://localhost:9901/server_info | grep state | grep -q LIVE"],
            ),
            user="1337"
        )
        
        skillsets_envoy_container.add_ulimits(ecs.Ulimit(
            hard_limit=1048576, # case replication - 12040857631
            name=ecs.UlimitName.NOFILE,
            soft_limit=524288 # case replication - 12040857631
            )
        )
    
        ### Primary container needs to depend on envoy before it can be reached out
        skillsets_container.add_container_dependencies(ecs.ContainerDependency(
               container=skillsets_envoy_container,
               condition=ecs.ContainerDependencyCondition.HEALTHY
           )
        )
        # App Mesh envoy proxy container configuration END ##
        ######################################################

        # Enable app mesh Xray observability
        #ammmesh-xray-uncomment
        skillsets_xray_container = skillsets_task_definition.add_container(
             "skillsetsXrayContainer",
             image=ecs.ContainerImage.from_registry("amazon/aws-xray-daemon"),
             logging=ecs.LogDriver.aws_logs(
                 stream_prefix='/xray-container',
                 log_group=logGroup
             ),
             essential=True,
             container_name="xray",
             memory_reservation_mib=512,
             #cpu=256,
             user="1337",
            environment={
                "AWS_REGION": region,
            },
         )
    
        skillsets_envoy_container.add_container_dependencies(ecs.ContainerDependency(
               container=skillsets_xray_container,
               condition=ecs.ContainerDependencyCondition.START
           )
         )
        #ammmesh-xray-uncomment

        ## Otel Container - START ##
        skillsets_otel_container = skillsets_task_definition.add_container(
             "skillsetsOtelContainer",
             image=ecs.ContainerImage.from_registry("codesenju/aws-otel-collector:case"),
             logging=ecs.LogDriver.aws_logs(
                 stream_prefix='/otel-container',
                 log_group=logGroup
             ),
             essential=True,
             container_name="otel",
             memory_reservation_mib=512,
             #cpu=256,
            environment={
                "AWS_REGION": region,
                "AWS_PROMETHEUS_ENDPOINT": "https://aps-workspaces.us-east-1.amazonaws.com/workspaces/ws-5f8b1530-3388-4177-82af-eae1c6d54d57/api/v1/remote_write"
            },
            command=["--config=/etc/ecs/otel-config.yaml"]
         )
        ## Otel Container - END ##
        
        ## Service ##
        #skillsets_service = ecs.Ec2Service(self, "skillsets",
        skillsets_service = ecs.FargateService(self, "skillsets",
            cluster=cluster,
            task_definition=skillsets_task_definition,
            security_groups=[skillsets_sg], # - RuntimeError: vpcSubnets, securityGroup(s) and assignPublicIp can only be used in AwsVpc networking mode
            enable_execute_command=True,
            capacity_provider_strategies=[ecs.CapacityProviderStrategy(
               # capacity_provider="amd-spot-api-capasity-provider", 
                capacity_provider="FARGATE", 
                weight=1,
            )],
            service_name="skillsets",
            health_check_grace_period=cdk.Duration.seconds(5000)

        )

        ###################################
        ## LOADBALANCING & ASUTO SCALING ##
        ###################################
        # Import the certificate
        certificate = acm.Certificate.from_certificate_arn( self,"Certificate", os.getenv("CERT_ARN"))

        # Create ALB
        skillsets_load_balancer = elbv2.ApplicationLoadBalancer(self, "skillsetsLoadBalancer",vpc=vpc, internet_facing=True,security_group=elb_SG)
        
        # Add an HTTP listener
        skillsets_listener = skillsets_load_balancer.add_listener("skillsetsListener",port=80)
        # Add a target group for the HTTP listener with a rule for the Host header
        skillsets_targetGroup = skillsets_listener.add_targets("skillsetsTargets",
                                                               targets=[skillsets_service],
                                                               protocol=elbv2.ApplicationProtocol.HTTP,
                                                               priority=1,
                                                               conditions=[elbv2.ListenerCondition.host_headers([skillsets_fqdn])])
        
        skillsets_targetGroup.configure_health_check(path="/healthz")

        # Add an HTTPS listener
        https_listener = skillsets_load_balancer.add_listener("HTTPSListener", port=443, certificates=[certificate])
        # Add a target group for the HTTPS listener with a rule for the Host header
        https_target_group = https_listener.add_targets("HTTPSTargets",
                                   targets=[skillsets_service],
                                   protocol=elbv2.ApplicationProtocol.HTTPS,
                                   priority=1, 
                                   conditions=[elbv2.ListenerCondition.host_headers([skillsets_fqdn])])
        https_target_group.configure_health_check(path="/healthz")
        https_listener.add_target_groups("HTTPSTargetGroup",target_groups=[https_target_group])
       
        # Add a redirect from HTTP to HTTPS
        skillsets_listener.add_action("Redirect", action=elbv2.ListenerAction.redirect(port="443", protocol="HTTPS"))
    
        ## AutoScaling for skillsets ##
        scaling_skillsets = skillsets_service.auto_scale_task_count(max_capacity=10)
        scaling_skillsets.scale_on_cpu_utilization("CpuScaling",
            target_utilization_percent=80
        )
        scaling_skillsets.scale_on_memory_utilization("MemoryScaling",
            target_utilization_percent=80
        )

        # Creates an A Recod and associates it with skillsets_load_balancer
        #os.getenv("HOSTED_ZONE_ID")
        full_hosted_zone_id = os.popen("aws route53 list-hosted-zones-by-name --dns-name 'lmasu.co.za' --query 'HostedZones[].Id' --out text").read()
        # This code splits the input string at each occurrence of the ‘/’ character and takes the last element of the resulting list, which is the desired substring
        # Using strip()to remove both leading and trailing whitespace 
        hosted_zone_id = full_hosted_zone_id.split('/')[-1].strip() 

        zone = route53.PublicHostedZone.from_public_hosted_zone_attributes(self,"ImportedHostedZone",zone_name=skillsets_zone_name,hosted_zone_id=hosted_zone_id)
        skillsets_record = route53.ARecord(self, "SkillsetsRecord",
            zone=zone,
            target=route53.RecordTarget.from_alias(route54_targets.LoadBalancerTarget(skillsets_load_balancer)),
            record_name=skillsets_fqdn
        )
        ## OUTPUT ###
        # Output the ARN of the ECS service to use in other Stacks.
        # - https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/CfnOutput.html

        cdk.CfnOutput(self,"SkillsetsElbEndpoint",export_name="SkillsetsElbEndpoint",value=skillsets_load_balancer.load_balancer_dns_name)
        cdk.CfnOutput(self,"SkillsetsRecordDNSName",export_name="SkillsetsRecordDNSName",value=skillsets_record.domain_name)

app=cdk.App()
skillsetsStack(app, "skillsetsStack", env=cdk.Environment(account=os.getenv("AWS_ACCOUNT_ID"), region=os.getenv("AWS_REGION")),)
app.synth()