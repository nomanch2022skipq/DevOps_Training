# Sprint 7 =============> Design Sprint ============> Day 8
<br>
<br>

## Tasks

<br>
<br>

### You are a DevOps engineer working at a big tech company and your manager has given you a task to migrate a three-tier PHP-based monolithic application to microservices. Consider the scenario that the application is running on a EC2 server with ALB in front of it. Now design an E2E architecture that would containerize the application.
<br>
<br>

### Expectation:
### 1) How the application would be migrated to microservices
### 2) Need a running application of container based services
### 3) The application should have an E2E CI/CD pipeline that would build the application and deploy the updated code/manifest on the container-based services
### 4) Design the above architecture in draw.io

<br>
<br>

## Solution

<br>
<br>

### 1) How the application would be migrated to microservices

<br>
<br>

I migrated the application to microservices by using the following steps:

<br>

1. I break the application into modules and then I create a separate docker image for each module.

2. I connect db with each module separately.

<br>
<br>

![screenshot](images/convert_into_microservices.jpg)


<br>
<br>

### 2) Need a running application of container based services

<br>
<br>

I created a running application of container-based services by using the following steps:

<br>
1. I create images of all modules and attach them with the ALB and DB.

<br>
<br>

![screenshot](images/monolithic_to_micro.jpg)

<br>
<br>

### 3) The application should have an E2E CI/CD pipeline that would build the application and deploy the updated code/manifest on the container-based services

<br>
<br>

I created an E2E CI/CD pipeline that would build the application and deploy the updated code/manifest on the container-based services by using the following steps:

<br>

1. I create a CI/CD pipeline for each module and connect it with the github repo.

2. Whenever I push any changes in the github repo, the CI/CD pipeline will automatically build the application and deploy the updated code/manifest on the container-based services.

<br>
<br>

![screenshot](images/ci_cd_for_microservice.jpg)



