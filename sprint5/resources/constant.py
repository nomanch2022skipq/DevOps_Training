import json
import urllib3

# for metric in cw_client.list_metrics():

site_url = ['skip.org', 'google.com', 'facebook.com', 'youtube.com']
namespace = 'Noman_ch_NameSpace'
AvailbilityMetrics = "URL_Avalability"
latencyMetrics = "URL_Letancy"

# for pic data from the dynamoDB and add into the site_url list

# test_url = 'https://05of9w89zc.execute-api.us-east-2.amazonaws.com/prod/Products'
    
# http = urllib3.PoolManager()

# response = http.request("GET", test_url)

# response_byte = response.data

# my_json = response_byte.decode('utf8').replace("'", '"')

# loop = json.loads(my_json)

# for i in loop:
#     site_url.append(i['url'])






