from venv import create
from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_apigateway as apigateway,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct


class Day7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambda_role = self.create_lambda_role()
        
        fn = self.create_lambda("day7_Noman_lambda","./resources", "day7_lambda.lambda_handler", lambda_role)
        
        api = apigateway.RestApi(self, "Api",
            rest_api_name="MyApi",
            endpoint_types=[apigateway.EndpointType.REGIONAL],
        )
        res = api.root.add_resource("product")
        res.add_method("POST", apigateway.LambdaIntegration(fn))
        
    
    
    
    
    
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
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"),
                ],
            )
