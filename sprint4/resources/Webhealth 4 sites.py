# lambda function to check the health of the web server

values = dict()

import urllib3
import datetime
from cloudwatch_put_date import AwsCloudWatch
import constant

def lambda_handler(event, context):
    
    cw_client = AwsCloudWatch()
        
    avail = availbility(constant.site_url)
    late = latency(constant.site_url)
    
    dimensions = [{'Name': 'Url','Value': constant.site_url}]
    
    cw_client.cloudwatch_put_date(constant.namespace, constant.AvailbilityMetrics, dimensions, avail)
    cw_client.cloudwatch_put_date(constant.namespace, constant.latencyMetrics, dimensions, avail)
    
    
    # print(avail,late)
    values.update({f'{constant.site_url}' : f'Availbility == > {avail} || Latency == > {late}'})
        
    return values

def availbility(Url):

    http = urllib3.PoolManager()

    response = http.request("GET", Url)

    if response.status == 200:
        return 1
    else:
        return 0
    
def latency(Url):
    
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request('GET', Url)
    end = datetime.datetime.now()
    
    delta = end - start
    
    latencySec = round(delta.microseconds * .000001, 6)
    
    return latencySec