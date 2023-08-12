import boto3
import os

def lambda_handler(event, context):
    
    dynamodb = boto3.resource('dynamodb')
    record = event['Records'][0]['Sns']
    
    print(event)
    
  
    db_name = os.environ['Noman__table']
    
    table = dynamodb.Table(db_name)
    
    table.put_item(
        Item={
            'id' : record["MessageId"],
            'timestamps' : record['Timestamp'],
            'Message' :  record["Message"], 
            'Subject' : record["Subject"]
            
        }
    )
    
