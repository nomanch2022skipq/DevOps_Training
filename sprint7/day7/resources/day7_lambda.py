import json, os, boto3

from boto3.s3.transfer import TransferConfig

s3 = boto3.client('s3')



def lambda_handler(event, context):
    
    
    if event['httpMethod'] == 'POST' and event['path'] == '/product':
        
        
        try:
            config = TransferConfig(multipart_threshold=5 * 1024 * 1024)
            
            with open("Free_Test_Data_10.5MB_PDF.pdf", 'rb') as file:
                s3.upload_fileobj(file, 'nomantest2', 'test.pdf', Config=config)
            
            
            
            
            return {
                'statusCode': 200,
                'body': json.dumps('File uploaded successfully')
            }
            
        except Exception as e:
            return {
                'statusCode': 500,
                "body": json.dumps(str(e))
            }