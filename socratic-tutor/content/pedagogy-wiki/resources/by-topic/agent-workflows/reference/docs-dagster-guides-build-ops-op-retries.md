# Source: https://docs.dagster.io/guides/build/ops/op-retries
# Title: Op retries - Dagster Docs
# Fetched via: jina
# Date: 2026-04-09

Title: Op retries | Dagster Docs



# Op retries | Dagster Docs

Opens in a new window Opens an external website Opens an external website in a new window

This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics, personalization, and targeted advertising. To learn more, view the following link: [Privacy Policy](https://dagster.io/privacy)

Manage Preferences 


**Developing with AI? Check out our new [AI skills](https://github.com/dagster-io/skills)!**


[Latest (1.13.0)](https://docs.dagster.io/guides/build/ops/op-retries)
*   [Latest (1.13.0)](https://docs.dagster.io/guides/build/ops/op-retries)
*   [Version 1.12 (1.12.8)](https://release-1-12-8.archive.dagster-docs.io/)
*   [Version 1.11 (1.11.16)](https://release-1-11-16.archive.dagster-docs.io/)
*   [Version 1.10 (1.10.21)](https://release-1-10-21.archive.dagster-docs.io/)
*   [Version 1.9 (1.9.13)](https://release-1-9-13.archive.dagster-docs.io/)
*   [1.9.9 and earlier](https://legacy-docs.dagster.io/)
*   [Upcoming release (Preview)](https://main.archive.dagster-docs.io/)

[Sign in](https://dagster.plus/)[Try Dagster+](https://dagster.plus/signup)


*   [Getting Started](https://docs.dagster.io/guides/build/ops/op-retries#) 
    *   [Overview](https://docs.dagster.io/)
    *   [Quickstart (Dagster+ Hybrid and OSS)](https://docs.dagster.io/getting-started/quickstart)
    *   [Quickstart (Dagster+ Serverless)](https://docs.dagster.io/getting-started/quickstart-serverless)
    *   [Installation](https://docs.dagster.io/getting-started/installation)
    *   [Concepts](https://docs.dagster.io/getting-started/concepts)
    *   [AI tools](https://docs.dagster.io/getting-started/ai-tools)
    *   [Dagster University](https://courses.dagster.io/)
    *   [Python primer](https://dagster.io/blog/python-packages-primer-1)

*   [Tutorial](https://docs.dagster.io/dagster-basics-tutorial) 
    *   [Projects](https://docs.dagster.io/dagster-basics-tutorial/projects)
    *   [Assets](https://docs.dagster.io/dagster-basics-tutorial/assets)
    *   [Resources](https://docs.dagster.io/dagster-basics-tutorial/resources)
    *   [Asset dependencies](https://docs.dagster.io/dagster-basics-tutorial/dependencies)
    *   [Asset checks](https://docs.dagster.io/dagster-basics-tutorial/asset-checks)
    *   [Automation](https://docs.dagster.io/dagster-basics-tutorial/schedules)
    *   [Components](https://docs.dagster.io/dagster-basics-tutorial/custom-components)
    *   [Dagster basics tutorial](https://docs.dagster.io/dagster-basics-tutorial)

*   [Build](https://docs.dagster.io/guides/build) 
    *   [Build pipelines](https://docs.dagster.io/guides/build)
    *   [Projects and workspaces](https://docs.dagster.io/guides/build/projects) 
    *   [Assets](https://docs.dagster.io/guides/build/assets) 
    *   [Components](https://docs.dagster.io/guides/build/components) 
    *   [Partitions and backfills](https://docs.dagster.io/guides/build/partitions-and-backfills) 
    *   [External resources](https://docs.dagster.io/guides/build/external-resources) 
    *   [I/O managers](https://docs.dagster.io/guides/build/io-managers) 
    *   [Ops](https://docs.dagster.io/guides/build/ops) 
        *   [Op events and exceptions](https://docs.dagster.io/guides/build/ops/op-events)
        *   [Op hooks](https://docs.dagster.io/guides/build/ops/op-hooks)
        *   [Op retries](https://docs.dagster.io/guides/build/ops/op-retries)
        *   [Op graphs](https://docs.dagster.io/guides/build/ops/graphs)
        *   [Nesting op graphs](https://docs.dagster.io/guides/build/ops/nesting-graphs)
        *   [Dynamic graphs](https://docs.dagster.io/guides/build/ops/dynamic-graphs)

    *   [Jobs](https://docs.dagster.io/guides/build/jobs) 

*   [Automate](https://docs.dagster.io/guides/automate) 
    *   [Automate](https://docs.dagster.io/guides/automate)
    *   [Schedules](https://docs.dagster.io/guides/automate/schedules) 
    *   [Declarative Automation](https://docs.dagster.io/guides/automate/declarative-automation) 
    *   [Sensors](https://docs.dagster.io/guides/automate/sensors) 
    *   [Asset sensors](https://docs.dagster.io/guides/automate/asset-sensors)

*   [Operate](https://docs.dagster.io/guides/operate) 
    *   [Configuration](https://docs.dagster.io/guides/operate/configuration) 
    *   [Operating pipelines](https://docs.dagster.io/guides/operate)
    *   [Dagster webserver and UI](https://docs.dagster.io/guides/operate/webserver)
    *   [User settings in the UI](https://docs.dagster.io/guides/operate/ui-user-settings)
    *   [Run executors](https://docs.dagster.io/guides/operate/run-executors)
    *   [Managing concurrency](https://docs.dagster.io/guides/operate/managing-concurrency) 
    *   [Transitioning from development to production](https://docs.dagster.io/guides/operate/dev-to-prod)

*   [Log & debug](https://docs.dagster.io/guides/log-debug) 
    *   [Logging & debugging pipelines](https://docs.dagster.io/guides/log-debug)
    *   [Logging](https://docs.dagster.io/guides/log-debug/logging) 
    *   [Debugging](https://docs.dagster.io/guides/log-debug/debugging) 

*   [Observe](https://docs.dagster.io/guides/observe) 
    *   [Asset catalog (Dagster+)](https://docs.dagster.io/guides/observe/asset-catalog) 
    *   [Alerts (Dagster+)](https://docs.dagster.io/guides/observe/alerts) 
    *   [Asset health status (Dagster+)](https://docs.dagster.io/guides/observe/asset-health-status)
    *   [Asset freshness policies](https://docs.dagster.io/guides/observe/asset-freshness-policies)
    *   [Insights (Dagster+)](https://docs.dagster.io/guides/observe/insights) 
    *   [Observe](https://docs.dagster.io/guides/observe)

*   [Test](https://docs.dagster.io/guides/test) 
    *   [Testing assets](https://docs.dagster.io/guides/test)
    *   [Asset checks](https://docs.dagster.io/guides/test/asset-checks)
    *   [Running a subset of asset checks](https://docs.dagster.io/guides/test/running-a-subset-of-asset-checks)
    *   [Unit testing assets and ops](https://docs.dagster.io/guides/test/unit-testing-assets-and-ops)
    *   [Testing partitioned config and jobs](https://docs.dagster.io/guides/test/testing-partitioned-config-and-jobs)
    *   [Data contracts with asset checks](https://docs.dagster.io/guides/test/data-contracts)

*   [Labs](https://docs.dagster.io/guides/labs) 
    *   [Compass AI assistant (Dagster+)](https://docs.dagster.io/guides/labs/compass-ai-assistant)
    *   [Connections](https://docs.dagster.io/guides/labs/connections) 
    *   [Labs](https://docs.dagster.io/guides/labs)
    *   [Webhooks](https://docs.dagster.io/guides/labs/webhook-alerts) 

    *   [Community](https://docs.dagster.io/about/community)
    *   [Contributing code](https://docs.dagster.io/about/contributing)
    *   [Contributing documentation](https://docs.dagster.io/about/contributing-docs) 
    *   [Dagster telemetry](https://docs.dagster.io/about/telemetry)
    *   [Releases](https://docs.dagster.io/about/releases)
    *   [Changelog](https://docs.dagster.io/about/changelog)
    *   [Data portability](https://docs.dagster.io/about/data-portability)

*   [](https://docs.dagster.io/)
*   [Build](https://docs.dagster.io/guides/build)
*   [Ops](https://docs.dagster.io/guides/build/ops)
*   Op retries

On this page

# Op retries

Assets vs ops

If you are just getting started with Dagster, we strongly recommend you use [assets](https://docs.dagster.io/guides/build/assets) rather than ops to build your data pipelines. The ops documentation is for Dagster users who need to manage existing ops, or who have complex use cases.

When an exception occurs during op execution, Dagster provides tools to retry that op within the same job run.

## Relevant APIs[​](https://docs.dagster.io/guides/build/ops/op-retries#relevant-apis "Direct link to Relevant APIs")

| Name | Description |
| --- | --- |
| [`RetryRequested`](https://docs.dagster.io/api/dagster/ops#dagster.RetryRequested) | An exception that can be thrown from the body of an op to request a retry |
| [`RetryPolicy`](https://docs.dagster.io/api/dagster/ops#dagster.RetryPolicy) | A declarative policy to attach which will have retries requested on exception |
| [`Backoff`](https://docs.dagster.io/api/dagster/ops#dagster.Backoff) | Modification to delay between retries based on attempt number |
| [`Jitter`](https://docs.dagster.io/api/dagster/ops#dagster.Jitter) | Random modification to delay beween retries |

## Overview[​](https://docs.dagster.io/guides/build/ops/op-retries#overview "Direct link to Overview")

In Dagster, code is executed within an [op](https://docs.dagster.io/guides/build/ops). Sometimes this code can fail for transient reasons, and the desired behavior is to retry and run the function again.

Dagster provides both declarative [`RetryPolicy`](https://docs.dagster.io/api/dagster/ops#dagster.RetryPolicy) as well as manual [`RetryRequested`](https://docs.dagster.io/api/dagster/ops#dagster.RetryRequested) exceptions to enable this behavior.

## Using op retries[​](https://docs.dagster.io/guides/build/ops/op-retries#using-op-retries "Direct link to Using op retries")

Here we start off with an op that is causing us to have to retry the whole job anytime it fails.

src/<project_name>/defs/ops.py

`@dg.opdef problematic():    fails_sometimes()`

### `RetryPolicy`[​](https://docs.dagster.io/guides/build/ops/op-retries#retrypolicy "Direct link to retrypolicy")

To get this op to retry when an exception occurs, we can attach a [`RetryPolicy`](https://docs.dagster.io/api/dagster/ops#dagster.RetryPolicy).

src/<project_name>/defs/ops.py

`@dg.op(retry_policy=dg.RetryPolicy())def better():    fails_sometimes()`

This improves the situation, but we may need additional configuration to control how many times to retry and/or how long to wait between each retry.

src/<project_name>/defs/ops.py

`@dg.op(    retry_policy=dg.RetryPolicy(        max_retries=3,        delay=0.2,  # 200ms        backoff=dg.Backoff.EXPONENTIAL,        jitter=dg.Jitter.PLUS_MINUS,    ))def even_better():    fails_sometimes()`

In addition to being able to set the policy directly on the op definition, it can also be set on specific invocations of an op, or a [`@dg.job`](https://docs.dagster.io/api/dagster/jobs#dagster.job) to apply to all ops contained within.

src/<project_name>/defs/ops.py

`default_policy = dg.RetryPolicy(max_retries=1)flakey_op_policy = dg.RetryPolicy(max_retries=10)@dg.job(op_retry_policy=default_policy)def default_and_override_job():    problematic.with_retry_policy(flakey_op_policy)()`

info

Retry policies also work for asset jobs.

src/<project_name>/defs/ops.py

`import randomimport dagster as dg@dg.assetdef sample_asset():    if random.choice([True, False]):        raise Exception("failed")sample_job = dg.define_asset_job(    name="sample_job",    selection="sample_asset",    op_retry_policy=dg.RetryPolicy(max_retries=3),)`

### `RetryRequested`[​](https://docs.dagster.io/guides/build/ops/op-retries#retryrequested "Direct link to retryrequested")

In certain more nuanced situations, we may need to evaluate code to determine if we want to retry or not. For this we can use a manual [`RetryRequested`](https://docs.dagster.io/api/dagster/ops#dagster.RetryRequested) exception.

src/<project_name>/defs/ops.py

`@dg.opdef manual():    try:        fails_sometimes()    except Exception as e:        if should_retry(e):            raise dg.RetryRequested(max_retries=1, seconds_to_wait=1) from e        else:            raise`

Using `raise from` will ensure the original exceptions information is captured by Dagster.

[Edit this page](https://github.com/dagster-io/dagster/tree/master/docs/docs/guides/build/ops/op-retries.md)

[Previous Op hooks](https://docs.dagster.io/guides/build/ops/op-hooks)[Next Op graphs](https://docs.dagster.io/guides/build/ops/graphs)

*   [Relevant APIs](https://docs.dagster.io/guides/build/ops/op-retries#relevant-apis)
*   [Overview](https://docs.dagster.io/guides/build/ops/op-retries#overview)
*   [Using op retries](https://docs.dagster.io/guides/build/ops/op-retries#using-op-retries)
    *   [`RetryPolicy`](https://docs.dagster.io/guides/build/ops/op-retries#retrypolicy)
    *   [`RetryRequested`](https://docs.dagster.io/guides/build/ops/op-retries#retryrequested)

[Terms of Service](https://www.dagster.io/terms)[Privacy Policy](https://www.dagster.io/privacy/)[Security](https://www.dagster.io/security/)[Cookie Preferences](https://docs.dagster.io/guides/build/ops/op-retries)

[![Image 3](https://docs.dagster.io/icons/twitter.svg)](https://twitter.com/dagster "X")[![Image 4](https://docs.dagster.io/icons/slack.svg)](https://www.dagster.io/slack/ "Community Slack")[![Image 5](https://docs.dagster.io/icons/github.svg)](https://github.com/dagster-io/dagster "GitHub")[![Image 6](https://docs.dagster.io/icons/youtube.svg)](https://www.youtube.com/channel/UCfLnv9X8jyHTe6gJ4hVBo9Q/videos "Youtube")


Copyright 2026 Dagster Labs

Ask Dagster AI

![Image 9](https://bat.bing.com/action/0?ti=343107175&tm=gtm002&Ver=2&mid=b08fae05-a783-43f2-a67b-b45f69d0d76d&bo=1&sid=2056ecf0347e11f19febc90db411be3b&vid=20579230347e11f1b098cd7de399e07b&vids=1&msclkid=N&pi=918639831&lg=en-US&sw=800&sh=600&sc=24&tl=Op%20retries%20%7C%20Dagster%20Docs&p=https%3A%2F%2Fdocs.dagster.io%2Fguides%2Fbuild%2Fops%2Fop-retries&r=&lt=635&evt=pageLoad&sv=2&cdb=ARoR&rn=825338)