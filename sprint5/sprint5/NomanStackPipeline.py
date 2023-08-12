from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    pipelines as pipelines,
    aws_codepipeline_actions as actions,
)
import aws_cdk as cdk
from constructs import Construct
# from resources import constant

from sprint5.StageNoman import StageNoman


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
                    "cd noman_ch/sprint5", 
                    'npm install -g aws-cdk',
                    "pip install -r requirements.txt", 
                    "cdk synth"
                    
                ],
            primary_output_directory="noman_ch/sprint5/cdk.out"
        )
        
        
        
        
        # Create a pipeline and add the synth step
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/CodePipeline.html
        
        pipeline = pipelines.CodePipeline(self, "NomanStackPipeline",synth = synth)
        
        
        # that create 2 stages for the pipeline
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.core/Stage.html
        
        
        
        # Add unite terting in alpha pre stage.
        alpha = StageNoman(self, "alpha")
        pipeline.add_stage(alpha, pre=[
            
            pipelines.ShellStep("Pytest",
            input=source,
            commands=['ls',
                    "cd noman_ch/sprint5", 
                    'npm install -g aws-cdk',
                    "pip install -r requirements.txt", 
                    "pip install -r requirements-dev.txt", 
                    'python -m pytest'
                    
                ],
            # primary_output_directory="noman_ch/sprint5/cdk.out"
            )
            
            
        ])
        
        
        
        prod = StageNoman(self, "prod")
        
        # that two stages add to the pipeline, one is alpha and another is prod
        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/CodePipeline.html
        
        prod = pipeline.add_stage(prod, pre=[
            pipelines.ManualApprovalStep("ApproveProd")
        ])
        
        
        
        
        
        