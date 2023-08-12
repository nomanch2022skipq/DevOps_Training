from functools import partial
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    pipelines as pipelines,
    aws_codebuild as codebuild,
    aws_codepipeline_actions as actions,
)
import aws_cdk as cdk
from constructs import Construct
# from resources import constant

from sprint6.StageNoman import StageNoman


class NomanStackPipeline(Stack):
    

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        

        # Create a source: GitHub
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipelineSource.html#:~:text=%22latest%22%0A)-,classmethod,CodePipelineSource,-classmethod
        
        source = pipelines.CodePipelineSource.git_hub(
            "nomanch2022skipq/EaglePython",
            "main",
            authentication = cdk.SecretValue.secrets_manager("pipeline_test_n"),
            trigger = actions.GitHubTrigger('POLL')
            
            )

        
        # Create a shell script step to run cdk synth
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/ShellStep.html
        
        synth=pipelines.ShellStep("Synth",
            input=source,
            commands=['ls',
                    "cd noman_ch/sprint6", 
                    'npm install -g aws-cdk',
                    "pip install -r requirements.txt", 
                    "cdk synth"
                    
                ],
            primary_output_directory="noman_ch/sprint6/cdk.out"
        )
        
        
        
        
        # Create a pipeline and add the synth step
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        
        pipeline = pipelines.CodePipeline(self, "NomanStackPipeline",synth = synth)
        
        
        # that create 2 stages for the pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        
        
        
        # Add unite terting in alpha pre stage.
        alpha = StageNoman(self, "alpha")
        
        
        docker_url_test =[
        pipelines.CodeBuildStep("PyDockerTest",
            commands=[],
            build_environment = codebuild.BuildEnvironment(
                # The user of a Docker image asset in the pipeline requires turning on
                # 'dockerEnabledForSelfMutation'.
                build_image = codebuild.LinuxBuildImage.from_asset(self, "Image",
                    directory="./docker_image"
                ).from_docker_registry(name = "docker:dind"),
                privileged=True,
            ),
            partial_build_spec = codebuild.BuildSpec.from_object({
                "version": 0.2,
                "phases": {
                    "install": {
                    "commands": [
                        "nohup /usr/local/bin/dockerd --host=unix:///var/run/docker.sock --host=tcp://127.0.0.1:2375 --storage-driver=overlay2 &",
                        "timeout 15 sh -c \"until docker info; do echo .; sleep 1; done\""
                    ]
                },

                    
                    "pre_build": {
                    "commands": [
                        "cd noman_ch/sprint6/docker_image", 
                        "docker build -t get_test ."
                    ]
                    
                    },
                    "build": {
                    "commands": [
                        "docker images",
                        "docker run get_test"
                    ]
                    }
                }
                })
            
            )]
        
        
        
        pipeline.add_stage(alpha,post= docker_url_test, pre=[
            
            pipelines.ShellStep("Pytest",
            input=source,
            commands=['ls',
                    "cd noman_ch/sprint6", 
                    'npm install -g aws-cdk',
                    "pip install -r requirements.txt", 
                    "pip install -r requirements-dev.txt", 
                    'python -m pytest'
                    
                ],
            # primary_output_directory="noman_ch/sprint6/cdk.out"
            )
            
            
        ])
        
        
        
        prod = StageNoman(self, "prod")
        
        # that two stages add to the pipeline, one is alpha and another is prod
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        
        prod = pipeline.add_stage(prod, pre=[
            pipelines.ManualApprovalStep("ApproveProd")
        ])
        
        
        
        
        
        