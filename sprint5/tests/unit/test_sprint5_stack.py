import importlib as imp
from re import A, template
import aws_cdk as core
import aws_cdk.assertions as assertions
import urllib3
# from resources.Webhealth import availbility
# from resources import Cloud_watch_putData

import pytest
from sprint5.sprint5_stack import Sprint5Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in sprint4/sprint4_stack.py
# def test_sqs_queue_created():
#     app = core.App()
#     stack = Sprint4Stack(app, "sprint4")
#     template = assertions.Template.from_stack(stack)
#     

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })


@pytest.fixture
def test_stack():
    app = core.App()
    stack = Sprint5Stack(app, "sprint4")
    template = assertions.Template.from_stack(stack)
    return template


# def test_unit(test_stack):
#     test_stack.resource_count_is("AWS::SNS::Subscription",2)
    
# def test_unit2(test_stack):
#     test_stack.resource_count_is("AWS::Lambda::Function",3)
    
# def test_unit3(test_stack):
#     test_stack.resource_count_is("AWS::SNS::Topic",1)
    
# def test_unit4(test_stack):
#     test_stack.resource_count_is("AWS::CloudWatch::Alarm",16)
    
# def test_unit5(test_stack):
#     test_stack.resource_count_is("AWS::SNS::Subscription",2)
    

    
def test_unit_resource(test_stack):
    test_stack.all_resources_properties("AWS::Lambda::Function", {
        "Runtime": "python3.9",
        }   
    )
    
    
    
    
# add availability module from resources folder and go in Webhealth.py file and add the below code

def test_availbility(Url = 'google.com'):

    http = urllib3.PoolManager()

    response = http.request("GET", Url)

    if response.status == 200:
        assert 1
    else:
        assert 0

    
    
    
    
    

    

    
    
    