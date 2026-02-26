---
title: "Using hybrid-cloud to cost-optimize AI workloads"
excerpt: "Migrating AI workloads from AWS Lambda to on-premises Kubernetes to cut costs."
categories:
  - Infrastructure
tags:
  - kubernetes
  - aws
  - bedrock
  - hybrid-cloud
  - cost-optimization
---

The AWS bill notification had become a monthly reminder of cloud convenience at a cost: $75+ with a growing percentage going to AI services through Bedrock. Though only 5% of my total, these AI costs were trending upward — fast. As an old-school engineer with servers humming in my home office, I couldn’t help but wonder: why was I paying Amazon for compute I already owned? That question launched me into creating a hybrid-cloud architecture that would keep the best parts of AWS while bringing lightweight compute workloads back where they belonged — on my own hardware, running on my own terms.

### Background

I built a Lambda-based Bedrock API proxy as a self-managed OpenAPI-compatible REST API in October 2024. I created a [CDK package](https://github.com/kuhl-haus/bedrock-access-gateway-cdk/tree/mainline) to deploy the infrastructure with improvements like retrieving API keys from Secrets Manager instead of SSM Parameter Store, enabling TLS, and restricting access to my WAN IP. While this worked, Bedrock API usage only accounted for 5% of my costs.

Here’s the cost breakdown for the past 5 months of usage:

* 77%: VPC, ELB, and Route 53
* 17%: KMS, Secrets Manager, and Tax
* 5%: Bedrock
* 1%: Other (including free-tier Lambda)

Moving compute on-premises eliminates 77% of costs, with further savings from reduced Secrets Manager and KMS usage. The compute needs are minimal — even 10-year-old hardware can handle it, as Bedrock does the heavy lifting.

![](/assets/images/posts/using-hybrid-cloud-to-cost-optimize-ai-workloads/img-01.png)

Of note, I shutdown my test stack because I didn’t use it and it didn’t make sense to pay for a VPC, ELB, etc. That’s the big drop in cost at the tail-end of January.

![](/assets/images/posts/using-hybrid-cloud-to-cost-optimize-ai-workloads/img-02.png)

*Average daily cost of AWS Lambda-based API*

I created the CDK package to automate infrastructure deployments to my standards. I’ll call these my “V1 Problems”.

### V1 Problems

1. [INFRASTRUCTURE] Sample CFN template does not use TLS; does not redirect HTTP to HTTPS
2. [INFRASTRUCTURE] Sample CFN template SG port 80 open to the world
3. [INFRASTRUCTURE] Cannot create `SecretString` SSM Parameters via CDK/CFN
4. [CODE] Sample code uses SSM to store API Key — requires Secrets Manager integration to enable creating all infrastructure via CDK
5. [INFRASTRUCTURE] Lambda cold starts results in slow/spotty performance

### V1 Solutions

I addressed the first three problems through my CDK package: implementing TLS/access restrictions, creating secrets via CDK. I addressed the fourth problem by forking the sample code to use Secrets Manager. For cold starts (P5), I added a simple canary that hits the health check URL to keep Lambda hydrated.

[P1, P2] <https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/cdk/stacks/load_balancer_stack.py>

[P3] <https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/cdk/stacks/rest_api_stack.py#L113-L128>

[P4] <https://github.com/kuhl-haus/bedrock-access-gateway/tree/fec84aac1d454abf9b0c46c8e8c8ad5f26cca79c>

[P5] <https://github.com/aws-samples/bedrock-access-gateway/blob/main/src/api/app.py#L39-L42>

This approach had a side-effect: Lambdas have a 15-minute timeout. Sometimes a request hits a Lambda with seconds left before termination, causing transient errors. With Lambdas terminating 4 times hourly, the chance of this happening is about 0.22% per hour. Seems low, but how does this play out over time?

The cumulative probability grows significantly:

* 1.75% over an 8-hour day
* 5.15% over 24 hours
* 30.93% over a week
* 79.52% over a month

Like occasional network glitches — annoying but manageable.

Keeping a Lambda running 24\*7 just to avoid cold-start delays is clearly viable but has some sharp edges. My canary invokes every 5 minutes and only uses a few milliseconds of compute per invocation — well within the perpetual free-tier usage. As a result, the cost is negligible. However, it could get expensive if I implemented one or more of the following: a deep health check that consumes more compute, increased concurrency, increased invocation frequency.

### Need for V2

The architecture implemented in the sample is hosted entirely in AWS (of course!). The cost to call the Bedrock APIs is trivial compared to the costs for VPC, ELB, etc. The cost for the Lambda is negligible because my usage sits in the perpetual free-tier range but the performance is subpar. Switching to a container-based version would solve the performance problems but running an ECS cluster is not free, unlike the Lambda. Considering the requirements — [1 vCPU and 2GB of RAM](https://github.com/aws-samples/bedrock-access-gateway/blob/main/deployment/BedrockProxyFargate.template#L246-L258) — it is possible to self-host the container on a Raspberry Pi. That said, I have on-prem Kubernetes clusters for running containers, so that’s what I’m going to do.

Another cost concern is the “free-tier usage” that I get each month. After 1-year, I no longer get the free-tier stuff and I’m paying full price. By moving the API on-premises, not only do I reduce my AWS costs, but I’ll avoid having a heart attack when I get my invoice after my free-tier pricing expires.

### V2 Problems

1. Suboptimal Lambda performance
2. Optimize AWS costs — It’s cool for a PoC but will be expensive long-term.

### V2 Solutions

1. [Performance] Switch from Lambda to container-based solution (P1)
2. [Cost] Move the workload on-premises. (P2)

### [Optimize Performance] Platform Change

Changing platforms from AWS Lambda to a container will eliminate the problems caused by cold-starts and 15-minute timeouts.

The API code is deployed as a container image that exposes an HTTP endpoint to provide an Open AI compatible REST API. All of the heavy-lifting for AI is performed by AWS Bedrock. Simply build the image and upload it to AWS Elastic Container Registry (ECR) — both implementations pull from ECR. Code-wise, no changes are required to switch platforms so this is purely an infrastructure change.

### [Optimize Cost] Move the workload on-premises

Considering only 5% of my costs come from Bedrock and the requirements for hosting the API are so trivial, it makes sense to bring that on-premises. I’m solving problem 2 by migrating the HTTP handler running in on-premises Kubernetes. I already have a self-hosted image repository and TLS certificates are free and automated via ACME/Kubernetes so, the problems that I need to solve by bringing the workload on-premises are:

1. Credentials for accessing the AWS API
2. Adding the Secret ARN to the API configuration

The Lambda uses an IAM role to grant access to the AWS APIs. Instead of using an IAM role, I’ll create an IAM User + Access Key. Though I’d prefer to use IAM Anywhere, it requires a private CA and depending on the approach taken, adds complexity (self-hosted CA) or cost (AWS-hosted CA). I’ll consider adding IAM Anywhere later because I’d prefer to use ephemeral creds, but an Access Key will work for now.

I could use a self-hosted Secret store, like Vault, or something but I’m going to keep Secrets Manager since the call rate will be infrequent. Switching to another technology would increase the scope too much. However, this will make configuration a pain in the ass — the Secret ARN is different in each account/region/environment and if the ARN changes, for any reason, I have to redeploy. I could probably figure out a way to use CDK but the solution would be brittle and hacky, so I need a better solution.

The original implementation used SSM Parameter but I switched to Secrets Manager so I could programmatically create the Secret via CDK. I’m going to solve this by combining the two solutions. I will use SSM parameter to store the Secret ARN, instead of the API key. I’ll use the same SSM Parameter name across all regions/accounts/environments, effectively giving me an abstraction layer. It will require two API calls but now configuration is simplified. These values will be fetched on start-up and then cached in memory. Since we’re going to run this in a container, unlike a Lambda, the API calls will be infrequent. This only required a small change to my fork. ([Here’s the completed code](https://github.com/kuhl-haus/bedrock-access-gateway/tree/4a9cc106a24187f6fe1fb733fc5b294938ecf226).)

AWS components needed for an on-premises hybrid stack:

* Secrets Manager Secret — generates initial API key, stores it, and manages rotation
* SSM Parameter — consistent name used across all regions/environments/accounts, contains ARN of the secret with the API key.
* KMS Customer-Managed Key
* IAM User
* IAM Group
* IAM Policy

[**bedrock-access-gateway-cdk/README.md at mainline · kuhl-haus/bedrock-access-gateway-cdk**  
*Example CDK to deploy AWS Lambda infrastructure that is compatible aws-samples/bedrock-access-gateway …*github.com](https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/README.md#deploy-the-self-hosted-stack "https://github.com/kuhl-haus/bedrock-access-gateway-cdk/blob/mainline/README.md#deploy-the-self-hosted-stack")

### Impact

![](/assets/images/posts/using-hybrid-cloud-to-cost-optimize-ai-workloads/img-02.png)

*Average daily cost of AWS Lambda-based API*

![](/assets/images/posts/using-hybrid-cloud-to-cost-optimize-ai-workloads/img-03.png)

*Average daily cost of on-premises hybrid*

There’s an opportunity to save $0.32/day on secrets management, but I will deal with that in a month or so.

![](/assets/images/posts/using-hybrid-cloud-to-cost-optimize-ai-workloads/img-04.png)

*AWS ALB cost $1.08 per day once free-tier usage is exceeded.*

### Next Steps

The Bedrock API GW sample code is great for building a proof-of-concept and, for the most part, just simply works right out of the box. However, there’s no application-level metrics or instrumentation and I’m restricted to the use-cases supported by the maintainers. In my next post, I’m going to show you how I will turn this into something that meets my particular needs.
