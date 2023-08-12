from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_logs as logs,
    aws_sns_subscriptions as subscriptions,
    aws_sns as sns,
)
from constructs import Construct

class Day6Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        
        fn = self.create_lambda("day6_Noman_lambda","./resources", "day6_lambda.lambda_handler", lambda_role)
        
        
        my_topic = sns.Topic(self, "Noman_topic")

        my_topic.add_subscription(subscriptions.EmailSubscription("mnomanch786@gmail.com"))
        
        fn.add_environment("admin_arn", my_topic.topic_arn)
        
        my_topic_2 = sns.Topic(self, "Noman_2_topic")

        my_topic_2.add_subscription(subscriptions.EmailSubscription("nomanchskipq@gmail.com"))
        
        fn.add_environment("user_arn", my_topic_2.topic_arn)
    
    
    def create_lambda(self, id, path, handler, role):
        return lambda_.Function(self,
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_8,
            code=lambda_.Code.from_asset(path),
            handler=handler,
            timeout=Duration.seconds(100),
            role=role
        )
        
        
    def create_lambda_role(self):
        return iam.Role(self, "Noman_role5",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                
                
                ],
            )
