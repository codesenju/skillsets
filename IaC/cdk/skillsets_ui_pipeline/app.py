
#!/usr/bin/env python3
# Reference:
# - https://ecsworkshop.com/app_mesh/appmesh-implementation/mesh-crystal-app/
# - https://docs.aws.amazon.com/cdk/api/v2/python/index.html
# - https://catalog.us-east-1.prod.workshops.aws/workshops/d93fec4c-fb0f-4813-ac90-758cb5527f2f/en-US/walkthrough
import boto3
import subprocess
from os import path
from aws_cdk import (
    CfnParameter,
    Stack,
    aws_codebuild as codebuild,
    aws_codecommit as codecommit,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_eks as eks,
    aws_secretsmanager as secretsmanager,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions
)

import os, json
from constructs import Construct
import aws_cdk as cdk
#from aws_cdk.aws_ecr_assets import DockerImageAsset
#import  cdk_ecr_deployment  as ecrdeploy

class pipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        #############################
        ### Environment Variables ###
        #############################
        # ENV = os.getenv("ENV","dev") # Will also be the prefix of the applicaiton
        ARGOCD_CLUSTER_NAME =  os.getenv("ARGOCD_CLUSTER_NAME","in-cluster") # Argocd cluster name where the applicaiton will be deployed
        EKS_CLUSTER_NAME = os.getenv("EKS_CLUSTER_NAME","uat")
        APP_NAME="skillsets-ui" # Don't forget to change the name of the pipelineStack bellow!
        APP_ENDPOINT="https://uat-skillsets-ui.lmasu.co.za/api/engineers"
        AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID"),
        AWS_REGION = os.getenv("AWS_REGION")
        DOCKER_PASSWORD=os.getenv("DOCKER_PASSWORD")
        DOCKER_USERNAME=os.getenv("DOCKER_USERNAME")
        ARGOCD_USERNAME=os.getenv("ARGOCD_USERNAME")
        ARGOCD_PASSWORD=os.getenv("ARGOCD_PASSWORD")
        ARGOCD_SERVER=os.getenv("ARGOCD_SERVER")
        CODECOMMIT_PASSWORD=os.getenv("CODECOMMIT_PASSWORD")
        CODECOMMIT_USERNAME=os.getenv("CODECOMMIT_USERNAME")
        DEST_SERVER=os.getenv("DEST_SERVER","https://kubernetes.default.svc")
        REPOSITORY_URI=f"%s.dkr.ecr.{AWS_REGION}.amazonaws.com/iac-{APP_NAME}" % (AWS_ACCOUNT_ID)
        EKS_KUBECTL_ROLE_ARN="arn:aws:iam::%s:role/EksCodeBuildKubectlRole" % (AWS_ACCOUNT_ID)
        APP_PATH="../../../frontend"
        K8S_PATH="../../../kustomize.ui" 
        # Skip secret creation it's already created in api stack       
        #####################
        ### SecretManager ###
        #####################
        ## Create docker secrets from local environments
        #secret = secretsmanager.Secret(self, f"iac_{APP_NAME}_docker_secret",
        #    secret_name="iac-my-docker-secret",
        #         secret_object_value={
        #    "username": cdk.SecretValue.unsafe_plain_text(DOCKER_USERNAME),
        #    "password": cdk.SecretValue.unsafe_plain_text(DOCKER_PASSWORD)
        #}
        #)

        ## Create codecommmit secrets from local environments
        #secret = secretsmanager.Secret(self, f"iac_{APP_NAME}_codecommit_secret",
        #    secret_name="iac-my-codecommit-secret",
        #         secret_object_value={
        #    "username": cdk.SecretValue.unsafe_plain_text(CODECOMMIT_USERNAME),
        #    "password": cdk.SecretValue.unsafe_plain_text(CODECOMMIT_PASSWORD)
        #}
        #)

        ## Creates argocd secrets from local environments
        #secret = secretsmanager.Secret(self, f"iac_{APP_NAME}_argocd_secret",
        #    secret_name="iac-my-argocd-secret",
        #         secret_object_value={
        #    "username": cdk.SecretValue.unsafe_plain_text(ARGOCD_USERNAME),
        #    "password": cdk.SecretValue.unsafe_plain_text(ARGOCD_PASSWORD),
        #    "server": cdk.SecretValue.unsafe_plain_text(ARGOCD_SERVER)
        #}
        #)

        #####################
        ### IAM Resources ###
        #####################
        # Creates a policy document for CodeBuild role bellow
        my_secretmanager_policy_document = iam.PolicyDocument(
            statements=[
                iam.PolicyStatement(
                    actions=["secretsmanager:GetSecretValue"],
                    resources=["*"]
                )
            ]
        )

        # Creates a role for CodeBuild
        role = iam.Role(self,f"iac_{APP_NAME}_codebuild_role",
           assumed_by=iam.ServicePrincipal("codebuild.amazonaws.com"),
           # custom description if desired
           description=f"Codebuild {APP_NAME} role",
           managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeBuildAdminAccess"),
                             iam.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2ContainerRegistryPowerUser"),
                             iam.ManagedPolicy.from_aws_managed_policy_name("AWSCodeCommitPowerUser"),
                             ],

            role_name=f"001_IaC_{APP_NAME}_codebuild_role",
            inline_policies={
               "my_secretsmanager_policy": my_secretmanager_policy_document
            }
        )       

        # Creates ECR repository
        ecr_repo = ecr.Repository(self, f"iac_{APP_NAME}_repository",
            image_scan_on_push=True,
            repository_name=f"iac-{APP_NAME}",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )

        ##################
        ### CodeCommit ###
        ##################
        # Creates Codecommit repository from local directory for the applicaiton
        app_repo = codecommit.Repository(self, f"iac_{APP_NAME}_app_repository", 
        repository_name=f"iac-{APP_NAME}",
        code=codecommit.Code.from_directory(APP_PATH)
        )

        # Creates Codecommit repository from local directory for k8s manifest files
        k8s_repo = codecommit.Repository(self, f"iac_{APP_NAME}_k8s_repository", 
        repository_name=f"iac-{APP_NAME}-k8s-manifests",
        code=codecommit.Code.from_directory(K8S_PATH)
        )

        ####################
        ### CodeBuild CI ###
        ####################
        # Creates Codebuild Project for CI Pipeline
        ci_pipeline = codebuild.Project(self, f"iac_{APP_NAME}_codebuildproject_ci",
            project_name=f"IaC-{APP_NAME}-ci",
            description="CodeBuild Project for EKS DevOps CI Pipeline",
            build_spec=codebuild.BuildSpec.from_source_filename("buildspec.yaml "),
            role=role,
            environment=codebuild.BuildEnvironment(
            environment_variables={
                "REPOSITORY_URI": codebuild.BuildEnvironmentVariable(
                    value=REPOSITORY_URI
                ),
                "EKS_KUBECTL_ROLE_ARN": codebuild.BuildEnvironmentVariable(
                    value=EKS_KUBECTL_ROLE_ARN
                ),
                "EKS_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=EKS_CLUSTER_NAME
                ),
                "ARGOCD_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=ARGOCD_CLUSTER_NAME
                ),
                "ENV": codebuild.BuildEnvironmentVariable(
                    value="dev"
                ),
                "APP_NAME": codebuild.BuildEnvironmentVariable(
                    value=APP_NAME
                ),
                "DEST_SERVER": codebuild.BuildEnvironmentVariable(
                    value=DEST_SERVER
                )
            },
            privileged=True, 
            compute_type=codebuild.ComputeType.SMALL,
            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
            ),
            source=codebuild.Source.code_commit(repository=app_repo),
            secondary_sources=[codebuild.Source.code_commit(repository=k8s_repo,identifier="K8S")]
        )

        # Creates Codebuild Project for dev CD Pipeline
        cd_pipeline_dev = codebuild.Project(self, f"iac_{APP_NAME}_codebuildproject_cd_dev",
            project_name=f"IaC-{APP_NAME}-cd-dev",
            description="CodeBuild Project for EKS DevOps DEV CD Pipeline",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "env": {
                    "git-credential-helper": "yes"
                },
                "phases": {
                    "install": {
                        "commands":[
                                    "echo \"Install kustomize cli...\"",
                                    "curl -sLo /tmp/kustomize.tar.gz  https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.0.3/kustomize_v5.0.3_linux_amd64.tar.gz",
                                    "tar xzvf /tmp/kustomize.tar.gz -C /usr/bin/ && chmod +x /usr/bin/kustomize && rm -rf /tmp/kustomize.tar.gz",
                                    "kustomize version",
                                    "echo \"Install ARGOCD cli & Authenticate with ARGOCD SERVER...\"",
                                    "curl -sLo /usr/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.7.2/argocd-linux-amd64 && chmod +x /usr/bin/argocd",
                                    "argocd version --client",
                                   ]
                    },
                      "pre_build": {
                        "commands": [
                                    "echo \"Authenticate with Argocd Server...\"",
                                    "ARGOCD_CREDS=$(aws secretsmanager get-secret-value --secret-id iac-my-argocd-secret --query SecretString --output text)",
                                    "ARGOCD_USERNAME=$(echo $ARGOCD_CREDS | jq -r .username)",
                                    "ARGOCD_PASSWORD=$(echo $ARGOCD_CREDS | jq -r .password)",
                                    "ARGOCD_SERVER=$(echo $ARGOCD_CREDS | jq -r .server)",
                                    "argocd login $ARGOCD_SERVER --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD",
                                    "argocd version",
                                    "APP_NAME=$(cat build.json | jq -r '.[0].app_name')",
                                    "REPOSITORY_URI=$(cat build.json | jq -r '.[0].image_name')",
                                    "TAG=$(cat build.json | jq -r '.[0].image_tag')",
                                    "echo \"Login to ECR Registry for docker to push the image to ECR Repository\"",
                                    "echo \"Login in to Amazon ECR...\"",
                                    "$(aws ecr get-login --no-include-email)",
                                    "echo \"Ready to deploy $APP_NAME - $REPOSITORY_URI:$TAG\"",
                                    ]
                    },
                      "build": {
                        "commands": [
                                    "cd $CODEBUILD_SRC_DIR_K8S/$ENV",
                                    "echo 'Update the k8s repository with new image...'",
                                    "CODECOMMIT_CREDS=$(aws secretsmanager get-secret-value --secret-id iac-my-codecommit-secret --query SecretString --output text)",
                                    "CODECOMMIT_USERNAME=$(echo $CODECOMMIT_CREDS | jq -r .username)",
                                    "CODECOMMIT_PASSWORD=$(echo $CODECOMMIT_CREDS | jq -r .password)",
                                    "kustomize edit set image SKILLSETS_API_IMAGE_NAME=$REPOSITORY_URI:$TAG",
                                    "cat kustomization.yaml | head -n 13",
                                    "git config --global user.email \"devops@codepipeline.com\"",
                                    "git config --global user.name \"codesenju\"",
                                    "git add kustomization.yaml",
                                    "git commit -m \"Updated $ENV-$APP_NAME image to $REPOSITORY_URI:$TAG\" || true",
                                    "git push",
                                    ]
                    },
                    "post_build": {
                        "commands": [
                                    "cd $CODEBUILD_SRC_DIR",
                                    "echo \"Create argocd application $ENV-$APP_NAME if does not exist...\"",
                                    "app_exists=$(argocd app get $ENV-$APP_NAME > /dev/null 2>&1; echo $?)",
                                    """if [ $app_exists -ne 0 ]; then
                                        argocd repo add $CODEBUILD_SOURCE_REPO_URL_K8S --username $CODECOMMIT_USERNAME --password $CODECOMMIT_PASSWORD --name $APP_NAME-k8s-manifests
                                        cat argocd.yaml | envsubst | argocd app create --upsert -f -
                                    fi
                                    """,
                                    "echo \"Argocd server application status\"",
                                    "argocd app get $ENV-$APP_NAME --refresh",
                                    "echo \"Wait for argocd server application sync to complete\"",
                                    "argocd app wait $ENV-$APP_NAME",
                                    ]
                    },
                },
            }),
            role=role,
            environment=codebuild.BuildEnvironment(
            environment_variables={
                "EKS_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=EKS_CLUSTER_NAME
                ),
                "ARGOCD_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=ARGOCD_CLUSTER_NAME
                ),
                "ENV": codebuild.BuildEnvironmentVariable(
                    value="dev"
                ),
                "APP_NAME": codebuild.BuildEnvironmentVariable(
                    value=APP_NAME
                ),
                "DEST_SERVER": codebuild.BuildEnvironmentVariable(
                    value=DEST_SERVER
                )
            },
            privileged=True, 
            compute_type=codebuild.ComputeType.SMALL,
            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
            ),
            source=codebuild.Source.code_commit(repository=app_repo),
            secondary_sources=[codebuild.Source.code_commit(repository=k8s_repo,identifier="K8S")]
        )
        
        # Creates Codebuild Project for UAT CD Pipeline
        cd_pipeline_uat = codebuild.Project(self, f"iac_{APP_NAME}_codebuildproject_cd_uat",
            project_name=f"IaC-{APP_NAME}-cd-uat",
            description="CodeBuild Project for EKS DevOps UAT CD Pipeline",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "env": {
                    "git-credential-helper": "yes"
                },
                "phases": {
                    "install": {
                        "commands":[
                                    "echo \"Install kustomize cli...\"",
                                    "curl -sLo /tmp/kustomize.tar.gz  https://github.com/kubernetes-sigs/kustomize/releases/download/kustomize%2Fv5.0.3/kustomize_v5.0.3_linux_amd64.tar.gz",
                                    "tar xzvf /tmp/kustomize.tar.gz -C /usr/bin/ && chmod +x /usr/bin/kustomize && rm -rf /tmp/kustomize.tar.gz",
                                    "kustomize version",
                                    "echo \"Install ARGOCD cli & Authenticate with ARGOCD SERVER...\"",
                                    "curl -sLo /usr/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.7.2/argocd-linux-amd64 && chmod +x /usr/bin/argocd",
                                    "argocd version --client",
                                   ]
                    },
                      "pre_build": {
                        "commands": [
                                    "echo \"Authenticate with Argocd Server...\"",
                                    "ARGOCD_CREDS=$(aws secretsmanager get-secret-value --secret-id iac-my-argocd-secret --query SecretString --output text)",
                                    "ARGOCD_USERNAME=$(echo $ARGOCD_CREDS | jq -r .username)",
                                    "ARGOCD_PASSWORD=$(echo $ARGOCD_CREDS | jq -r .password)",
                                    "ARGOCD_SERVER=$(echo $ARGOCD_CREDS | jq -r .server)",
                                    "argocd login $ARGOCD_SERVER --username $ARGOCD_USERNAME --password $ARGOCD_PASSWORD",
                                    "argocd version",
                                    "APP_NAME=$(cat build.json | jq -r '.[0].app_name')",
                                    "REPOSITORY_URI=$(cat build.json | jq -r '.[0].image_name')",
                                    "TAG=$(cat build.json | jq -r '.[0].image_tag')",
                                    "echo \"Login to ECR Registry for docker to push the image to ECR Repository\"",
                                    "echo \"Login in to Amazon ECR...\"",
                                    "$(aws ecr get-login --no-include-email)",
                                    "echo \"Ready to deploy $APP_NAME - $REPOSITORY_URI:$TAG\"",
                                    ]
                    },
                      "build": {
                        "commands": [
                                    "cd $CODEBUILD_SRC_DIR_K8S/$ENV",
                                    "echo 'Update the k8s repository with new image...'",
                                    "CODECOMMIT_CREDS=$(aws secretsmanager get-secret-value --secret-id iac-my-codecommit-secret --query SecretString --output text)",
                                    "CODECOMMIT_USERNAME=$(echo $CODECOMMIT_CREDS | jq -r .username)",
                                    "CODECOMMIT_PASSWORD=$(echo $CODECOMMIT_CREDS | jq -r .password)",
                                    "kustomize edit set image SKILLSETS_API_IMAGE_NAME=$REPOSITORY_URI:$TAG",
                                    "cat kustomization.yaml | head -n 13",
                                    "git config --global user.email \"devops@codepipeline.com\"",
                                    "git config --global user.name \"codesenju\"",
                                    "git add kustomization.yaml",
                                    "git commit -m \"Updated $ENV-$APP_NAME image to $REPOSITORY_URI:$TAG\" || true",
                                    "git push",
                                    ]
                    },
                    "post_build": {
                        "commands": [
                                    "cd $CODEBUILD_SRC_DIR",
                                    "echo \"Create argocd application $ENV-$APP_NAME if does not exist...\"",
                                    "app_exists=$(argocd app get $ENV-$APP_NAME > /dev/null 2>&1; echo $?)",
                                    """if [ $app_exists -ne 0 ]; then
                                        argocd repo add $CODEBUILD_SOURCE_REPO_URL_K8S --username $CODECOMMIT_USERNAME --password $CODECOMMIT_PASSWORD --name $APP_NAME-k8s-manifests
                                        cat argocd.yaml | envsubst
                                        cat argocd.yaml | envsubst | argocd app create --upsert -f -
                                    fi
                                    """,
                                    "echo \"Argocd server application status\"",
                                    "argocd app get $ENV-$APP_NAME --refresh",
                                    "echo \"Wait for argocd server application sync to complete\"",
                                    "argocd app wait $ENV-$APP_NAME",
                                    ]
                    },
                },
            }),
            role=role,
            environment=codebuild.BuildEnvironment(
            environment_variables={
                "EKS_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=EKS_CLUSTER_NAME
                ),
                "ARGOCD_CLUSTER_NAME": codebuild.BuildEnvironmentVariable(
                    value=ARGOCD_CLUSTER_NAME
                ),
                "ENV": codebuild.BuildEnvironmentVariable(
                    value="uat"
                ),
                "APP_NAME": codebuild.BuildEnvironmentVariable(
                    value=APP_NAME
                ),
                "DEST_SERVER": codebuild.BuildEnvironmentVariable(
                    value=DEST_SERVER
                )
            },
            privileged=True, 
            compute_type=codebuild.ComputeType.SMALL,
            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
            ),
            source=codebuild.Source.code_commit(repository=app_repo),
            secondary_sources=[codebuild.Source.code_commit(repository=k8s_repo,identifier="K8S")]
        )
        # Creates Codebuild Project for Auto Testing CD Pipeline
        cd_pipeline_auto_test = codebuild.Project(self, f"iac_{APP_NAME}_codebuildproject_auto_test",
            project_name=f"IaC-{APP_NAME}-auto-test",
            description="CodeBuild Project for EKS DevOps Automated Testing Pipeline",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                # "env": {
                #     "git-credential-helper": "yes"
                # },
                "phases": {
                    "install": {
                        "commands":[
                                    "echo \"Install k6 cli...\"",
                                    "curl -sLo /tmp/k6.tar.gz https://github.com/grafana/k6/releases/download/v0.45.0/k6-v0.45.0-linux-amd64.tar.gz",
                                    "cd /tmp && tar -xvf /tmp/k6.tar.gz && mv k6-v0.45.0-linux-amd64/k6 /usr/bin/ && chmod +x /usr/bin/k6",
                                    "k6 version"
                                   ]
                    },
                      "build": {
                        "commands": [
                                    "echo 'Create file...'",
                                    """echo "import { sleep } from 'k6';

                                           import http from 'k6/http';
                                           
                                           export const options = {
                                             duration: '$K6_DURATION',
                                             vus: $K6_VUs,
                                             thresholds: {
                                               http_req_duration: ['p(95)<600'], // 95 percent of response times must be below 600ms
                                               http_req_failed: ['rate<0.01'], // http errors should be less than 1%
                                             },
                                           };
                                           
                                           export default function () {
                                             http.get('$APP_ENDPOINT');
                                             sleep(1.5);
                                           }" > script.js""",
                                    "cat script.js",
                                    "echo 'Run performance test...'",
                                    "k6 run script.js",
                                    ]
                    },
                },
            }),
            role=role,
            environment=codebuild.BuildEnvironment(
              environment_variables={
                  "APP_ENDPOINT": codebuild.BuildEnvironmentVariable(
                      value=APP_ENDPOINT
                  ),
                  "ENV": codebuild.BuildEnvironmentVariable(
                      value="uat"
                  ),
                  "APP_NAME": codebuild.BuildEnvironmentVariable(
                      value=APP_NAME
                  ),
                  "K6_DURATION": codebuild.BuildEnvironmentVariable(
                      value="1m"
                  ),
                      "K6_VUs": codebuild.BuildEnvironmentVariable(
                      value="250"
                  )
              },
            # privileged=True, 
            compute_type=codebuild.ComputeType.LARGE,
            build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_4,
            ),
            source=codebuild.Source.code_commit(repository=app_repo),
            secondary_sources=[codebuild.Source.code_commit(repository=k8s_repo,identifier="K8S")]
        )
        
        ############################
        ### CodePipeline Actions ###
        ############################
        # Create app source stage action
        app_source_output = codepipeline.Artifact("APP")
        app_source_action = codepipeline_actions.CodeCommitSourceAction(
           action_name="APP",
           repository=app_repo,
           branch="main",
           output=app_source_output,
        )

        # Create ci build stage action
        ci_build_artifact = codepipeline.Artifact("CIBUILD")
        ci_build_action = codepipeline_actions.CodeBuildAction(
            action_name="Image_Build",
            project=ci_pipeline,
            input=app_source_output,
            #extra_inputs=[k8s_source_output],
            outputs=[ci_build_artifact],
        )

        # Create dev cd build stage action
        cd_build_artifact_dev = codepipeline.Artifact("CDBUILD_dev")
        cd_build_action_dev = codepipeline_actions.CodeBuildAction(
            action_name="Deployment",
            project=cd_pipeline_dev,
            input=ci_build_artifact,
            outputs=[cd_build_artifact_dev],
        )
        # Creates manual approval aciton
        manual_approval = codepipeline_actions.ManualApprovalAction(
            action_name="Approval",
            run_order=1,
            additional_information="Approve request to promote to UAT"
        )
        # Create uat cd build stage action
        cd_build_artifact_uat = codepipeline.Artifact("CDBUILD_uat")
        cd_build_action_uat = codepipeline_actions.CodeBuildAction(
            action_name="Promote_to_UAT",
            project=cd_pipeline_uat,
            input=ci_build_artifact,
            outputs=[cd_build_artifact_uat],
            run_order=2,
        )

        # Create Performance Test cd build stage action
        cd_auto_test_artifact = codepipeline.Artifact("TEST")
        cd_auto_test_action = codepipeline_actions.CodeBuildAction(
            action_name="Performance_Test",
            project=cd_pipeline_auto_test,
            input=ci_build_artifact,
            outputs=[cd_auto_test_artifact],
            run_order=3,
        )
        
        ####################
        ### CodePipeline ###
        ####################
        # Create code pipeline
        pipeline = codepipeline.Pipeline(self, f"iac_{APP_NAME}_pipeline",
            pipeline_name=f"IaC_{APP_NAME}_Pipeline",
            stages=[
            codepipeline.StageProps(
            stage_name="Source",
            actions=[app_source_action]
        ),
            codepipeline.StageProps(
            stage_name="Build",
            actions=[ci_build_action]
        ),
            codepipeline.StageProps(
            stage_name="DEV",
            actions=[cd_build_action_dev]
        ),
            codepipeline.StageProps(
            stage_name="UAT",
            actions=[manual_approval,cd_build_action_uat,cd_auto_test_action],
        ),
        ]
        )
        
        # STACK OUTPUTS
        cdk.CfnOutput(self,f"iac-{APP_NAME}-app-repository",export_name=f"iac-{APP_NAME}-app-repository",value=app_repo.repository_clone_url_http)
        cdk.CfnOutput(self,f"iac-{APP_NAME}-k8s-repository",export_name=f"iac-{APP_NAME}-k8s-repository",value=k8s_repo.repository_clone_url_http)

app=cdk.App()
pipelineStack(app, "SkilllsetsUIPipelineStack", env=cdk.Environment(account=os.getenv("AWS_ACCOUNT_ID"), region=os.getenv("AWS_REGION")),)
app.synth()

# aws ecr delete-repository --repository-name iac-skillsets-ui --force && printf y | cdk destroy --require-approval never && cdk deploy --require-approval never