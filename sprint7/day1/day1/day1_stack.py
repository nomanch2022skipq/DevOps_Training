from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
    aws_cloudwatch as cloudwatch,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    
    # aws_sqs as sqs,
)
from constructs import Construct

class Day1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lamda_role = self.create_lambda_role()

        # lambda for dynamodb
        
        db_lambda = self.create_lambda("db_lambda", "./resources", "dbcrud.lambda_handler", lamda_role)
        
        # code for database
        
        
        db_table = dynamodb.Table(self, "crud_table_noman",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
        )
        
        # make envoinment variable and give permission to the lambda
        
        db_lambda.add_environment("Noman_crud_table", db_table.table_name)
        db_table.grant_read_write_data(db_lambda)
        
        print(db_table.table_name)
        
        
        
        api = apigateway.RestApi(self, "NomanAPiGateay",
                rest_api_name = "Noman_api_Day1",
                endpoint_types=[apigateway.EndpointType.REGIONAL]
            )
        
        handler = apigateway.LambdaIntegration(db_lambda)
        
        resource = api.root.add_resource('product')
        resource.add_method("POST", handler)
        
        
        # get Metric
        
        metric = cloudwatch.Metric(
            namespace="Noman_design_namespace",
            metric_name="event_alarm",
            dimensions_map={
                'arg': "user_value_by_api"
            }
            
            )
        
        alarm = cloudwatch.Alarm(self, "Noman_alarm",
            evaluation_periods=1,
            metric=metric,
            threshold=10,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD    
            
        )
        
        # sns topic
        
        my_topic = sns.Topic(self, "Topic")

        my_topic.add_subscription(subscriptions.EmailSubscription("mnomanch786@gmail.com"))
        
        
        
        
        
    
    
    
    # function for creating DB Lambda Function.
    
    def create_lambda(self, id, asset , handler, lambda_role):
        return lambda_.Function( self,
        id = id,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        role=lambda_role
        
    )
        
    # function for creating lambda role
    
    def create_lambda_role(self):
        return iam.Role(self, "Noman_lambda_role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                # iam.ManagedPolicy.from_aws_managed_policy_name("BasicExecutionRole"),
                
            ]
        )