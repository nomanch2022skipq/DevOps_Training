from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    pipelines as pipelines,
    aws_codepipeline_actions as actions,
    Stage,
)
import aws_cdk as cdk
from constructs import Construct

# from resources import constant

from sprint4.sprint4_stack import Sprint4Stack


class StageNoman(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # add stage of sprint3
        
        self.stage = Sprint4Stack(self, 'NomanStage')