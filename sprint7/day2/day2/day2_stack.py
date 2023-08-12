from urllib.request import HTTPRedirectHandler
from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_lambda as lambda_,
    # aws_sqs as sqs,
    aws_dynamodb as dynamodb,
    aws_apigateway as apigateway,
)
from constructs import Construct

class Day2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.lambda_role()
        
        dblambda = self.create_lambda("dbcrud", "./resources", "dbcrud.lambda_handler", lambda_role)
        
        dbtable = dynamodb.Table(self, "Noman_Table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
        )
        
        
        dblambda.add_environment("TABLE_NAME", dbtable.table_name)
        dbtable.grant_read_write_data(dblambda)
        
        
        api = apigateway.RestApi(self, "NomanApiGateway",
            rest_api_name="NomanApiGateway",
            endpoint_types=[apigateway.EndpointType.REGIONAL]
        )
        
        resource = api.root.add_resource("Product")
        
        handler = apigateway.LambdaIntegration(dblambda)
        
        resource.add_method("GET", handler)
        
        resource.add_method("POST", handler)
        
        
        
        
        
        

    
    def create_lambda(self, id, asset, handler, lambda_role):
        return lambda_.Function(self, 
            id = id,
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler=handler,
            code=lambda_.Code.from_asset(asset),
            role = lambda_role,
            timeout=Duration.seconds(300)
    )
        
    def lambda_role(self):
        return iam.Role(self, 
            id = "lambda-role",
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess")
                
            ]
        )
