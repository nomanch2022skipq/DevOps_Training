import aws_cdk as core
import aws_cdk.assertions as assertions

from day6.day6_stack import Day6Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in day6/day6_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Day6Stack(app, "day6")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
