# Sprint 4

## Tasks:


<br>


<br>

## 1) Write unit tests

```python

@pytest.fixture
def test_stack():
    app = core.App()
    stack = Sprint4Stack(app, "sprint4")
    template = assertions.Template.from_stack(stack)
    return template

def test_unit(test_stack):
    test_stack.resource_count_is("AWS::SNS::Subscription",2)
    
def test_unit_resource(test_stack):
    test_stack.all_resources_properties("AWS::Lambda::Function", {
        "Runtime": "python3.9",
        }   
    )

```

<br>

## 2) Write functional test

<br>

```python


def test_availbility(Url = 'google.com'):

    http = urllib3.PoolManager()

    response = http.request("GET", Url)

    if response.status == 200:
        assert 1
    else:
        assert 0


```

<br>

## Create two metrics for the web crawler

<br>

```python

duration_metric = WH.metric('Duration')
invocations_metric = WH.metric('Invocations')

```

<br>

## Create alarms on the metrics
<br>

```python

# Duration alarm

duraction_alarm = cloudwatch.Alarm(self, f"WHDurationAlarm",
                comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
                threshold=1,
                evaluation_periods=1,
                metric=duration_metric
            ) 

# Invocations alarm
        
invocations_alarm = cloudwatch.Alarm(self, "WHInvocationsAlarm",
        comparison_operator=cloudwatch.ComparisonOperator.LESS_THAN_THRESHOLD,
        threshold=1,
        evaluation_periods=1,
        metric = invocations_metric
    )
        

```


<br>

## Configure auto rollback if any of the metrics are in alarm

<br>

```python

config = codedeploy.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE
        
# create lambda alias

# https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Alias.html

version = WH.current_version
alias = lambda_.Alias(self, "LambdaAliasNoman",
    alias_name="Prod",
    version=version
)

# create lamda deployment group

# https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html


deployment_group = codedeploy.LambdaDeploymentGroup(self, "NomanDeployment",
    alarms=[duraction_alarm, invocations_alarm],
    alias=alias,
    deployment_config=config
)


