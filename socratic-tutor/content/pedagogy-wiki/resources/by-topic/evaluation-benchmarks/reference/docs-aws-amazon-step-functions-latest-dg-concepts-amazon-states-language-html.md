# Source: https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html
# Title: AWS Step Functions Developer Guide — Amazon States Language (ASL) specification
# Fetched via: jina
# Date: 2026-04-10

Title: Using Amazon States Language to define Step Functions workflows


# Using Amazon States Language to define Step Functions workflows - AWS Step Functions

## Select your cookie preferences

We use essential cookies and similar tools that are necessary to provide our site and services. We use performance cookies to collect anonymous statistics, so we can understand how customers use our site and make improvements. Essential cookies cannot be deactivated, but you can choose “Customize” or “Decline” to decline performance cookies. 

 If you agree, AWS and approved third parties will also use cookies to provide useful site features, remember your preferences, and display relevant content, including relevant advertising. To accept or decline all non-essential cookies, choose “Accept” or “Decline.” To make more detailed choices, choose “Customize.”

Accept Decline Customize

## Customize cookie preferences

We use cookies and similar tools (collectively, "cookies") for the following purposes.

### Essential

Essential cookies are necessary to provide our site and services and cannot be deactivated. They are usually set in response to your actions on the site, such as setting your privacy preferences, signing in, or filling in forms.

### Performance

Performance cookies provide anonymous statistics about how customers navigate our site so we can improve site experience and performance. Approved third parties may perform analytics on our behalf, but they cannot use the data for their own purposes.

- [x]  

Allowed

### Functional

Functional cookies help us provide useful site features, remember your preferences, and display relevant content. Approved third parties may set these cookies to provide certain site features. If you do not allow these cookies, then some or all of these services may not function properly.

- [x]  

Allowed

### Advertising

Advertising cookies may be set through our site by us or our advertising partners and help us deliver relevant marketing content. If you do not allow these cookies, you will experience less relevant advertising.

- [x]  

Allowed

Blocking some types of cookies may impact your experience of our sites. You may review and change your choices at any time by selecting Cookie preferences in the footer of this site. We and selected third-parties use cookies or similar technologies as specified in the[AWS Cookie Notice](https://aws.amazon.com/legal/cookies/).

Cancel Save preferences

## Unable to save cookie preferences

We will only store essential cookies at this time, because we were unable to save your cookie preferences.

If you want to change your cookie preferences, try again later using the link in the AWS console footer, or contact support if the problem persists.

Dismiss


[English](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html# "Language Selector. Currently set to: English")

[Preferences](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

[Contact Us](https://aws.amazon.com/contact-us/?cmpid=docs_headercta_contactus)

[Feedback](https://docs.aws.amazon.com/feedback/doc-feedback.html?hidden_service_name=Step+Functions&topic_url=https%3A%2F%2Fdocs.aws.amazon.com%2Fstep-functions%2Flatest%2Fdg%2Fconcepts-amazon-states-language.html)


[Get started](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

[Service guides](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

[Developer tools](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

[AI resources](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

[Create an AWS Account](https://portal.aws.amazon.com/)

## AWS Step Functions

### Developer Guide

*   [What is Step Functions?](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)
*   [Use cases](https://docs.aws.amazon.com/step-functions/latest/dg/use-cases.html)
*   [Getting started tutorial](https://docs.aws.amazon.com/step-functions/latest/dg/getting-started.html)
*   [State machines](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-statemachines.html)
*   [Activities](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html)
*   [Choosing workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html)
*   
[Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) 

    *   [State machine structure](https://docs.aws.amazon.com/step-functions/latest/dg/statemachine-structure.html)
    *   [Intrinsic functions](https://docs.aws.amazon.com/step-functions/latest/dg/intrinsic-functions.html)

*   
[Workflow states](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-states.html) 

    *   [Task](https://docs.aws.amazon.com/step-functions/latest/dg/state-task.html)
    *   [Choice](https://docs.aws.amazon.com/step-functions/latest/dg/state-choice.html)
    *   [Parallel](https://docs.aws.amazon.com/step-functions/latest/dg/state-parallel.html)
    *   
[Map](https://docs.aws.amazon.com/step-functions/latest/dg/state-map.html) 

        *   [Inline mode](https://docs.aws.amazon.com/step-functions/latest/dg/state-map-inline.html)
        *   [Distributed mode](https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html)

    *   [Pass](https://docs.aws.amazon.com/step-functions/latest/dg/state-pass.html)
    *   [Wait](https://docs.aws.amazon.com/step-functions/latest/dg/state-wait.html)
    *   [Succeed](https://docs.aws.amazon.com/step-functions/latest/dg/state-succeed.html)
    *   [Fail](https://docs.aws.amazon.com/step-functions/latest/dg/state-fail.html)

*   
[Tutorials and Workshops](https://docs.aws.amazon.com/step-functions/latest/dg/learning-resources.html) 

    *   [Handle error conditions](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-handling-error-conditions.html)
    *   [Create a state machine using AWS SAM](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-state-machine-using-sam.html)
    *   [Examine executions](https://docs.aws.amazon.com/step-functions/latest/dg/debug-sm-exec-using-ui.html)
    *   [Create a state machine that uses Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-creating-lambda-state-machine.html)
    *   [Wait for human approval](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-human-approval.html)
    *   [Repeat actions with Inline Map](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-map-inline.html)
    *   [Copy large-scale CSV using Distributed Map](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-map-distributed.html)
    *   [Iterate a loop with Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-create-iterate-pattern-section.html)
    *   [Process batch data with Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-itembatcher-param-task.html)
    *   [Process individual items with Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-itembatcher-single-item-process.html)
    *   [Start a workflow from EventBridge](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html)
    *   [Create an API using API Gateway](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-api-gateway.html)
    *   [Create an Activity state machine](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-creating-activity-state-machine.html)
    *   [View X-Ray traces](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-xray-traces.html)
    *   [Gather Amazon S3 bucket info](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-gather-s3-info.html)
    *   [Continue long-running workflows using Step Functions API (recommended)](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-continue-new.html)
    *   [Using Lambda to continue a workflow](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-use-lambda-cont-exec.html)
    *   [Access cross-account resources](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-access-cross-acct-resources.html)

*   
[Starter templates](https://docs.aws.amazon.com/step-functions/latest/dg/starter-templates.html) 

    *   [Manage a container task](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-container-task-notification.html)
    *   [Transfer data records](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-transfer-data-sqs.html)
    *   [Job poller](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-job-poller.html)
    *   [Task timer](https://docs.aws.amazon.com/step-functions/latest/dg/task-timer-sample.html)
    *   [Callback pattern example](https://docs.aws.amazon.com/step-functions/latest/dg/callback-task-sample-sqs.html)
    *   [Manage an Amazon EMR job](https://docs.aws.amazon.com/step-functions/latest/dg/sample-emr-job.html)
    *   [Run an EMR Serverless job](https://docs.aws.amazon.com/step-functions/latest/dg/sample-emr-serverless-job.html)
    *   [Start a workflow within a workflow](https://docs.aws.amazon.com/step-functions/latest/dg/sample-start-workflow.html)
    *   [Process data with a Map](https://docs.aws.amazon.com/step-functions/latest/dg/sample-map-state.html)
    *   [Distributed Map to process a CSV file in S3](https://docs.aws.amazon.com/step-functions/latest/dg/sample-dist-map-csv-process.html)
    *   [Distributed Map to process files in S3](https://docs.aws.amazon.com/step-functions/latest/dg/sample-dist-map-s3data-process.html)
    *   [Train a machine learning model](https://docs.aws.amazon.com/step-functions/latest/dg/sample-train-model.html)
    *   [Tune a machine learning model](https://docs.aws.amazon.com/step-functions/latest/dg/sample-hyper-tuning.html)
    *   [Perform AI prompt-chaining with Amazon Bedrock](https://docs.aws.amazon.com/step-functions/latest/dg/sample-bedrock-prompt-chaining.html)
    *   [Process high-volume messages from SQS](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-express-high-volume-sqs.html)
    *   [Selective checkpointing example](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-express-selective-checkpointing.html)
    *   [Start a CodeBuild build](https://docs.aws.amazon.com/step-functions/latest/dg/sample-project-codebuild.html)
    *   [Preprocess data and train a machine learning model](https://docs.aws.amazon.com/step-functions/latest/dg/sample-preprocess-feature-transform.html)
    *   [Orchestrate Lambda functions](https://docs.aws.amazon.com/step-functions/latest/dg/sample-lambda-orchestration.html)
    *   [Start an Athena query](https://docs.aws.amazon.com/step-functions/latest/dg/sample-athena-query.html)
    *   [Execute queries in sequence and parallel using Athena](https://docs.aws.amazon.com/step-functions/latest/dg/run-multiple-queries.html)
    *   [Query large datasets](https://docs.aws.amazon.com/step-functions/latest/dg/sample-query-large-datasets.html)
    *   [Keep data up to date](https://docs.aws.amazon.com/step-functions/latest/dg/sample-keep-data-updated.html)
    *   [Manage an Amazon EKS cluster](https://docs.aws.amazon.com/step-functions/latest/dg/sample-eks-cluster.html)
    *   [Make a call to API Gateway](https://docs.aws.amazon.com/step-functions/latest/dg/sample-apigateway-workflow.html)
    *   [Call a microservice with API Gateway](https://docs.aws.amazon.com/step-functions/latest/dg/sample-apigateway-ecs-workflow.html)
    *   [Send a custom event to EventBridge](https://docs.aws.amazon.com/step-functions/latest/dg/sample-eventbridge-custom-event.html)
    *   [Invoke Synchronous Express Workflows through API Gateway](https://docs.aws.amazon.com/step-functions/latest/dg/synchronous-execution.html)
    *   [ETL job in Amazon Redshift](https://docs.aws.amazon.com/step-functions/latest/dg/sample-etl-orchestration.html)
    *   [Manage a batch job](https://docs.aws.amazon.com/step-functions/latest/dg/batch-job-notification.html)
    *   [Fan out a batch job](https://docs.aws.amazon.com/step-functions/latest/dg/sample-batch-fan-out.html)
    *   [Batch job with Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/sample-batch-lambda.html)

*   
[Developing workflows](https://docs.aws.amazon.com/step-functions/latest/dg/developing-workflows.html) 

    *   
[Using Workflow Studio](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio.html) 

        *   [Create a workflow](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio-create.html)
        *   [Configure input and output](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio-process.html)
        *   [Set up execution roles](https://docs.aws.amazon.com/step-functions/latest/dg/manage-state-machine-permissions.html)
        *   [Configure error handling](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio-process-error.html)
        *   [Using Workflow Studio in Infrastructure Composer](https://docs.aws.amazon.com/step-functions/latest/dg/use-wfs-in-app-composer.html)

    *   [Using AWS SAM](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-sam-sfn.html)
    *   [Create a state machine with CloudFormation](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-lambda-state-machine-cloudformation.html)
    *   [Using CDK to create a Standard workflow](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-lambda-state-machine-cdk.html)
    *   [Using CDK to create an Express workflow](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-step-functions-rest-api-integration-cdk.html)
    *   [Using Terraform to deploy workflows](https://docs.aws.amazon.com/step-functions/latest/dg/terraform-sfn.html)
    *   [Exporting to IaC templates](https://docs.aws.amazon.com/step-functions/latest/dg/exporting-iac-templates.html)

*   
[Starting state machines](https://docs.aws.amazon.com/step-functions/latest/dg/statemachine-starting.html) 

    *   [Start from a Task](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-nested-workflows.html)
    *   [Using EventBridge Scheduler](https://docs.aws.amazon.com/step-functions/latest/dg/using-eventbridge-scheduler.html)
    *   [Viewing workflow runs](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-view-execution-details.html)
    *   [Redriving state machines](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html)
    *   [Viewing Map Runs](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-examine-map-run.html)
    *   [Redriving Map Runs](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-map-run.html)

*   
[Processing input and output](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-input-output-filtering.html) 

    *   [Passing data with variables](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-variables.html)
    *   [Transforming data with JSONata](https://docs.aws.amazon.com/step-functions/latest/dg/transforming-data.html)
    *   [Context object](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-contextobject.html)
    *   [Using JSONPath paths](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html)
    *   [Manipulate parameters with paths](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-inputpath-params.html)
    *   [Example: Manipulating state data with paths](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-example.html)
    *   [Specify state output with paths](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultpath.html)
    *   
[Map state configuration](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-fields-dist-map.html) 

        *   [ItemReader](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-itemreader.html)
        *   [ItemsPath (JSONPath)](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-itemspath.html)
        *   [ItemSelector](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-itemselector.html)
        *   [ItemBatcher](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-itembatcher.html)
        *   [ResultWriter](https://docs.aws.amazon.com/step-functions/latest/dg/input-output-resultwriter.html)
        *   [Parsing input CSV files](https://docs.aws.amazon.com/step-functions/latest/dg/example-csv-parse-dist-map.html)

*   
[Integrating services](https://docs.aws.amazon.com/step-functions/latest/dg/integrate-services.html) 

    *   [AWS SDK integrations](https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html)
    *   [Service integration patterns](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html)
    *   [Call HTTPS APIs](https://docs.aws.amazon.com/step-functions/latest/dg/call-https-apis.html)
    *   [Pass parameters](https://docs.aws.amazon.com/step-functions/latest/dg/connect-parameters.html)

*   
[Integrating optimized services](https://docs.aws.amazon.com/step-functions/latest/dg/integrate-optimized.html) 

    *   [Amazon API Gateway](https://docs.aws.amazon.com/step-functions/latest/dg/connect-api-gateway.html)
    *   [Amazon Athena](https://docs.aws.amazon.com/step-functions/latest/dg/connect-athena.html)
    *   [AWS Batch](https://docs.aws.amazon.com/step-functions/latest/dg/connect-batch.html)
    *   [Amazon Bedrock](https://docs.aws.amazon.com/step-functions/latest/dg/connect-bedrock.html)
    *   [AWS CodeBuild](https://docs.aws.amazon.com/step-functions/latest/dg/connect-codebuild.html)
    *   [Amazon DynamoDB](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html)
    *   [Amazon ECS/Fargate](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ecs.html)
    *   [Amazon EKS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-eks.html)
    *   [Amazon EMR](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr.html)
    *   [Amazon EMR on EKS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr-eks.html)
    *   [Amazon EMR Serverless](https://docs.aws.amazon.com/step-functions/latest/dg/connect-emr-serverless.html)
    *   [Amazon EventBridge](https://docs.aws.amazon.com/step-functions/latest/dg/connect-eventbridge.html)
    *   [AWS Glue](https://docs.aws.amazon.com/step-functions/latest/dg/connect-glue.html)
    *   [AWS Glue DataBrew](https://docs.aws.amazon.com/step-functions/latest/dg/connect-databrew.html)
    *   [AWS Lambda](https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html)
    *   [AWS Elemental MediaConvert](https://docs.aws.amazon.com/step-functions/latest/dg/connect-mediaconvert.html)
    *   [Amazon SageMaker AI](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html)
    *   [Amazon SNS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sns.html)
    *   [Amazon SQS](https://docs.aws.amazon.com/step-functions/latest/dg/connect-sqs.html)
    *   [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/connect-stepfunctions.html)

*   
[Securing state machines](https://docs.aws.amazon.com/step-functions/latest/dg/security.html) 

    *   
[Data protection](https://docs.aws.amazon.com/step-functions/latest/dg/data-protection.html) 

        *   [Data at rest encryption](https://docs.aws.amazon.com/step-functions/latest/dg/encryption-at-rest.html)
        *   [Data in transit encryption](https://docs.aws.amazon.com/step-functions/latest/dg/encryption-in-transit.html)

    *   
[Identity and Access Management](https://docs.aws.amazon.com/step-functions/latest/dg/auth-and-access-control-sfn.html) 

        *   [How AWS Step Functions works with IAM](https://docs.aws.amazon.com/step-functions/latest/dg/security_iam_service-with-iam.html)
        *   [Identity-based policy examples](https://docs.aws.amazon.com/step-functions/latest/dg/security_iam_id-based-policy-examples.html)
        *   [AWS managed policies](https://docs.aws.amazon.com/step-functions/latest/dg/security-iam-awsmanpol.html)
        *   [Creating a state machine IAM role](https://docs.aws.amazon.com/step-functions/latest/dg/procedure-create-iam-role.html)
        *   [Creating granular permissions for non-admin users](https://docs.aws.amazon.com/step-functions/latest/dg/concept-create-iam-advanced.html)
        *   [Accessing cross-account AWS resources](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-access-cross-acct-resources.html)
        *   [Create VPC endpoints](https://docs.aws.amazon.com/step-functions/latest/dg/vpc-endpoints.html)
        *   [IAM Policies for integrated services](https://docs.aws.amazon.com/step-functions/latest/dg/service-integration-iam-templates.html)
        *   [IAM policies for Distributed Maps](https://docs.aws.amazon.com/step-functions/latest/dg/iam-policies-eg-dist-map.html)
        *   [Creating tag-based policies](https://docs.aws.amazon.com/step-functions/latest/dg/tag-based-policies.html)
        *   [Troubleshooting identity and access](https://docs.aws.amazon.com/step-functions/latest/dg/security_iam_troubleshoot.html)

*   
[Logging and monitoring](https://docs.aws.amazon.com/step-functions/latest/dg/monitoring-logging.html) 

    *   [Metrics in CloudWatch](https://docs.aws.amazon.com/step-functions/latest/dg/procedure-cw-metrics.html)
    *   [Automate event delivery](https://docs.aws.amazon.com/step-functions/latest/dg/eventbridge-integration.html)
    *   [API calls in CloudTrail](https://docs.aws.amazon.com/step-functions/latest/dg/procedure-cloud-trail.html)
    *   [Logging in CloudWatch Logs](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html)
    *   [Trace data in X-Ray](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-xray-tracing.html)
    *   [Events using User Notifications](https://docs.aws.amazon.com/step-functions/latest/dg/using-user-notifications-sfn.html)

*   
[Testing and debugging](https://docs.aws.amazon.com/step-functions/latest/dg/test-and-debug.html) 

    *   [Testing with TestState](https://docs.aws.amazon.com/step-functions/latest/dg/test-state-isolation.html)
    *   
[Step Functions Local (unsupported)](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local.html) 

        *   [Tutorial: Testing using Step Functions and AWS SAM CLI Local](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-lambda.html)
        *   [Testing with mocked service integrations](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-local-test-sm-exec.html)

*   
[Versions and aliases](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-cd-aliasing-versioning.html) 

    *   [Versions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html)
    *   [Aliases](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-alias.html)
    *   [Versions and alias authorization](https://docs.aws.amazon.com/step-functions/latest/dg/auth-version-alias.html)
    *   [Associating executions with a version or alias](https://docs.aws.amazon.com/step-functions/latest/dg/execution-alias-version-associate.html)
    *   [Deployment example](https://docs.aws.amazon.com/step-functions/latest/dg/example-alias-version-deployment.html)
    *   [Gradual deployment of versions](https://docs.aws.amazon.com/step-functions/latest/dg/version-rolling-deployment.html)

*   [Handling errors](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
*   [Troubleshooting](https://docs.aws.amazon.com/step-functions/latest/dg/troubleshooting.html)
*   [Best practices](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-best-practices.html)
*   [Service quotas](https://docs.aws.amazon.com/step-functions/latest/dg/service-quotas.html)
*   [Recent feature launches](https://docs.aws.amazon.com/step-functions/latest/dg/recent-launches.html)
*   [Document history](https://docs.aws.amazon.com/step-functions/latest/dg/document-history.html)

1.   [Documentation](https://docs.aws.amazon.com/index.html) 
2.   ...           
3.   [AWS Step Functions](https://docs.aws.amazon.com/step-functions/index.html) 
4.   Developer Guide 

1.   [Documentation](https://docs.aws.amazon.com/index.html) 
2.   [AWS Step Functions](https://docs.aws.amazon.com/step-functions/index.html) 
3.   Developer Guide 

# Using Amazon States Language to define Step Functions workflows

[PDF](https://docs.aws.amazon.com/pdfs/step-functions/latest/dg/step-functions-dg.pdf#concepts-amazon-states-language)

[RSS](https://docs.aws.amazon.com/step-functions/latest/dg/recent-updates.rss)


# Using Amazon States Language to define Step Functions workflows - AWS Step Functions

[](https://docs.aws.amazon.com/pdfs/step-functions/latest/dg/step-functions-dg.pdf#concepts-amazon-states-language "Open PDF")

[Documentation](https://docs.aws.amazon.com/index.html)[AWS Step Functions](https://docs.aws.amazon.com/step-functions/index.html)[Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html)

[Example Amazon States Language Specification (JSONata)](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#example-amazon-states-language-specification)

The Amazon States Language is a JSON-based, structured language used to define your state machine, a collection of [states](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-states.html), that can do work (`Task` states), determine which states to transition to next (`Choice` states), stop an execution with an error (`Fail` states), and so on.

For more information, see the [Amazon States Language Specification](https://states-language.net/spec.html) and [Statelint](https://github.com/awslabs/statelint), a tool that validates Amazon States Language code.

To create a state machine on the [Step Functions console](https://console.aws.amazon.com/states/home?region=us-east-1#/) using Amazon States Language, see [Getting Started](https://docs.aws.amazon.com/step-functions/latest/dg/getting-started.html).

###### Note

If you define your state machines outside the Step Functions' console, such as in an editor of your choice, you must save your state machine definitions with the extension _.asl.json_.

## Example Amazon States Language Specification (JSONata)

```
{
  "Comment": "An example of the Amazon States Language using a choice state.",
  "QueryLanguage": "JSONata",
  "StartAt": "FirstState",
  "States": {
    "FirstState": {
      "Type": "Task",
      "Assign": {
        "foo" : "{% $states.input.foo_input %}" 
        },
      "Resource": "arn:aws:lambda:region:123456789012:function:FUNCTION_NAME",
      "Next": "ChoiceState"
    },
    "ChoiceState": {
      "Type": "Choice",
      "Default": "DefaultState",
      "Choices": [
        {
          "Next": "FirstMatchState",
          "Condition": "{% $foo = 1 %}"
        },
        {
          "Next": "SecondMatchState",
          "Condition": "{% $foo = 2 %}"
        }
      ]
    },
    "FirstMatchState": {
      "Type" : "Task",
      "Resource": "arn:aws:lambda:region:123456789012:function:OnFirstMatch",
      "Next": "NextState"
    },

    "SecondMatchState": {
      "Type" : "Task",
      "Resource": "arn:aws:lambda:region:123456789012:function:OnSecondMatch",
      "Next": "NextState"
    },

    "DefaultState": {
      "Type": "Fail",
      "Error": "DefaultStateError",
      "Cause": "No Matches!"
    },

    "NextState": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:123456789012:function:FUNCTION_NAME",
      "End": true
    }
  }
}
```

[Document Conventions](https://docs.aws.amazon.com/general/latest/gr/docconventions.html)

Choosing workflow type

State machine structure

Did this page help you? - Yes

Thanks for letting us know we're doing a good job!

If you've got a moment, please tell us what we did right so we can do more of it.

Did this page help you? - No

Thanks for letting us know this page needs work. We're sorry we let you down.

If you've got a moment, please tell us how we can make the documentation better.

*   
### On this page

    1.   [Example Amazon States Language Specification (JSONata)](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#example-amazon-states-language-specification)

*   ### Related resources [Step Functions API Reference](https://docs.aws.amazon.com/step-functions/latest/apireference) [AWS CLI commands for Step Functions](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/) [Amazon States Language Specification](https://states-language.net/spec.html)    
*   Did this page help you?   Yes No     [Provide feedback](https://docs.aws.amazon.com/feedback/doc-feedback.html?hidden_service_name=Step+Functions&topic_url=https%3A%2F%2Fdocs.aws.amazon.com%2Fstep-functions%2Flatest%2Fdg%2Fconcepts-amazon-states-language.html)     
*        

#### Next topic:

[State machine structure](https://docs.aws.amazon.com/step-functions/latest/dg/statemachine-structure.html)

#### Previous topic:

[Choosing workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html)

## Get Started

[AWS Hands-On Tutorials](https://aws.amazon.com/getting-started/hands-on/)

[AWS Solutions Library](https://aws.amazon.com/solutions/)

[AWS Decision Guides](https://aws.amazon.com/getting-started/decision-guides/)

## Service Guides

[Choosing a generative AI service](https://docs.aws.amazon.com/generative-ai-on-aws-how-to-choose/)

[AWS service guides](https://docs.aws.amazon.com/#products)

[AWS CLI Tutorials on GitHub](https://github.com/aws-samples/sample-developer-tutorials)

## Developer Tools

[AWS Code Example Library](https://docs.aws.amazon.com/code-library/latest/ug/what-is-code-library.html)

[AWS CLI](https://docs.aws.amazon.com/cli/)

[AWS Builder Center](https://builder.aws.com/)

[AWS Developer Tools Blog](https://aws.amazon.com/blogs/developer/)

## Helpful Links

[Download the AWS Docs MCP Server](https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server)

[Sign into the AWS Console](https://console.aws.amazon.com/)

[AWS re:Post](https://repost.aws/)

[Privacy](https://aws.amazon.com/privacy)

[Site terms](https://aws.amazon.com/terms)

[Cookie preferences](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html#)

 © 2026, Amazon Web Services, Inc. or its affiliates. All rights reserved.

English

Language selector

Top