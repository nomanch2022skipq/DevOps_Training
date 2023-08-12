import os, boto3
from collections import Counter

arn = os.environ['TOPIC_ARN']
s3 = boto3.client('s3')
sns = boto3.client('sns')


count1 = {}

def lambda_handler(event, context):
    print("Hello World", arn)
    
    objects = s3.list_objects(Bucket="nomantest2")
    
    for obj in objects['Contents']:
        Key = obj['Key']
    

    
    
        z = s3.get_object(
            Bucket = "nomantest2",
            Key=Key,
        )
        
        data = z['Body'].read().decode('utf-8')
        
        print(type(data))
        
        new_data = data.split(" ")
        
        counter = Counter(new_data)
        
        
        for i in counter.items():
            print(i.key, i.value)
            
    
        with open('/tmp/results.txt', 'a') as f:
            f.write(f'The data of that File {Key} \n{str(counter)}')
        
        
    s3.upload_file('/tmp/results.txt', 'nomantest2', 'output/results.txt')
    
    sns.publish(TopicArn=arn, Message=str(counter), Subject="Count values of the file")
    
  

    return "hello"
    