import json
import os
import boto3

dynamodb = boto3.resource("dynamodb")
db_table = os.environ['Noman_crud_table']
table = dynamodb.Table(db_table)


cloudwatch = boto3.client("cloudwatch")


def lambda_handler(event, context):
    
    
    if event["path"] == "/product" and event["httpMethod"] == "POST":
        
        try:
        
            body = json.loads(event["body"])
            
            item = {
                "id" : body["id"],
                "arg" : body["arg"]
            }
            
                
            cloudwatch.put_metric_data(
                Namespace='Noman_design_namespace',
                MetricData=[
                    {
                        'MetricName': 'event_alarm',
                        'Dimensions': [
                            {
                                'Name': 'arg',
                                'Value': "user_value_by_api"
                            },
                        ],
                        'Value': int(body['arg']),
                        
                    },
                ]
            )
            
            
            
            
            table.put_item(
                Item = item
            )
            
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "message": "Data successfully added to the database",
                    "data": item
                })
            }
            
        except Exception as e:
                return {
                    "statusCode": 500,
                    "body": json.dumps({
                        "message": "Failed to add data to the database",
                        "error": str(e)
                    })
                }