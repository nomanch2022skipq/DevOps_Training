import boto3, os

admin_arn = os.environ['admin_arn']
user_arn = os.environ['user_arn']

def lambda_handler(event, context):
    
    client = boto3.client('logs', region_name='us-east-2')
    
    admin_report = ""
    user_report = ""
    
    log_group = "/aws/lambda/NomanWhPlusCwMetricsPlusDya-WHSprint2Stack3EDA8453-T8C0kHq9uyZb"
    log_stream = "2023/03/14/[$LATEST]fc486b67c6e048d6898d6d812324c428"
    # start_time = 0
    # end_time = 10000
    
    response = client.get_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        # startTime=start_time,
        # endTime=end_time,
        startFromHead=True
    )
    
    z = response["events"]
    
    for i in range(len(z)):
        if z[i]['message'].startswith("REPORT"):
            print(z[i]['message'] + '/n')
            admin_report = admin_report + z[i]['message']
            
            
    for i in range(len(z)):
        user_report = user_report + z[i]['message']
        
    sns = boto3.client('sns')
    
    sns.publish(
        TopicArn=admin_arn,
        # PhoneNumber='03074604891',
        Message=admin_report,
        Subject="Reports for Admin",
        
    )
    
    sns.publish(
        TopicArn=user_arn,
        # PhoneNumber='03074604891',
        Message=user_report,
        Subject="Reports for User",
        
    )
        
    
    return admin_report
    
    