import json
import os
import boto3

ddb = boto3.resource('dynamodb')
table_name = os.environ['Noman_crud_table']
table = ddb.Table(table_name)


def lambda_handler(event, context):
    # Fetch all the data from the database.
    
    '''
    
    that get all the data from the database
    
    '''
    
    if event["path"] == "/Products" and event["httpMethod"] == "GET":
        products = table.scan()['Items']
        
        print(event)
        # Return the data to the caller.
        return {
            'statusCode': 200,
            'body': json.dumps(products)
        }
        
    '''
    
    that insert the data into the database
    
    '''    
    
        
    if event["path"] == "/Product" and event["httpMethod"] == "POST":
        
        body = json.loads(event['body'])
        item = {
            'id': body['id'],
            'url': body['url']
        }
    
        table.put_item(Item=item)
    
        response = {
            'statusCode': 200,
            'body': json.dumps(f'Data inserted successfully : {item}')
        }
        
        return response
        
    
    # get one item from the database and my path is /Product/{id}
    
    if event["path"] == "/Product" and event["httpMethod"] == "GET" and event['queryStringParameters']:
        
        id = event['queryStringParameters']["id"]
        print(id)
        
        response = table.get_item(
            Key={
                'id': id
            }
        )
        
        
        
        item = response['Item']
        
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    
    # Delete one item from the database and my path is /Product and my method is DELETE
    
    if event["path"] == "/Product" and event["httpMethod"] == "DELETE" and event['queryStringParameters']:
        
        id = event['queryStringParameters']["id"]
        print(id)
        
        response = table.delete_item(
            Key={
                'id': id
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'ID {id} deleted successfully')
        }
    
    # put one item from the database and my path is /Product and my method is PUT
    
    if event["path"] == "/Product" and event["httpMethod"] == "PUT":
        
        body = json.loads(event['body'])
        url = body['url']
        id = body['id']
        
        response = table.update_item(
                Key={
                    'id': id,
                },
                UpdateExpression='SET #updateUrl = :u',
                ExpressionAttributeValues={
                    ':u': url
                },
                ExpressionAttributeNames={
                    '#updateUrl': 'url'
                },
                ReturnValues='UPDATED_NEW'
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(f'ID {id} updated successfully')
        }