import json, boto3, os, datetime



dbb = boto3.resource('dynamodb')
db_table = os.environ['TABLE_NAME']
table = dbb.Table(db_table)


client = boto3.client('cloudwatch')


def lambda_handler(event, context):
    
    dimension = [{'Name': 'Values','Value': 'argu'}]
    
    if event['httpMethod'] == 'POST' and event['path'] == '/Product':
        
        try:
            body = json.loads(event['body'])
            
            
            '''
            
            {
    "id":"2",
    "arg":[{"event1":{"attr1": "20" }}] 
    "arg": "20"
}
            
            '''
            
            
            if type(body['arg']) == list:
                item = {
                'id': body['id'],
                'timestamps': str(datetime.datetime.now()),
                'arg' : body['arg'][0]["event1"]["attr1"],
                'event': body["arg"]
            }
                cloudwatch_put_data(int(item['arg']), dimension) 
                
                
            else:
                item = {
                'id': body['id'],
                'timestamps': str(datetime.datetime.now()),
                'arg' : body['arg'],
                'event': body
            }
                cloudwatch_put_data(int(item['arg']), dimension)
            
            
            
            
            table.put_item(Item=item)
            
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
                
                
                
    if event['httpMethod'] == 'GET' and event['path'] == '/Product':
        
        products = table.scan()['Items']
        
        sort = sorted(products, key=lambda k: k['timestamps'], reverse=True)
        
        events = []
        
        for i in range(len(sort)):
            if i != 10:
                events.append(sort[i]["event"])
        
        
        
        return {
            'statusCode': 200,
            'body': json.dumps(events)
        }
        
            
            
def cloudwatch_put_data(value, dimension):
    
    response = client.put_metric_data(
                Namespace='Noman_day2_namespace',
                MetricData=[
                    {
                        'MetricName': 'arguments',
                        'Dimensions': dimension,
                        'Value': value,
                    },
                ]
            )
            
