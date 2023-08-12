# sprint 5

<br>

## Make Resources and Methods of the API Gateway

```python

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



```

<br>

### Make GET, POST, PUT, DELETE methods for Product and Products resources.

<br>

For GET method of all items, we will use the following code:


```python

if event["path"] == "/Products" and event["httpMethod"] == "GET":
        products = table.scan()['Items']
        
        print(event)
        # Return the data to the caller.
        return {
            'statusCode': 200,
            'body': json.dumps(products)
        }
        
```

<br>

For GET method of a single item, we will use the following code:

```python

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

```

<br>

For POST method, we will use the following code:

```python

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

```

<br>

For PUT method, we will use the following code:

```python

if event["path"] == "/Product" and event["httpMethod"] == "PUT":
        
    body = json.loads(event['body'])
    id = body['id']
    url = body['url']
    
    response = table.update_item(
        Key={
            'id': id
        },
        UpdateExpression="set url = :r",
        ExpressionAttributeValues={
            ':r': url
        },
        ReturnValues="UPDATED_NEW"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Data updated successfully : {response}')
    }

```

<br>

For DELETE method, we will use the following code:

```python   

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
        'body': json.dumps(f'Data deleted successfully : {response}')
    }

```
