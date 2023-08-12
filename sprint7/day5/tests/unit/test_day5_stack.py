import aws_cdk as core
import aws_cdk.assertions as assertions

from day5.day5_stack import Day5Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in day5/day5_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Day5Stack(app, "day5")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
