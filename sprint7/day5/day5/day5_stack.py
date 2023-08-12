from venv import create
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_iam as iam,
)
from constructs import Construct

class Day5Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_role = self.create_lambda_role()

        fn = self.create_lambda_function("Noman_design5", "./resources/", "design_5.lambda_handler", lambda_role)
        
        
        topic = sns.Topic(self, "Noman_topic5")
        sub = topic.add_subscription(sns_subscriptions.EmailSubscription("mnomanch786@gmail.com"))
        
        # how to get arn of the topic
        
        arn = topic.topic_arn
        
        fn.add_environment("TOPIC_ARN", arn)
        
        
        
    def create_lambda_function(self, id, asset, handler, role):
        return lambda_.Function(self, 
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            role=role,
        )

    def create_lambda_role(self):
        return iam.Role(self, "Noman_role5",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                ],
            )
        
        