from os import environ
from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_events as events_,
    aws_cloudwatch as cloudwatch,
    aws_events_targets as targets,
    aws_lambda as lambda_,
    RemovalPolicy,
    aws_iam as iam_,
    aws_sns as sns,
    aws_cloudwatch_actions as cw_actions,
    aws_sns_subscriptions as subscriptions,
    aws_dynamodb as dynamodb,
    aws_codedeploy as codedeploy,
    aws_apigateway as apigateway,
)
from constructs import Construct
from resources import constant

class Sprint6Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        lambda_role = self.create_lambda_role()
        '''
        That is webhealth lambda function creation
        '''
        WH = self.create_lambda("WHSprint2Stack", "./resources", "Webhealth.lambda_handler", lambda_role)
        # create alarm of lambda function duration
        
        # dimension = {'FunctionName' : WH.function_name}
        
        # print(dimension)
        
        duration_metric = WH.metric('Duration')
        ConcurrentExecutions_metric = WH.metric('ConcurrentExecutions')
        
        
        # duration_metric = cloudwatch.Metric(
        #         metric_name = 'Duration',
        #         namespace='AWS/Lambda',
        #         dimensions_map = dimension

            
        #     )
        
        # ConcurrentExecutions_metric = cloudwatch.Metric(
        #         metric_name = 'ConcurrentExecutions',
        #         namespace='AWS/Lambda',
        #         dimensions_map = dimension

            
        #     )
        
        
        # create configuration for lambda deployment
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentConfig.html
        
        duraction_alarm = cloudwatch.Alarm(self, "DurationError",
                metric=duration_metric,                       
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=900,
                evaluation_periods=60,
            )
        
        # create alarm of lambda function invocations
        
        
        ConcurrentExecutions_alarm = cloudwatch.Alarm(self, "ConcurrentExecutionsError",
                metric = ConcurrentExecutions_metric,
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=60,
            )
        
        
        
        # create lambda alias
        
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html
        
        version = WH.current_version
        alias = lambda_.Alias(self, "NomanLambda_Alias",
            alias_name="Prod_phase",
            version=version
        )
        
        # create lamda deployment group

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html
        
        
        deployment_group = codedeploy.LambdaDeploymentGroup(self, "DeploymentGroup",
            alarms=[duraction_alarm, ConcurrentExecutions_alarm],
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_5_MINUTES
        )
        
        
      
        
        WH.apply_removal_policy(RemovalPolicy.DESTROY)
        
        
        '''
        That is Dynamo DB lambda function creation
        '''
        
        dbLambda = self.create_lambda("dynamoDBSprint2Stackdb", "./resources", "DBApp.lambda_handler", lambda_role)
        dbTable = self.create_dynamo_table()
        
        # create DyanmoDB table for Crud operation

        dbcrudLambda = self.create_lambda("dynamoDBSprint2Stackdbcrud", "./resources", "DBCrud.lambda_handler", lambda_role)
        dbcruddTable = self.create_dynamo_crud_table()
        # that define the time of lambda function execution with 60 minutes.
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events/Schedule.html
        
        schedule = events_.Schedule.rate(Duration.minutes(1))
        
        # that define the target of lambda function.
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events_targets/LambdaFunction.html
        
        target = targets.LambdaFunction(handler=WH)
        
        rule = events_.Rule(self, "Rule",

            schedule = schedule,
            targets = [target]
        
        )
        
        # apply removal policy on rule
        rule.apply_removal_policy(RemovalPolicy.DESTROY)
        
        '''
        Create sns topic if avalability is less than 1 or latency is greater 
        than 0.5 then sns send notification to emeail.
        
        url : https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns/Topic.html
        
        '''
        Topic = sns.Topic(self, "WHNofications")
        
        '''
        Sms Subscription
        url : https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns_subscriptions/SmsSubscription.html
        '''
        
        Topic.add_subscription(subscriptions.EmailSubscription("mnomanch786@gmail.com"))
        
        
        for i in range(len(constant.site_url)):
            
            dimensions = {'Url' : constant.site_url[i]}
        
            '''
            that is Avalability Alarm Code
            
            that link is for Alarm : https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Alarm.html
            
            that link is use for Metric : https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch/Metric.html
            
            '''
            
            
            avalilability_Metric = cloudwatch.Metric(
                metric_name = constant.AvailbilityMetrics,
                namespace=constant.namespace,
                dimensions_map = dimensions

            
            )
            
            avalilability_alarm = cloudwatch.Alarm(self, f"{constant.site_url[i]}_Avalilability",
                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=avalilability_Metric
            )
            
            avalilability_alarm.add_alarm_action(cw_actions.SnsAction(Topic))
 # type: ignore            
            '''
            that is latency Alarm Code
            '''
            
            latency_Metric = cloudwatch.Metric(
                metric_name = constant.latencyMetrics,
                namespace=constant.namespace,
                dimensions_map= dimensions

            
            )

            latency_alarm = cloudwatch.Alarm(self, f"{constant.site_url[i]}_Latency",
                comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,
                threshold=0.73,
                evaluation_periods=1,
                metric=latency_Metric
            )
            
            latency_alarm.add_alarm_action(cw_actions.SnsAction(Topic))
            
            
            
        
            
    
            
            
        """
        Create a table in dynamo DB
        """
        dbTable.grant_read_write_data(dbLambda)
        dbLambda.add_environment("Noman__table", dbTable.table_name)
        # Topic.add_subscription(subscriptions.LambdaSubscription(dbLambda))
        
        
        dbcruddTable.grant_read_write_data(dbcrudLambda)
        dbcrudLambda.add_environment("Noman_crud_table", dbcruddTable.table_name)
        
        Topic.add_subscription(subscriptions.LambdaSubscription(dbLambda))
        
            
        '''
        
        Create api gateway for crud operation
        
        and make methods for get, post, put, delete
        
        '''
        
        # Create the API Gateway
        # api = apigateway.RestApi(self, "NomanApiGateway")

        # # Create the resource for the crawlers
        # crawlers = api.root.add_resource("crawlers")

        # # Create the GET method to retrieve a list of crawlers
        # crawlers.add_method("GET", apigateway.LambdaIntegration(dbcrudLambda))

        # # Create the POST method to create a new crawler
        # crawlers.add_method("POST", apigateway.LambdaIntegration(dbcrudLambda))
        
        api = apigateway.RestApi(self, "NomanApiGateway", 
                rest_api_name="NomanApiGateway",
                endpoint_types=[apigateway.EndpointType.REGIONAL])
        handle = apigateway.LambdaIntegration(dbcrudLambda)
        crud = api.root.add_resource('Product')
        crud.add_method("POST", handle)
        crud.add_method("GET", handle)
        crud.add_method("DELETE", handle)
        crud.add_method("PUT", handle)
        
        crud = api.root.add_resource('Products')
        crud.add_method("GET", handle)
        
        
        # # Deploy the API to a stage named "prod"
        # deployment = apigateway.Deployment(self, "Deployment", api=api, description="Deploying to prod")
        # stage = apigateway.Stage(self, "ProdStage", deployment=deployment, stage_name="prod")
         
        
        
        
        
    
        
        
        
        
            
            
            
    
            
    # that create lambda function.
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html    
            
    def create_lambda(self, id, asset, handler, role):
        return lambda_.Function(self, 
            id = id,
            code=lambda_.Code.from_asset(asset),
            handler=handler,
            role = role,
            runtime=lambda_.Runtime.PYTHON_3_9,
            timeout=Duration.minutes(5),
            
        )
        
    '''
    that code is use for to create table into the dyanamo Db
    '''
    
    
    def create_dynamo_table(self):
        '''
        https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html
        '''
        table = dynamodb.Table(self, "Noman__table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="timestamps", type=dynamodb.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
            
            )
        return table
    
    # dynamo table for crud operation
    
    def create_dynamo_crud_table(self):
        
        table = dynamodb.Table(self, "Noman_crud_table",
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            # sort_key=dynamodb.Attribute(name="url", type=dynamodb.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
            
            )
        return table
    
        
        
        
        
        
        
        
        
    
    def create_lambda_role(self):       
        lambdaRole = iam_.Role(self, "Lambda_Role",            
        assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"), 
        managed_policies=[              
            iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
            iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
            # iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"),
            # role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess")),
            
            ])
        
        return lambdaRole
    
    
    
    
    
    
    
    

        