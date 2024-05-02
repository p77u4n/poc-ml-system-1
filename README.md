# Simple POC for Educational Purpose

# Domain

Machine Learning Processing

## SubDomain - Bounded context 

### Core Domain

Machine Learning Processing system

### Supporting Domain

    - Uploading File, Progress Status Reporting
    - Web Interface for User

# Problem Assumption and Requirement

1. The machine learning work is resource-intensive task
2. Our system must be acted as an robusness service eventhough behind it our service is very busy of processing the machine learning work

# Solution

We need at lease two service that do two unrelated concern
    * For interacting, as a direct interface of our system to the end user
    * For running the machine learning job

Our solution for our system avaibility is decoupling two service using asynchronous communication method, message-queue communicating pattern

## Service

![system layout](https://pub-655b129b1b4f44dda33a7f1a9bf4d857.r2.dev/Untitled-2023-11-24-1104.png "system layout")

### The Machine learning service

Written in Domain Driven design, Hexagon Architecture, using parsing-not-validate pattern for model integration logic.
    * source code folder: here
    * written in Python

[source](https://github.com/p77u4n/poc-ml-system-1/tree/master/modules/machine-learning)

### The Nodejs service 

Works as an interface interacting directly to our end user
    * Accepting user input
        * Upload file to a object storage, or datalake
    * Initiate the task and has a data model instance in a shared memory accross services
        * We use postgres for our sharing memory between services

[source](https://github.com/p77u4n/poc-ml-system-1/tree/master/modules/portal-service)

#### GRPC
The main service would be exposed by GRPC interface

#### RestAPi
We have expressjs rest api for interacting with the user interface like Webapp

### React App

Only for web interface
    * Communicate with the nodejs service via Rest API

[source](https://github.com/p77u4n/poc-ml-system-1/tree/master/modules/webapp)
    
